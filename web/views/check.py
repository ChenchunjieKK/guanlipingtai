"""
账单界面，使用导航条
仿照day16中的，实现账单list直接显示以及其数据的增删改查功能

先设计表单
时间 费用 用于什么事情
"""

from django.shortcuts import render, HttpResponse, redirect
from web import models
from django import forms
from django.db.models import Sum
from datetime import datetime

def check_list(request):
    """账单清单"""
    # 获取所有用户列表 [obj,obj,obj]
    queryset = models.Check.objects.all()
    return render(request, 'check_list.html', {"queryset": queryset})

def check_add(request):
    """新增账单"""
    if request.method == "GET":

        return render(request, 'check_add.html')


class CheckModelForm(forms.ModelForm):

    class Meta:
        model = models.Check
        fields = ["time", "money", "uses"]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件，添加了class="form-control"
        for name, field in self.fields.items():

            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def check_model_form_add(request):
    """
    添加用户（ModelForm版本）
    """
    if request.method == "GET":
        # 如果是GET请求，创建一个空的ModelForm实例
        form = CheckModelForm()
        # 渲染模板并将表单传递给模板
        return render(request, 'check_add.html', {"form": form})

        # 如果是POST请求，将请求的表单数据传递给ModelForm实例
    form = CheckModelForm(data=request.POST)
    if form.is_valid():
        # 如果表单验证成功，保存数据并重定向到列表页面
        form.save()
        return redirect('/check/list/')

        # 如果表单验证失败，渲染模板并将表单传递给模板，同时显示错误信息
    return render(request, 'check_add.html', {"form": form})

def check_edit(request, nid):
    """ 编辑用户 """
    # 从数据库获取nid为多少的所有数据
    row_object = models.Check.objects.filter(id=nid).first()

    if request.method == "GET":
        # 根据ID去数据库获取要编辑的那一行数据（对象）
        form = CheckModelForm(instance=row_object)
        return render(request, 'check_edit.html', {'form': form})

    form = CheckModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据，如果想要再用户输入以外增加一点值
        # form.instance.字段名 = 值
        form.save()
        return redirect('/check/list/')
    return render(request, 'check_edit.html', {"form": form})

def check_delete(request, nid):
    models.Check.objects.filter(id=nid).delete()
    return redirect('/check/list/')

def check_deplay(request):
    """将每天的开销进行累加，并类似于list样式在Html界面输出"""
    # 在数据库中查询time列所有的不重复的值，保存为一个列表
    unique_times = models.Check.objects.values_list('time', flat=True).distinct()
    time_list = list(unique_times)

    # 创建一个字典，将时间格式化，从tame_list遍历时间，累加money值
    result_dict = {}
    for time in time_list:
        formatted_date = time.strftime('%Y-%m-%d')
        accumulated_money = models.Check.objects.filter(time=time).aggregate(total_money=Sum('money'))
        result_dict[formatted_date] = accumulated_money['total_money'] if accumulated_money['total_money'] else 0

    return render(request, 'check_deplay.html', {'result_dict': result_dict})
