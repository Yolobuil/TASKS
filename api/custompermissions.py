from rest_framework import permissions

class OwnerPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODSとはgetメソッド、データの取得するだけで、変更がないため。Trueはパーミッションを許可する
        if request.method in permissions.SAFE_METHODS:
            return True
        # オーナーのユーザーIDとログインユーザのIDを比較して同じ時のみTrue
        return obj.owner.id == request.user.id