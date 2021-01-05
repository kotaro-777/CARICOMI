from django.db import models
#accountsアプリに作成したCustomUserをインポート
from accounts.models import CustomUser


# Create your models here.

#口コミモデル
class Reviews(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name="ユーザー", on_delete=models.PROTECT)
    service_name = models.CharField(verbose_name="サービス名", max_length=20)
    SERVICE_QUALITY_CHOICES = [
        # (データベースに登録されている値, 表示上の値) ※表示上の値はget_field名_displayで取得
        ('5', '★★★★★'),
        ('4', '★★★★'),
        ('3', '★★★'),
        ('2', '★★'),
        ('1', '★')
    ]
    support_quality = models.CharField(verbose_name="サポートの質", choices=SERVICE_QUALITY_CHOICES, max_length=5)
    subject = models.TextField(verbose_name="サービスの感想")
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    update_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Reviews'
    
    def __str__(self):
        return self.service_name
