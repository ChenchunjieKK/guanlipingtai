"""
初始界面
需求：有登录与注册按钮，点击之后跳转至对应的界面
     背景图
"""
from django.shortcuts import render, HttpResponse, redirect

def zero(request):
    return render(request, 'zero.html')