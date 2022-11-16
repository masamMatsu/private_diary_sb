from accounts.models import CustomUser
from django.db import models


class Diary(models.Model):
    """日記モデル"""

    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)
    title = models.CharField(verbose_name='タイトル', max_length=40)
    content = models.TextField(verbose_name='本文', blank=True, null=True)
    photo1 = models.ImageField(verbose_name='写真1', blank=True, null=True)
    photo2 = models.ImageField(verbose_name='写真2', blank=True, null=True)
    photo3 = models.ImageField(verbose_name='写真3', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    class Meta:
        verbose_name_plural = 'Diary'

    def __str__(self):
        return self.title

class Sukashi(models.Model):
    """透かしモデル"""
    SELECTION = (
        (1,'1　どこにでもある'),
        (2,'2　ちょっと探せばある'),
        (3,'3　ちょっと探してもない'),
        (4,'4　かなり探すとある'),
        (5,'5　奇跡の出会い')
    )
    OSELECTION = (
        (1,'公開'),
        (2,'限定公開'),
        (3,'非公開')
    )


    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)
    stype = models.CharField(verbose_name='型', max_length=40)
    splace = models.CharField(verbose_name='採取地', max_length=40)
    rare = models.IntegerField(choices=SELECTION ,verbose_name='レア度')
    oflag = models.IntegerField(choices=OSELECTION ,verbose_name='公開フラグ',default=1)
    content = models.TextField(verbose_name='本文', blank=True, null=True)
    photo1 = models.ImageField(verbose_name='写真1', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    class Meta:
        verbose_name_plural = 'Sukashi'

    def __str__(self):
        return str(self.rare)+' '+str(self.user)+' '+self.content
