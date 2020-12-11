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
        
    def __str__(self):
        return self.title
    