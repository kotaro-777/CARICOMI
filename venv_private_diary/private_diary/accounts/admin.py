from django.contrib import admin

#models.pyのCustomUserモデルをインポート
from .models import CustomUser
# Register your models here.

#CustomUserモデルをadmin（管理サイト上）で編集できるようにする　register = 登録
admin.site.register(CustomUser)