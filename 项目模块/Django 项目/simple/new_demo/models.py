from django.db import models

# Create your models here.

class BaceManber(models.Model):
    name = models.CharField(verbose_name='名字', max_length=20)
    year = models.CharField(verbose_name='年份', max_length=20)
    work = models.CharField(verbose_name='工作', max_length=20)
    place = models.CharField(verbose_name='地址', max_length=20)

    def __str__(self):
        return self.name