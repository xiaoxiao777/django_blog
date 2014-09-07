# -*- coding:utf-8 -*-  
from django.contrib.auth import authenticate, login as user_login, logout as user_logout   
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from models import Tag,MainCat,DetailCat,Article,Upimg,Comment,Album,Photos,Photo_Comment
from django.http import HttpResponse
import random, calendar,datetime
from django.db.models import Count
from django import forms
from django.contrib.auth.decorators import login_required
from captcha.fields import CaptchaField


class commentss(forms.Form):
    captcha=CaptchaField()


class UserForm(forms.Form):
    photo_name= forms.CharField()
    albumid= forms.CharField()
    headImg = forms.FileField()


def getthree():
    nart=Article.objects.all().order_by('-createtime')[:5]
    art=Comment.objects.values("article").annotate(Count('article')).order_by('-article__count')[:5]
    cart=[]
    for c in art:
        cart.append(Article.objects.get(id=c['article']))
    rart=Article.objects.all() if Article.objects.count() <5 else random.sample(Article.objects.all(),5)

    cm=Comment.objects.order_by('-time')[:5]
    tg=Tag.objects.all()[:100]
    #nart 最近5篇文章，cart随机5篇文章，
    return nart,cart,rart,cm,tg
def base(request,articles):
    maincat=MainCat.objects.all()
    
    nart,cart,rart,cm,tg=getthree()
    #日历
    today=datetime.datetime.now()
    s=calendar.HTMLCalendar(6)
    cals=list(s.itermonthdays2(today.year,today.month))
    tdarts=Article.objects.values('id','createtime').filter(createtime__year=today.year,createtime__month=today.month).order_by('createtime') #列表字典[{'createtime': datetime.datetime(2014, 4, 6, 4, 36, 32, 896000, tzinfo=<UTC>)},
    tdart=set([i['createtime'].day for i in tdarts])

    tmpq=Article.objects.exclude(createtime__year=today.year,createtime__month=today.month)
    premon=tmpq.filter(createtime__lt=today).order_by('-createtime')[:1]
    aftmon=tmpq.filter(createtime__gt=today).order_by('createtime')[:1]
    #cals=s.formatmonth(today.year,today.month)
    tt=[]
    for i in cals:
        tt.append(list(i))
    ttt=[]   
    for a in tt:
        for i in tdart:
            if a[0] == i:
                a.append(1)
        if len(a)==2:
            a.append(0)    
        ttt.append(a)
    return render_to_response('home.htm',locals(),context_instance=RequestContext(request))
def home(request):
    print 'home'
    articles=Article.objects.all().order_by('-createtime')[:10]
    return base(request,articles)
def getarticle(request,artid=1):
    maincat=MainCat.objects.all()
    article=Article.objects.get(id=artid)
    #article.readcount=article.readcount+1
    #article.save()
    #article.update(readcount=article.readcount+1)
    Article.objects.filter(id=artid).update(readcount=article.readcount+1)
    articleurl=request.META['HTTP_HOST']+request.path
    #前一篇文章与后一篇文章
    try:
        preart=Article.objects.get(id=int(artid)-1)
    except Exception:
        preart=None
    try:
        aftart=Article.objects.get(id=int(artid)+1)
    except Exception:
        aftart=None
    #感兴趣的文章,具有相同的tag
    intreart=[]
    for t in article.tag.all():
        intreart+=t.article_set.exclude(id=article.id)
    intreart=list(set(intreart))
    #得到comments
    comment =Comment.objects.filter(article=article)
    
    nart,cart,rart,cm,tg=getthree()
    #日历
    today=datetime.datetime.now()
    s=calendar.HTMLCalendar(6)
    cals=list(s.itermonthdays2(today.year,today.month))
    tdarts=Article.objects.values('id','createtime').filter(createtime__year=today.year,createtime__month=today.month).order_by('createtime') #列表字典[{'createtime': datetime.datetime(2014, 4, 6, 4, 36, 32, 896000, tzinfo=<UTC>)},
    tdart=set([i['createtime'].day for i in tdarts])

    tmpq=Article.objects.exclude(createtime__year=today.year,createtime__month=today.month)
    premon=tmpq.filter(createtime__lt=today).order_by('-createtime')[:1]
    aftmon=tmpq.filter(createtime__gt=today).order_by('createtime')[:1]
    tt=[]
    for i in cals:
        tt.append(list(i))
    ttt=[]   
    for a in tt:
        for i in tdart:
            if a[0] == i:
                a.append(1)
        if len(a)==2:
            a.append(0)    
        ttt.append(a)
    form=commentss()
    return render_to_response('detail.htm',locals(),context_instance=RequestContext(request))






