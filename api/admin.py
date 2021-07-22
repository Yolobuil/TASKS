#   ここにみたいモデルを登録していく（models.pyからimportする）
# /admin で登録したモデルをダッシュボード上で操作できる

from django.contrib import admin
from .models import Profile, Task, Category

# Register your models here.
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Task)
