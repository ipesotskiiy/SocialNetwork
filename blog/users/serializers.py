from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User, Follower


class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ('id', 'subscriber', 'created')


class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ('id', 'user', 'created')


class UserSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'login', 'following', 'followers')

    def get_following(self, obj):
        return FollowingSerializer(obj.user.all(), many=True).data

    def get_followers(self, obj):
        return FollowersSerializer(obj.subscriber.all(), many=True).data

class CompanionSerializer(serializers.ModelSerializer):
    login = serializers.CharField()

    class Meta:
        model = User
        fields = ('login',)


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        required=True, write_only=True, validators=[validate_password]
    )
    password2 = serializers.CharField(
        required=True, write_only=True
    )
    login = serializers.CharField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'login',
            'password',
            'password2'
        )

        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        if not UniqueValidator(attrs['email']):
            raise serializers.ValidationError(
                {
                    'email': 'This email is already taken'
                }
            )

        if not UniqueValidator(attrs['login']):
            raise serializers.ValidationError(
                {
                    'login': 'This login is already taken'
                }
            )

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {
                    'password': 'Passwords do not match'
                }
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            login=validated_data['login']
        )
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        data['token'] = data.pop('access')
        data['refreshToken'] = data.pop('refresh')

        data.update({'user': RegisterSerializer(self.user).data})
        return data