def listdate(request,year,month,day=0):
    if day==0:
        articles=Article.objects.filter(createtime__year=year,createtime__month=month)
    else:
        articles=Article.objects.filter(createtime__year=year,createtime__month=month,createtime__day=day)
    maincat=MainCat.objects.all()
    nart,cart,rart,cm,tg=getthree()
    #日历
    today=datetime.datetime(year=int(year),month=int(month),day=int(day) if day else 1)
    s=calendar.HTMLCalendar(6)
    cals=list(s.itermonthdays2(today.year,today.month))
    tdarts=Article.objects.values('id','createtime').filter(createtime__year=today.year,createtime__month=today.month).order_by('createtime') #列表字典[{'createtime': datetime.datetime(2014, 4, 6, 4, 36, 32, 896000, tzinfo=<UTC>)},
    tdart=set([i['createtime'].day for i in tdarts])

    tmpq=Article.objects.exclude(createtime__year=today.year,createtime__month=today.month)
    premon=tmpq.filter(createtime__lt=today).order_by('-createtime')[:1]
    aftmon=tmpq.filter(createtime__gt=today).order_by('createtime')[:1]
    tt=[]
    for i in cals:
        tt.append(list(i))
    ttt=[]   
    for a in tt:
        for i in tdart:
            if a[0] == i:
                a.append(1)
        if len(a)==2:
            a.append(0)    
        ttt.append(a)
    return render_to_response('home.htm',locals(),context_instance=RequestContext(request))
def makecomment(request,aid):
    print '111'
    if request.method == "POST":
        form = commentss(request.POST)
        print '112'
        if form.is_valid():
            print '113'
            un=request.POST.get('author')
            em=request.POST.get('email')
            cm=request.POST.get('comment')
            at=Article.objects.get(id=aid)
            Comment(username=un,email=em,comment=cm,article=at).save()
            return redirect('/article/'+aid+'/')
        else:
            return redirect('/article/'+aid+'/')

    else:
        return redirect('/article/'+aid+'/')



@csrf_exempt
def comment_photo(request,id):
    un=request.POST.get('author')
    em=request.POST.get('email')
    cm=request.POST.get('comment')
    at=Photos.objects.get(id=id)
    Photo_Comment(username=un,email=em,comment=cm,photo=at).save()
    return redirect('/det_photo/?id='+id)



def photo(request):
    maincat=MainCat.objects.all()
    nart,cart,rart,cm,tg=getthree()
    #日历
    today=datetime.datetime.now()
    s=calendar.HTMLCalendar(6)
    cals=list(s.itermonthdays2(today.year,today.month))
    tdarts=Article.objects.values('id','createtime').filter(createtime__year=today.year,createtime__month=today.month).order_by('createtime') #列表字典[{'createtime': datetime.datetime(2014, 4, 6, 4, 36, 32, 896000, tzinfo=<UTC>)},
    tdart=set([i['createtime'].day for i in tdarts])

    tmpq=Article.objects.exclude(createtime__year=today.year,createtime__month=today.month)
    premon=tmpq.filter(createtime__lt=today).order_by('-createtime')[:1]
    aftmon=tmpq.filter(createtime__gt=today).order_by('createtime')[:1]
    albums=Album.objects.all()
    tt=[]
    for i in cals:
        tt.append(list(i))
    ttt=[]   
    for a in tt:
        for i in tdart:
            if a[0] == i:
                a.append(1)
        if len(a)==2:
            a.append(0)    
        ttt.append(a)
    #return render_to_response("album_list.html",locals())
    return render_to_response('album_list.html',locals(),context_instance=RequestContext(request))




