from django.shortcuts import HttpResponse, render, redirect
from django.views.decorators.csrf import csrf_exempt

import os

fddResdata = [
{"period": '2018-10-01', "PUSCH": 2, "PDSCH": 104, "PDCCH": 62, "RRC": 0},
{"period": '2018-10-08', "PUSCH": 2, "PDSCH": 146, "PDCCH": 68, "RRC": 0},
{"period": '2018-10-15', "PUSCH": 4, "PDSCH": 112, "PDCCH": 60, "RRC": 0},
{"period": '2018-10-22', "PUSCH": 0, "PDSCH": 106, "PDCCH": 55, "RRC": 0},
{"period": '2018-10-29', "PUSCH": 0, "PDSCH": 66, "PDCCH": 45, "RRC": 0},
{"period": '2018-11-05', "PUSCH": 1, "PDSCH": 77, "PDCCH": 46, "RRC": 0},
{"period": '2018-11-12', "PUSCH": 2, "PDSCH": 79, "PDCCH": 36, "RRC": 0},
{"period": '2018-11-19', "PUSCH": 0, "PDSCH": 67, "PDCCH": 23, "RRC": 0},
{"period": '2018-11-26', "PUSCH": 0, "PDSCH": 74, "PDCCH": 31, "RRC": 0},
{"period": '2018-12-03', "PUSCH": 0, "PDSCH": 71, "PDCCH": 28, "RRC": 0},
{"period": '2018-12-10', "PUSCH": 2, "PDSCH": 100, "PDCCH": 42, "RRC": 0},
]

tddResdata = [
{"period": '2018-10-01', "PUSCH": 46, "PDSCH": 175, "PDCCH": 228, "RRC": 10},
{"period": '2018-10-08', "PUSCH": 49, "PDSCH": 207, "PDCCH": 311, "RRC": 32},
{"period": '2018-10-15', "PUSCH": 37, "PDSCH": 222, "PDCCH": 158, "RRC": 4},
{"period": '2018-10-22', "PUSCH": 36, "PDSCH": 231, "PDCCH": 162, "RRC": 3},
{"period": '2018-10-29', "PUSCH": 51, "PDSCH": 245, "PDCCH": 231, "RRC": 3},
{"period": '2018-11-05', "PUSCH": 43, "PDSCH": 252, "PDCCH": 205, "RRC": 2},
{"period": '2018-11-12', "PUSCH": 65, "PDSCH": 353, "PDCCH": 234, "RRC": 4},
{"period": '2018-11-19', "PUSCH": 70, "PDSCH": 380, "PDCCH": 242, "RRC": 7},
{"period": '2018-11-26', "PUSCH": 68, "PDSCH": 264, "PDCCH": 204, "RRC": 5},
{"period": '2018-12-03', "PUSCH": 64, "PDSCH": 289, "PDCCH": 212, "RRC": 12},
{"period": '2018-12-10', "PUSCH": 64, "PDSCH": 388, "PDCCH": 185, "RRC": 4},
]

# Create your views here.
def index(request) :
    return render(request, 'index.html', {'tddResdata': tddResdata, 'fddResdata': fddResdata})

def uploadTDDLoadFile(request) :

    return render(request, 'dropzone_tdd.html')


def uploadFDDLoadFile(request):
    return render(request, 'dropzone_fdd.html')

def login(request) :
    return render(request, 'login.html')

def reg(request) :
    return render(request, 'registration.html')

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