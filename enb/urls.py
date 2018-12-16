"""enb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import eNBLoadAnalyze.views as eNB

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', eNB.index),
    path('index/', eNB.index),
    path('uploadTDDLoadFile/', eNB.uploadTDDLoadFile),
    path('uploadFDDLoadFile/', eNB.uploadFDDLoadFile),
    path('uploadTDDLoadFile/getTDDFile', eNB.getTDDFile),
    path('login/', eNB.login),
    path('registration', eNB.reg)
]

handler404 = eNB.page_not_found #改动2