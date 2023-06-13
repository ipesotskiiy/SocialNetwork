from django.db import IntegrityError
from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from users.models import User
from users.serializers import RegisterSerializer, UserSerializer


class RegisterUserAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                token = AccessToken.for_user(user)
                refreshToken = RefreshToken.for_user(user)
                resp = Response({"user": UserSerializer(user, context=self.get_serializer_context()).data,
                                 "token": str(token), "refreshToken": str(refreshToken)
                                 })
                return resp

            else:
                return Response({"message": 'not valid'})

        except IntegrityError as e:
            account = User.objects.get(username='')
            account.delete()
            raise ValidationError({"400": f'{str(e)}'})

        except KeyError as e:
            print(e)
            raise ValidationError({"400": f'Field {str(e)} missing'})
