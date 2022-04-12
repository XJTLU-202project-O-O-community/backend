from django.shortcuts import render
import json
from django.core import serializers
from django.db.models import Q, Count, Sum, Aggregate, CharField
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .models import *


class Concat(Aggregate):
    """ORM用来分组显示其他字段 相当于group_concat"""
    function = 'GROUP_CONCAT'
    template = '%(function)s(%(distinct)s%(expressions)s)'

    def __init__(self, expression, distinct=False, **extra):
        super(Concat, self).__init__(
            expression,
            distinct='DISTINCT ' if distinct else '',
            output_field=CharField(),
            **extra)


'''
get 返回所有动态
'''


@require_http_methods(['GET'])
def get_posts(request):
    if request.method == 'GET':
        try:
            content = moments_info.objects.values('id', 'user_id', 'content', 'thumbs', 'likes', 'user_id__name',
                                                  'user_id__photo', 'user_id__signature').annotate(
                url=Concat('imgs__url')).order_by('-ctime')
            content = list(content)
            result = {
                'error_code': 200,
                'msg': 'success get moments',
                'data': {
                    'moments': content
                }
            }
            return JsonResponse(result, status=200)
        except Exception as e:
            print(e)
            result = {
                'error_code': 500,
                'msg': 'something wrong happens',
            }
            return JsonResponse(result, status=200)


'''
api: /posting/moment
post 发动态
get 看某个人的动态
'''


@require_http_methods(['GET', 'POST'])
def single_post(request):
    if request.method == 'POST':
        try:
            print(request.POST)
            user_id = request.POST.get("user_id")
            content = request.POST.get("content")
            imgList = request.POST.get("imglist")
            print(user_id,content,imgList)
            moments = moments_info.objects.create(user_id_id=user_id, content=content, thumbs=0, likes=0)
            if imgList != None:
                imgList = imgList.split(',')
                for i in range(len(imgList)):
                    imgs.objects.create(url=imgList[i], moments_id=moments.id)
            result = {
                'error_code': 200,
                'msg': 'moments created successfully',
            }
            return JsonResponse(result, status=200)
        except Exception as e:
            print(e)
            result = {
                'error_code': 500,
                'msg': 'counter problems',
            }
            return JsonResponse(result, status=500)

    if request.method == 'GET':
        try:
            user = request.GET.get('userid')
            content = moments_info.objects.filter(user_id=user).values('id', 'content', 'thumbs', 'user_id__name',
                                                                       'user_id__photo',
                                                                       ).annotate(url=Concat('imgs__url')).order_by(
                '-ctime')

            result = {
                'error_code': 200,
                'msg': 'successfully get personal moments',
                'data': {
                    'own_moments': list(content)
                }
            }
            return JsonResponse(result, status=200)
        except Exception as e:
            print(e)
            result = {
                'error_code': 500,
                'msg': 'encounter problems',
            }
            return JsonResponse(result, status=500)


@require_http_methods('POST')
def delete(request):
    try:
        delete_id = request.POST.get('id')
        print(delete_id,99999)
        moments_info.objects.filter(id=delete_id).delete()
        result = {
            'error_code': 200,
            'msg': 'deleted successfully',
        }
        return JsonResponse(result, status=200)

    except Exception as e:
        print(e)
        result = {
            'error_code': 500,
            'msg': 'encounter problems',
        }
        return JsonResponse(result, status=500)


@require_http_methods('POST')
def edit(request):
    try:
        edit_id = request.POST.get('id')
        edit_content = request.POST.get('content')
        # imgs=requ
        moments_info.objects.filter(id=edit_id).update(content=edit_content)
        data = moments_info.objects.filter(id=edit_id).values('id', 'content')
        result = {
            'error_code': 200,
            'msg': 'successfully edit moments',
            'data': {
                'own_moments': list(data)
            }
        }
        return JsonResponse(result, status=200)
    except Exception as e:
        print(e)
        result = {
            'error_code': 500,
            'msg': 'counter problems',
        }
        return JsonResponse(result, status=500)


@require_http_methods('POST')
def img_uploader(request):
    try:
        img = request.FILES['file']
        print(img.name)
        f=open('./media/moments/'+img.name,'wb+')
        f.write(img.read())
        f.close()
        res = {
            'code': 200,
            'message': 'upload success'
        }
        return JsonResponse(res, status=200)
    except Exception as e:
        print(e)
        res = {
            'code': 500,
            'message': 'Count problems'
        }
        return JsonResponse(res, status=500)

# Create your views here.
