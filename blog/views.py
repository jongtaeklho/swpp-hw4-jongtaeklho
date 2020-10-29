from django.http import HttpResponse, HttpResponseNotAllowed,JsonResponse,HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from json import JSONDecodeError
from .models import Article,Comment
from django.core.exceptions import ObjectDoesNotExist


def signup(request):
    if request.method == 'POST':
        try:
            req_data = json.loads(request.body.decode())
            username = req_data['username']
            password = req_data['password']
        except (KeyError, JSONDecodeError) as e:
            return HttpResponseBadRequest()

        User.objects.create_user(username=username, password=password)
        return HttpResponse(status=201)
    else:
        return HttpResponseNotAllowed(['POST'])

def signin(request):
    if request.method=='POST':
        try:
            req_data=json.loads(request.body.decode())
            username=req_data['username']
            password=req_data['password']
        except (KeyError, JSONDecodeError) as e:
            return HttpResponseBadRequest()
        try:
            names=User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponse(status=401)
        if names.check_password(password):
            login(request,names)
            request.session['user_id']=names.id
            return HttpResponse(status=204)
        else: return HttpResponse(status=401)
    else :
        return HttpResponseNotAllowed(['POST'])

def signout(request):
    if request.method=='GET':
        if request.user.is_authenticated==True:
            logout(request)
            return HttpResponse(status=204)
        else :
            return HttpResponse(status=401)
    else :
        return HttpResponseNotAllowed(['GET'])
  
def article(request):
    if request.user.is_authenticated!=True:
        return HttpResponse(status=401)
    if request.method=='GET':
        article_list=[article for article in Article.objects.all().values()]
        return JsonResponse(article_list,safe=False)
    elif request.method=='POST':
        try:
            req_data=json.loads(request.body.decode())
            title=req_data['title']
            content=req_data['content']
            
        except (KeyError, JSONDecodeError) as e:
            return HttpResponseBadRequest()
       
        user=User.objects.get(id=request.session['user_id'])
        article=Article(title=title,content=content,author=user)
        article.save()
        return JsonResponse({'title':article.title,'content':article.content,'author':article.author.id}
            ,status=201)


    else:
        return HttpResponseNotAllowed(['GET','POST'])

def article_info(request,article_id):
    if request.user.is_authenticated!=True:
        return HttpResponse(status=401)
        
    
    article=Article.objects.get(id=article_id)
    if request.method=='GET':
        return JsonResponse({'id':article.id,'title':article.title,
        'content':article.content,'author_id':article.author.id})
    elif request.method=='PUT':
        if article.author.id!=request.session['user_id']:
            return HttpResponse(status=401)
        try:
            req_data=json.loads(request.body.decode())
            title=req_data['title']
            content=req_data['content']
        except (KeyError, JSONDecodeError) as e:
            return HttpResponseBadRequest()
        article.title=title
        article.content=content
        article.save()
        return JsonResponse({'id':article.id,'title':article.title,
        'content':article.content,'author_id':article.author.id},status=200)
    elif request.method=='DELETE':
        if article.author.id!=request.session['user_id']:
            return HttpResponse(status=401)
        article.delete()
        return HttpResponse(status=200)

    else:
        return HttpResponseNotAllowed(['GET','PUT','DELETE'])
def comment(request,article_id):
    if request.user.is_authenticated!=True:
        return HttpResponse(status=401)
    article=Article.objects.get(id=article_id)
    if request.method=='GET':
        comment_list=[comment for comment in Comment.objects.filter(article_id=article_id).values()]
        return JsonResponse(comment_list,safe=False)
    elif request.method=='POST':
        try:
            req_data=json.loads(request.body.decode())
            content=req_data['content']
        except (KeyError, JSONDecodeError) as e:
            return HttpResponseBadRequest()
        user=User.objects.get(id=request.session['user_id'])
        comment=Comment(article=article,content=content,author=user)
        comment.save()
        return JsonResponse({'id':comment.id,'article_id':comment.article.id,'content':comment.content,
        'author_id':comment.author.id},status=201)
    else:
        return HttpResponseNotAllowed(['GET','POST'])

def comment_info(request,comment_id):
    if request.user.is_authenticated==False:
        return HttpResponse(status=401)
    comment=Comment.objects.get(id=comment_id)
    if request.method=='GET':
        return JsonResponse({'id':comment.id,'article_id':comment.article.id,
        'content':comment.content,'author_id':comment.author.id})
    elif request.method=='PUT':
        if comment.author.id!=request.session['user_id']:
            return HttpResponse(status=401)
        try:
            req_data=json.loads(request.body.decode())
            content=req_data['content']
        except (KeyError, JSONDecodeError) as e:
            return HttpResponseBadRequest()
        comment.content=content
        comment.save()
        return JsonResponse({'id':comment.id,'article_id':comment.article.id,
        'content':comment.content,'author_id':comment.author.id},status=200) 
    elif request.method=='DELETE':
        if comment.author.id!=request.session['user_id']:
            return HttpResponse(status=401)
        comment.delete()
        return HttpResponse(status=200)
    else :
        return HttpResponseNotAllowed(['GET','PUT','DELETE'])

@ensure_csrf_cookie
def token(request):
    if request.method == 'GET':
        return HttpResponse(status=204)
    else:
        return HttpResponseNotAllowed(['GET'])



