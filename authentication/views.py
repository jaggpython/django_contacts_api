from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import UserSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib import auth
import jwt
from contactapi.settings import JWT_SECRET_KEY
from rest_framework.views import APIView

class RegisterView(GenericAPIView):
    serializer_class = UserSerializer
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self,request):
        data=request.data
        username = data.get("username","")
        password = data.get("password", "")
        user = auth.authenticate(username=username,password=password)

        if user:
            auth_token = jwt.encode({"username": user.username}, str(JWT_SECRET_KEY))
            serializer = UserSerializer(user)

            data ={"user":serializer.data,"token": auth_token}
            return Response(data,status=status.HTTP_200_OK)

            #SEND RES
        return Response({"detail":"Invalid Credentials"},status=status.HTTP_401_UNAUTHORIZED)



class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message':'success'
        }
        return response