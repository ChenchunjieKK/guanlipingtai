from django.shortcuts import render,HttpResponse

# Create your views here.
from mycelery.sms.tasks import send_sms, send_sms2

import time


def test(request):

    # 异步任务
    # 1. 声明一个和celery一模一样的任务函数，但是我们可以导包来解决

    result01 = send_sms.delay("110")
    result02 = send_sms2.delay("119")
    # send_sms.delay() 如果调用的任务函数没有参数，则不需要填写任何内容

    # 获取result 的 id
    id1 = result01.id
    id2 = result02.id

    # 将获取的id值去redis数据库中进行比对判定

    from celery.result import AsyncResult
    from mycelery.main import app

    async_result = AsyncResult(id=id1, app=app)

    if async_result.successful():
        result = async_result.get()
        return HttpResponse(result)
        # result.forget() # 将结果删除
    elif async_result.failed():
        return HttpResponse('执行失败')
    elif async_result.status == 'PENDING':
        return HttpResponse('任务等待中被执行')
    elif async_result.status == 'RETRY':
        return HttpResponse('任务异常后正在重试')
    elif async_result.status == 'STARTED':
        return HttpResponse('任务已经开始被执行')

    time.sleep(5)

    # 定时任务

    return HttpResponse("OK")