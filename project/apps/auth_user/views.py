from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_200_OK, HTTP_201_CREATED, HTTP_403_FORBIDDEN
from project.apps.lib.custom.custom_views import *
from .models import User
from .serializer import UserSerializer
import time



class UserLogin(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        time.sleep(2)
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if not serializer.is_valid():
            return Response({"status": HTTP_401_UNAUTHORIZED})
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user_details = (UserSerializer(user))
        return Response({
            "status": HTTP_200_OK,
            'token': token.key,
            'user': user_details.data
        })


class UserLogout(APIView):
    def post(self, request):
        time.sleep(2)
        user_id = request.data.get("user_id")
        token_object = Token.objects.filter(user=user_id)
        if token_object.exists():
            token_object.delete()
            return Response({"status": status.HTTP_200_OK, "message": "logged out"})
        else:
            return Response({"status": status.HTTP_403_FORBIDDEN, "message": "already logged out"})


class UserRegister(APIView):
    def post(self, request):
        name = request.data.get("name")
        email = request.data.get("email")
        phone = request.data.get("phone")
        gender = request.data.get("gender")
        username = request.data.get("username")
        password = request.data.get("password")
        passwordConfirm = request.data.get("passwordConfirm")
        address = request.data.get("address")
        country = request.data.get("country")
        bio = request.data.get("bio")

        if password != passwordConfirm:
            return Response({"status": HTTP_403_FORBIDDEN, "message": "passwords do not match"})

        check = User.objects.filter(username=username)
        if check.exists():
            return Response({"status": HTTP_403_FORBIDDEN, "message": "user already exists"})
        created = User.objects.create_user(username=username,
                                           email=email,
                                           password=password,
                                           first_name=name.split()[0],
                                           last_name=" ".join(name.split()[1:]),
                                           phone=phone,
                                           gender=gender,
                                           address=address,
                                           country=country,
                                           bio=bio,
                                           role="user")
        created.save()

        return Response({"status": HTTP_201_CREATED, "message": "user registration successful"})