def photo_list(request):
    maincat=MainCat.objects.all()
    nart,cart,rart,cm,tg=getthree()
    #日历
    today=today=datetime.datetime.now()
    s=calendar.HTMLCalendar(6)
    cals=list(s.itermonthdays2(today.year,today.month))
    tdarts=Article.objects.values('id','createtime').filter(createtime__year=today.year,createtime__month=today.month).order_by('createtime') #列表字典[{'createtime': datetime.datetime(2014, 4, 6, 4, 36, 32, 896000, tzinfo=<UTC>)},
    tdart=set([i['createtime'].day for i in tdarts])

    tmpq=Article.objects.exclude(createtime__year=today.year,createtime__month=today.month)
    premon=tmpq.filter(createtime__lt=today).order_by('-createtime')[:1]
    aftmon=tmpq.filter(createtime__gt=today).order_by('createtime')[:1]
    albumid=request.GET.get('id','')
    photos=Photos.objects.filter(albumname=albumid)
    tt=[]
    for i in cals:
        tt.append(list(i))
    ttt=[]   
    for a in tt:
        for i in tdart:
            if a[0] == i:
                a.append(1)
        if len(a)==2:
            a.append(0)    
        ttt.append(a)
    if photos == []:
        return redirect('/')
    else:
        print photos
        return render_to_response("demo.html",locals())

@csrf_exempt
def det_photo(request):
    id=request.GET.get('id','')
    photo=Photos.objects.get(pk=id)
    photo=Photos.objects.get(pk=id)
    comment_photo =Photo_Comment.objects.filter(photo=id)
    try:
        preart=Photos.objects.get(id=int(id)-1)
    except Exception:
        preart=None
    try:
        aftart=Photos.objects.get(id=int(id)+1)
    except Exception:
        aftart=None
    return render_to_response('det_photo.html',locals(),context_instance=RequestContext(request))


    
@login_required
def uploadfile(request):
    if not request.user.is_authenticated():
        return  redirect('/')
    if request.method == "POST":
        uf = UserForm(request.POST, request.FILES)
        if uf.is_valid():
            print uf.cleaned_data
            photo_name= uf.cleaned_data['photo_name']
            albumid= uf.cleaned_data['albumid']
            headImg= uf.cleaned_data['headImg']
            photo = Photos()
            photo.photo_name = photo_name
            al = Album.objects.get(pk=albumid)
            photo.albumname = al
            photo.headimg = headImg
            photo.save()
            return redirect('/uploadfile/')
    else:
        uf = UserForm()
    maincat=MainCat.objects.all()
    nart,cart,rart,cm,tg=getthree()
    #日历
    today=today=datetime.datetime.now()
    s=calendar.HTMLCalendar(6)
    cals=list(s.itermonthdays2(today.year,today.month))
    tdarts=Article.objects.values('id','createtime').filter(createtime__year=today.year,createtime__month=today.month).order_by('createtime') #列表字典[{'createtime': datetime.datetime(2014, 4, 6, 4, 36, 32, 896000, tzinfo=<UTC>)},
    tdart=set([i['createtime'].day for i in tdarts])

    tmpq=Article.objects.exclude(createtime__year=today.year,createtime__month=today.month)
    premon=tmpq.filter(createtime__lt=today).order_by('-createtime')[:1]
    aftmon=tmpq.filter(createtime__gt=today).order_by('createtime')[:1]
    tt=[]
    for i in cals:
        tt.append(list(i))
    ttt=[]   
    for a in tt:
        for i in tdart:
            if a[0] == i:
                a.append(1)
        if len(a)==2:
            a.append(0)    
        ttt.append(a)
    return render_to_response('uploadfile.html',locals(),context_instance=RequestContext(request))


