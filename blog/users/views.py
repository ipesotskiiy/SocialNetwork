from rest_framework import generics, viewsets, response, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User, Follower
from users.serializers import UserSerializer, MyTokenObtainPairSerializer, RegisterSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        users = User.objects.all().order_by('login')
        serializer = UserSerializer(instance=users, many=True)
        return Response(serializer.data)


class RegisterUserAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return Response({
            'user': serializer.data,
            'refresh_token': str(refresh),
            'access_token': str(access_token)
        }, status=status.HTTP_201_CREATED)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserFollowingViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = UserSerializer
    queryset = Follower.objects.all()

    def create(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except Follower.DoesNotExist:
            return response.Response(status=404)
        Follower.objects.create(subscriber=request.user, user=user)
        return response.Response(status=201)

    def destroy(self, request, pk):
        try:
            sub = Follower.objects.get(subscriber=request.user, user=pk)
        except Follower.DoesNotExist:
            return response.Response(status=404)
        sub.delete()
        return response.Response(status=204)
