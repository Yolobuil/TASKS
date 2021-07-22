# DBの構造を定義する場所 ここでモデルのデータ構造を作る。
# ここで定義したモデルをDBの構造に落とし込む
from django.db import models
from django.contrib.auth.models import User
# マイナスの整数を受け付けないバリデーター
from django.core.validators import MinValueValidator
# 128bitの一意なIDを作ってくれるUUID (PK)
import uuid


# profileのインスタンスと画像の名前を引数にとり、ファイル名を.で分解し、末尾の名前を取得し変数に格納
# 　拡張子は.のうしろにあり、一番末尾であるため、extに拡張子名が入ってくる（pngなど）
# 　返り値として、mediaの中のavatarsというフォルダを作って、その中に、ユーザープロフィールのIDと拡張子をつけたファイルを作成。
def upload_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['avatars', str(instance.user_profile.id) + str(".") + str(ext)])


# Create your models here.
# purofileモデル Djangoのユーザモデルを紐づける OneToOneFieldでDjangoと紐付け。アバター画像を属性として持っている
# on_deleteにCASCADEのオプションをつけることで、ユーザモデルが削除された場合にプロフィールオブジェクトが自動削除
class Profile(models.Model):
    user_profile = models.OneToOneField(
        User, related_name='user_profile',
        on_delete=models.CASCADE
    )
    img = models.ImageField(blank=True, null=True, upload_to=upload_avatar_path)

    # ProfileモデルのStringの返り値としてPythonの特殊関数を使う。インスタンスが作られた際に、作られたインスタンスに対して、
    # print　fやStringへのキャストを実行した時にデフォルトで返してくれる文字列
    # user_profileで指定する、ユーザーモデルの中に、Djangoがデフォルトでユーザーネームやパスワードの情報を持っているため、その中からユーザーネームをとっている

    def __str__(self):
        return self.user_profile.username


# Category model
# タスクボードのカテゴリのこと。
# CharFieldを使ってアイテム属性を持たせる。最大文字列は１００文字
class Category(models.Model):
    # CharFieldを使ってアイテム属性を持たせる。最大文字列は１００文字
    item = models.CharField(max_length=100)


def __str__(self):
    return self.item


# Task model
class Task(models.Model):
    # statusの選択肢の要素
    STATUS = (
        ('1', 'Not standerd'),
        ('2', 'On going'),
        ('3', 'Done'),
    )

    # 通常は数字が連番でつくが、primary_key → プライマリーキー　editable　→編集可不可
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    task = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    criteria = models.CharField(max_length=100)
    # choice 決められた中から１つ選ぶことができる　
    status = models.CharField(max_length=40, choices=STATUS, default='1')
    # ForeignKeyで別モデルを参照できる。
    # CASCADEを指定することで、大元のカテゴリが削除された場合に、それに紐づくタスクも削除される
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # 最小値を０にしており、０以上の整数を受け取るように設定 数値はIntegerField
    estimate = models.IntegerField(validators=[MinValueValidator(0)])
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    responsible = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responsible')
    # 日時DateTimeField auto_now_add=をTrueにしておくことで、Taskが作成された際に、自動でその時の時間をDBに登録
    created_at = models.DateTimeField(auto_now_add=True)
    # addは不要。更新するたびにその時の日時を付与する
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task