def create_album(request):
    if not request.user.is_authenticated():
        return  redirect('/')
    if request.method=='GET':
        albums=Album.objects.all()
        print albums      
        maincat=MainCat.objects.all()
        nart,cart,rart,cm,tg=getthree()
        #日历
        today=today=datetime.datetime.now()
        s=calendar.HTMLCalendar(6)
        cals=list(s.itermonthdays2(today.year,today.month))
        tdarts=Article.objects.values('id','createtime').filter(createtime__year=today.year,createtime__month=today.month).order_by('createtime') #列表字典[{'createtime': datetime.datetime(2014, 4, 6, 4, 36, 32, 896000, tzinfo=<UTC>)},
        tdart=set([i['createtime'].day for i in tdarts])

        tmpq=Article.objects.exclude(createtime__year=today.year,createtime__month=today.month)
        premon=tmpq.filter(createtime__lt=today).order_by('-createtime')[:1]
        aftmon=tmpq.filter(createtime__gt=today).order_by('createtime')[:1]
           
        tt=[]
        for i in cals:
            tt.append(list(i))
        ttt=[]   
        for a in tt:
            for i in tdart:
                if a[0] == i:
                    a.append(1)
            if len(a)==2:
                a.append(0)    
            ttt.append(a)
        return render_to_response('create_album.html',locals(),context_instance=RequestContext(request))
    else:
        albumpath=request.POST['albumpath']
        albumname=request.POST['albumname']
        a=Album(album_name=albumname,album_path=albumpath)
        a.save()
        maincat=MainCat.objects.all()
        nart,cart,rart,cm,tg=getthree()
        #日历
        today=today=datetime.datetime.now()
        s=calendar.HTMLCalendar(6)
        cals=list(s.itermonthdays2(today.year,today.month))
        tdarts=Article.objects.values('id','createtime').filter(createtime__year=today.year,createtime__month=today.month).order_by('createtime') #列表字典[{'createtime': datetime.datetime(2014, 4, 6, 4, 36, 32, 896000, tzinfo=<UTC>)},
        tdart=set([i['createtime'].day for i in tdarts])

        tmpq=Article.objects.exclude(createtime__year=today.year,createtime__month=today.month)
        premon=tmpq.filter(createtime__lt=today).order_by('-createtime')[:1]
        aftmon=tmpq.filter(createtime__gt=today).order_by('createtime')[:1]
        tt=[]
        for i in cals:
            tt.append(list(i))
        ttt=[]   
        for a in tt:
            for i in tdart:
                if a[0] == i:
                    a.append(1)
            if len(a)==2:
                a.append(0)    
            ttt.append(a)
        return render_to_response('create_album.html',locals(),context_instance=RequestContext(request))



def editarticle(request,aid):
    article=Article.objects.get(id=aid)
    maincat=MainCat.objects.all()
    nart,cart,rart,cm,tg=getthree()
    if request.method=='POST':
        title=request.POST['title']
        tags=request.POST['tag']
        cat=request.POST['cat']
        content=request.POST['content']
        tags=tags.split(',')
        tagm=[]
        
        for i in tags:
            a=Tag.objects.filter(tag=i)
            if a:
                tagm.append(a[0])
            else:
                t=Tag(tag=i)
                t.save()
                tagm.append(t)
        article.user=request.user
        article.title=title
        article.content=content
        if cat.find('mc')>0:
            maincat=MainCat.objects.get(id=cat[:cat.find('m')])
            article.maincat=maincat
        elif cat.find('-')==-1:
            dcat=DetailCat.objects.get(id=cat)
            article.maincat=dcat.maincat
            article.detailcat=dcat
        else:
            pass
        article.save()
        article.tag=tagm
        article.save()
        return redirect(getarticle,article.id)
    
    #日历
    today=today=datetime.datetime.now()
    s=calendar.HTMLCalendar(6)
    cals=list(s.itermonthdays2(today.year,today.month))
    tdarts=Article.objects.values('id','createtime').filter(createtime__year=today.year,createtime__month=today.month).order_by('createtime') #列表字典[{'createtime': datetime.datetime(2014, 4, 6, 4, 36, 32, 896000, tzinfo=<UTC>)},
    tdart=set([i['createtime'].day for i in tdarts])

    tmpq=Article.objects.exclude(createtime__year=today.year,createtime__month=today.month)
    premon=tmpq.filter(createtime__lt=today).order_by('-createtime')[:1]
    aftmon=tmpq.filter(createtime__gt=today).order_by('createtime')[:1]
    
    tt=[]
    for i in cals:
        tt.append(list(i))
    ttt=[]   
    for a in tt:
        for i in tdart:
            if a[0] == i:
                a.append(1)
        if len(a)==2:
            a.append(0)    
        ttt.append(a)
    return render_to_response('new.htm',locals(),context_instance=RequestContext(request))
