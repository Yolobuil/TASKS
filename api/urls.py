#　ここではviews.pyで作ったビューとURLを紐付けテイク。
from django.urls import path, include
from rest_framework import routers
from.views import CategoryViewSet, CreateUserView, ListUserView, LoginUserView, ProfileViewSet, TaskViewSet

# template ここに登録することで、パス名とviewsを連携できる
# views内でModelViewSetを引数にとっている場合はRouterにviewを登録する
router = routers.DefaultRouter()
router.register('category', CategoryViewSet)
router.register('tasks', TaskViewSet)
router.register('profile', ProfileViewSet)


# views内でgenericsを引数にとっている場合はurlpatternsのpathにviewを登録する
urlpatterns = [
    # 下記を書くことで、ルートに来たときに、includeでrouterに登録している内容を参照してくれるようになる
    path('', include(router.urls)),
    # as_view()をつける必要がある
    path('create/', CreateUserView.as_view(), name="create"),
    path('users/', ListUserView.as_view(), name='users'),
    path('loginuser', LoginUserView.as_view(), name='loginuser')
]