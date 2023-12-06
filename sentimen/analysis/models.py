from django.db import models

class Tweet(models.Model):
    id_twt = models.AutoField(primary_key=True)
    full_text = models.TextField()
    username = models.CharField(max_length=255)
    idt = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'tweet'

class Clean(models.Model):
    id_twt = models.AutoField(primary_key=True)
    full_text = models.TextField()
    username = models.CharField(max_length=255)
    idt = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'clean'