def newarticle(request):
    if not request.user.is_authenticated():
        return  redirect('/Login/?next=%s' % request.path)
    if request.method=='POST':
        title=request.POST['title']
        tags=request.POST['tag']
        cat=request.POST['cat']
        content=request.POST['content']
        tags=tags.split(',')
        tagm=[]
        print tags
        for i in tags:
            a=Tag.objects.filter(tag=i)
            if a:
                tagm.append(a[0])
            else:
                t=Tag(tag=i)
                t.save()
                tagm.append(t)
        if cat.find('mc')>0:
            maincat=MainCat.objects.get(id=cat[:cat.find('m')])
            ar=Article(user=request.user,title=title,content=content,maincat=maincat)
        elif cat.find('-')==-1:
            dcat=DetailCat.objects.get(id=cat)
            maincat=dcat.maincat
            ar=Article(user=request.user,title=title,content=content,detailcat=dcat,maincat=maincat)
        else:
            ar=Article(user=request.user,title=title,content=content)
        ar.save()
        ar.tag=tagm
        ar.save()
        return redirect(getarticle,ar.id)
    
   
    maincat=MainCat.objects.all()
    nart,cart,rart,cm,tg=getthree()
    #日历
    today=today=datetime.datetime.now()
    s=calendar.HTMLCalendar(6)
    cals=list(s.itermonthdays2(today.year,today.month))
    tdarts=Article.objects.values('id','createtime').filter(createtime__year=today.year,createtime__month=today.month).order_by('createtime') #列表字典[{'createtime': datetime.datetime(2014, 4, 6, 4, 36, 32, 896000, tzinfo=<UTC>)},
    tdart=set([i['createtime'].day for i in tdarts])

    tmpq=Article.objects.exclude(createtime__year=today.year,createtime__month=today.month)
    premon=tmpq.filter(createtime__lt=today).order_by('-createtime')[:1]
    aftmon=tmpq.filter(createtime__gt=today).order_by('createtime')[:1]
    tt=[]
    for i in cals:
        tt.append(list(i))
    ttt=[]   
    for a in tt:
        for i in tdart:
            if a[0] == i:
                a.append(1)
        if len(a)==2:
            a.append(0)    
        ttt.append(a)
    return render_to_response('new.htm',locals(),context_instance=RequestContext(request))
def listcat(request):
    #该函数用来对大类，小类 标签，maincat,decat,tag
    tp=request.GET.get('type','')
    tid=request.GET.get('id','')
    if tp=='maincat': 
        maincat=MainCat.objects.get(id=tid)
        articles=maincat.article_set.all()
    elif tp=='decat':
        decat=DetailCat.objects.get(id=tid)
        articles=decat.article_set.all()
        
    elif tp=='tag':
        tag=Tag.objects.get(id=tid)
        articles=tag.article_set.all()
    else:
        pass
    #maincat=MainCat.objects.all()
    #return render_to_response('home.htm',locals(),context_instance=RequestContext(request))
    return base(request,articles)
    
    
@csrf_exempt
def uploadjson(request):
    if request.method=='POST':
        #print request.POST
        #print request.FILES['imgFile']
        imgurl='/static/a.png'
        img=Upimg(img=request.FILES['imgFile'])
        img.save()
        imgurl=img.img.url
        st=str('{"error" : 0,"url" : "'+imgurl+'"}')
        return HttpResponse (st,mimetype='application/json')
    return HttpResponse (str('''{
        "error" : 1,
        "message" : "somesorng"
}        '''),mimetype='application/json')

def getuploadimg(request,name='0'):
    
    f=Upimg.objects.get(name=name)
    if not f:
        return HttpResponse('Wrong')
    return HttpResponse(f.img.read(),mimetype='image/png')    
    
    
def addcat(request):
    if not request.user.is_authenticated():
        return  redirect('/')
    if request.method=='POST':
        if request.POST.get('maincatid'):
            mai=MainCat.objects.get(id=request.POST.get('maincatid'))
            cat=request.POST['cat']
            DetailCat(cat=cat,maincat=mai).save()
        else:
            MainCat(cat=request.POST['cat']).save()
    return  redirect('/')
    
def Login(request):   
    #表单提交过来的数据
    if request.user.is_authenticated():
        return  redirect('/')
    if request.method == 'POST':   
        username = request.POST['username']   
        password = request.POST['password']   
        user = authenticate(username=username, password=password)   
        if user is not None:   
            if user.is_active:   
                        user_login(request, user)
                        if request.GET.has_key('next'):
                            return redirect(request.GET['next'] )  
                        else:
                            return redirect('/' )  
            else:   
                    return HttpResponse('用户没有启用!')   
        else:   
                return HttpResponse('用户名或者密码错误！')   
    else:
        form = LoginForm()
        ct=RequestContext(request,{'form':form})
        return render_to_response('account/login.html',context_instance=ct)   
def Logout(request):   
    user_logout(request)   
    return  redirect('/')


def search(request):    
    s=request.GET.get('s','')
    try:
        articles=Article.objects.filter(content__contains=s)
    except Exception:
        articles=None
    print articles   
    if articles is not None:
        return base(request,articles)
    else:
        return  redirect('/')
