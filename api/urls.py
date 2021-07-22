#　ここではviews.pyで作ったビューとURLを紐付けテイク。
from django.urls import path, include
from rest_framework import routers

# template ここに登録することで、パス名とviewsを連携できる
router = routers.DefaultRouter()

urlpatterns = [
    # 下記を書くことで、ルートに来たときに、includeでrouterに登録している内容を参照してくれるようになる
    path('', include(router.urls)),
]