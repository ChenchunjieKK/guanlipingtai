from django.db import models

# Create your models here.
class Admin(models.Model):
    """ 管理员 """
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)

    def __str__(self):
        return self.username


class Check(models.Model):
    """账单"""
    time = models.DateTimeField(verbose_name="消费时间")
    money = models.CharField(verbose_name="金钱", max_length=16)
    uses = models.CharField(verbose_name="用途", max_length=255)