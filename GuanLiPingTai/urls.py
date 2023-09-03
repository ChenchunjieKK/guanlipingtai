"""
URL configuration for GuanLiPingTai project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from web.views import zero, account, check, my_celery

urlpatterns = [
    path("zero/", zero.zero),
    path("account/login/", account.login),
    path("account/register/", account.admin_add),
    path('image/code/', account.image_code),
    path('new/', account.new),

    # 账单管理
    path('check/list/', check.check_list),
    path('check/add/', check.check_model_form_add),
    path('check/<int:nid>/edit/', check.check_edit),
    path('check/<int:nid>/delete/', check.check_delete),
    path('check/deplay/', check.check_deplay),

    # celery并发异步
    path('celery/test/', my_celery.test),


]
