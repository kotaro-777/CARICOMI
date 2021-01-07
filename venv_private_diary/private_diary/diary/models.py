from django.db import models
#accountsアプリに作成したCustomUserモデルをインポート
from accounts.models import CustomUser

#就職日記モデル
class CareerDiary(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name="ユーザー", on_delete=models.PROTECT)
    company_name = models.CharField(verbose_name="企業名", max_length=25)
    interview_date = models.DateField(verbose_name="面接日")
    
    SELECTION_STAGE_CHOICES = [
        ('CASUAL', 'カジュアル面談'),
        ('1次面接', '1次面接'),
        ('2次面接', '2次面接'),
        ('3次面接', '3次面接'),
        ('4次面接', '4次面接'),
        ('5次面接', '5次面接'),
        ('最終選考', '最終選考')
    ]
    selection_stage = models.CharField(verbose_name="選考段階", choices=SELECTION_STAGE_CHOICES, max_length=7, blank=False, default=0)
    content = models.TextField(verbose_name="面接記録")
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    update_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)
    
    class Meta:
        verbose_name_plural = 'CareerDiary'
        
    def __str__(self):
        return self.company_name