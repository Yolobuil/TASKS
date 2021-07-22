"""jira_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# urlpatternsのpathでURLを指定することで、ローカルでそのサイトに飛べるようになる
# アプリケーション（api）が複数個できた場合、アプリケーションごとに、urls.pyを作り、親のルートと紐付ける構成をとる
urlpatterns = [
    # /admin/とURLに打つと、Djangoのデフォルトのadminのサイトに飛ぶ
    path('admin/', admin.site.urls),
    # /api/と打った場合に、apiアプリの中にあるurls参照するようになる
    path('api/', include('api.urls')),
    # /authen/と打ったときにdjoserを使ってjwtの認証関係のサイトに飛ぶように設定されている
    path('authen/', include('djoser.urls.jwt')),
]

# settings.pyd作った/media/というパスとメディアフォルダの場所を紐付けている。
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
