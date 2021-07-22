from rest_framework import serializers
from .models import Task, Category, Profile
from django.contrib.auth.models import User


# serializersというのは、モデルに対して１つ１つ作っていくもの。

# UserSerializer
class UserSerializer(serializers.ModelSerializer):
    # Metaにモデルとしてどのモデルを使うのか、フィールズに取り扱いたい属性、extra_kwargsで特定のパラメータに対して、さらにオプションをつけられる
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        # passwordに対して読み取り不可のwrite＿only　passwordの設定が必須であるというrequired
        extra_kwargs = {'password': {'write_only': True, 'required': True}}
        # passwordをハッシュ化してDBに登録するためにcreateメソッドを使用

    def create(self, validated_data):
        # ハッシュ化したパスワードをユーザーの属性に渡している
        user = User.objects.create_user(**validated_data)
        return user


# ProfileSerializer
class ProfileSerializer(serializers.ModelSerializer):
    # Metaにモデルとしてどのモデルを使うのか、フィールズに取り扱いたい属性、extra_kwargsで特定のパラメータに対して、さらにオプションをつけられる
    class Meta:
        model = Profile
        fields = ['id', 'user_profile', 'img']
        # readonlyである理由は、フロントエンドで新規でユーザを作った際にプロフィールを同時に作る。（djangoで自動で行うため）
        extra_kwargs = {'user_profile': {'read_only': True}}


# CategorySerializer
class CategorySerializer(serializers.ModelSerializer):
    # Metaにモデルとしてどのモデルを使うのか、フィールズに取り扱いたい属性、extra_kwargsで特定のパラメータに対して、さらにオプションをつけられる
    class Meta:
        model = Category
        fields = ['id', 'item']


# TaskSerializer
class TaskSerializer(serializers.ModelSerializer):
    # 　変換している全ての変数はread_onlyであるため、getを使っている時のみ返す。
    # foreignkeyを使っているを使って参照しているのは、番号が帰ってくる。そのため、直接名前がみたい場合は、下記のようにReadOnlyFieldを使って変数に入れる
    category_item = serializers.ReadOnlyField(source='category.item', read_only=True)
    owner_username = serializers.ReadOnlyField(source='owner.username', read_only=True)
    responsible_username = serializers.ReadOnlyField(source='responsible.username', read_only=True)

    # CharFieldを使っているstatusにもデフォルトで入ってくるのは１、２、３という数字get_変数名_displayを使うと名前が表示できる
    status_name = serializers.CharField(source='get_status_display', read_only=True)

    # 日付のフォーマット変換 DateTimeFieldを使って引数でformat使えばOK
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)

    # Metaにモデルとしてどのモデルを使うのか、フィールズに取り扱いたい属性、extra_kwargsで特定のパラメータに対して、さらにオプションをつけられる
    class Meta:
        model = Task
        fields = ['id', 'task', 'description', 'criteria', 'status', 'status_name', 'category', 'category_item',
                  'estimate', 'responsible', 'responsible_username', 'owner', 'owner_username', 'created_at',
                  "updated_at", ]
        # フロントエンドで新しくタスクを作るとき、オーナーがログインユーザに自動で割り当てられるようにに実装するため。
        extra_kwargs = {'owner': {'read_only': True}}
