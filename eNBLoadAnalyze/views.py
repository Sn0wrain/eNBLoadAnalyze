from django.shortcuts import HttpResponse, render, redirect
from django.views.decorators.csrf import csrf_exempt

import os

# Create your views here.
def index(request) :

    return render(request, 'index.html')

def uploadTDDLoadFile(request) :

    return render(request, 'dropzone_tdd.html')


def uploadFDDLoadFile(request):
    return render(request, 'dropzone_fdd.html')

def login(request) :
    return render(request, 'login.html')

def page_not_found(request):
    return render(request, '404.html')


# 增加装饰器，作用是跳过 csrf 中间件的保护
@csrf_exempt
def getTDDFile(request) :
    if request.method == "POST":    # 请求方法为POST时，进行处理
        myFile =request.FILES.get("tddFile", None)    # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            return HttpResponse("no files for upload!")

        if myFile.name.endswith('.xlsx')  == False :
            return HttpResponse('请上传xlsx格式的文件！')
        destination = open(os.path.join("D:\\python\\upload",myFile.name),'wb+')    # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():      # 分块写入文件
            destination.write(chunk)
        destination.close()
        return HttpResponse("upload over!")
  #  return 0