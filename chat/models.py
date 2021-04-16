from django.db import models
from .managers import ThreadManager
# Create your models here.
class Thread(models.Model):
    THREAD_TYPE=(
        ('personal','Personal'),
        ('group','Group')
    )
    name=models.CharField(max_length=50,null=True,blank=True)
    thread_type=models.CharField(max_length=15,choices=THREAD_TYPE,default='group')
    users=models.ManyToManyField('auth.User')

    objects=ThreadManager()