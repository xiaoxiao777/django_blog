from django.db import models
from django.contrib.auth.models import User
import datetime

class Tag(models.Model):
    tag=models.CharField(max_length=30)
    def __unicode__(self):
        return self.tag
class MainCat(models.Model):
    cat=models.CharField(max_length=30)
    def __unicode__(self):
        return self.cat

class DetailCat(models.Model):
    cat=models.CharField(max_length=30)
    maincat=models.ForeignKey(MainCat)
    def __unicode__(self):
        return self.cat
class Album(models.Model):
    album_name=models.CharField(max_length=30)
    album_path=models.CharField(max_length=30)
    def __unicode__(self):
        return self.album_name

class Photos(models.Model):
    photo_name=models.CharField(max_length=30)
    albumname=models.ForeignKey(Album)
    headimg=models.FileField(upload_to='photo/')
    def __unicode__(self):
        return self.photo_name



class Photo_Comment(models.Model):
    username=models.CharField(max_length=100)
    email=models.EmailField()
    comment=models.CharField(max_length=200)
    photo=models.ForeignKey(Photos)
    time=models.DateTimeField(auto_now=True)


        
class Article(models.Model):
    user=models.ForeignKey(User)
    title=models.CharField(max_length=100)
    maincat=models.ForeignKey(MainCat,null=True)
    detailcat=models.ForeignKey(DetailCat,null=True)
    tag=models.ManyToManyField(Tag,null=True)  
    createtime=models.DateTimeField(default=datetime.datetime.now) #str(datetime.utcnow()) "YYYY-MM-DD HH:MM[:ss[.uuuuuu]]
    #createtime=models.DateTimeField(auto_now_add=True) #str(datetime.utcnow()) "YYYY-MM-DD HH:MM[:ss[.uuuuuu]]
    #createtime=models.DateTimeField(auto_now=True) #str(datetime.utcnow()) "YYYY-MM-DD HH:MM[:ss[.uuuuuu]]
    readcount=models.IntegerField(default=0)
    content=models.CharField(max_length=20000)
    def __unicode__(self):
        return self.title
class Comment(models.Model):
    username=models.CharField(max_length=100)
    email=models.EmailField()
    comment=models.CharField(max_length=500)
    article=models.ForeignKey(Article)
    time=models.DateTimeField(auto_now=True)
class Upimg(models.Model):
    img=models.ImageField(upload_to='blogimg')
