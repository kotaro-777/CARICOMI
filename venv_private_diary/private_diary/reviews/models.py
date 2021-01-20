from django.db import models
# accountsアプリに作成したCustomUserをインポート
from accounts.models import CustomUser


# Create your models here.

# Service
class Service(models.Model):
    service = models.CharField(verbose_name="サービス名", max_length=25, default=1)
    url = models.URLField(verbose_name="URL")
    img = models.ImageField(verbose_name="画像")

    class Meta:
        verbose_name_plural = 'Service'

    def __str__(self):
        return self.service

# 口コミモデル


class Review(models.Model):
    user = models.ForeignKey(
        CustomUser, verbose_name="ユーザー", on_delete=models.PROTECT)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    SERVICE_QUALITY_CHOICES = [
        # (データベースに登録されている値, 表示上の値) ※表示上の値はget_フィールド名_displayで取得
        ('5', '★★★★★'),
        ('4', '★★★★'),
        ('3', '★★★'),
        ('2', '★★'),
        ('1', '★')
    ]
    quality = models.CharField(
        verbose_name="サポートの質", choices=SERVICE_QUALITY_CHOICES, max_length=5)
    content = models.TextField(verbose_name="サービスの感想")
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    class Meta:
        verbose_name_plural = 'Review'

    def __str__(self):
        return self.service
