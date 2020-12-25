from django.db import models
#accountsアプリに作成したCustomUserモデルをインポート
from accounts.models import CustomUser


# Create your models here.
class Diary(models.Model):
    """日記モデル"""
    
    user = models.ForeignKey(CustomUser, verbose_name = 'ユーザー', on_delete = models.PROTECT)
    title = models.CharField(verbose_name = 'タイトル', max_length=40)
    #blank=Trueの場合、フィールドがブランク（空）になることを許す
    #null=Trueの場合、データーベース内にNULLとして空の値を保持する
    content = models.TextField(verbose_name = '本文', blank=True, null=True)
    photo1 = models.ImageField(verbose_name = '写真1', blank=True, null=True)
    photo2 = models.ImageField(verbose_name = '写真2', blank=True, null=True)
    photo3 = models.ImageField(verbose_name = '写真3', blank=True, null=True)
    
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)
    
    #データをわかりやすく説明するクラス（Meta）=>管理画面のでのモデル名やモデルインスタンスの整列順など「フィールドに関係ない情報」を記述
    class Meta:
        #verbose_nameの場合 => 語尾に[s]がついてしまうので[plural]で複数形にする
        verbose_name_plural = 'Diary'
    
    #admin上でのデータの表示
    def __str__(self):
        return self.title

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