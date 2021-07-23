from django.shortcuts import render
from rest_framework import status, permissions, generics, viewsets

from . import custompermissions
from .serializers import UserSerializer, CategorySerializer, TaskSerializer, ProfileSerializer
from rest_framework.response import Response
from .models import Task, Category, Profile
from django.contrib.auth.models import User


# Create your views here.
# djangoのRESTフレームワークのビューには、generics（特定のメソッドに特化）から始まるものとmodelviewset（CRUDを全て提供）というものがある
# ユーザ作成のためのビュー（ユーザー作成に特化しているため、CreateAPIViewを使っている）
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    # 新規ユーザ作成の時はJWTを通さず、誰でもアクセスできるようにするパーミッションに変える
    permission_classes = (permissions.AllowAny,)


# UserのListを取得するビュー
class ListUserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Retrieveは特定のオブジェクトを検索して返してきてくれる
class LoginUserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        # request.userはログインユーザを指す
        return self.request.user


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    # CRUDのCに当たるメソッド
    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user)

    # 使わないメソッドの無効化
    def destroy(self, request, *args, **kwargs):
        response = {'message': 'DELETE method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        response = {'message': 'PATCH method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.obujects.all()
    serializer_class = CategorySerializer

    # 使わないメソッドの無効化
    def destroy(self, request, *args, **kwargs):
        response = {'message': 'DELETE method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        response = {'message': 'PUT method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        response = {'message': 'PATCH method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated, custompermissions.OwnerPermission,)

    def perform_create(self, serializer):
        # ログインユーザを自動でオーナーに割あてる処理
        serializer.save(owner=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        response = {'message': 'PATCH method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
