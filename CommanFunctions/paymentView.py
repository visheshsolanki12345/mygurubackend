from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from .PayTm import Checksum
from django.conf import settings
from threading import Thread, Condition, RLock, Event
import uuid
from CareerManagementSystem.models import (
    ArticlePaymentHistory, BookSlotPaymentHistory, EditorApproveArticle
)
from CareerManagementSystem import views
from .models import CheckForPaymentId


def PaytemFunc(check, forPayment, user, orderId, amount, userEmail):
    param_dict={
        'MID': settings.PAYTEM_MID,
        'ORDER_ID': orderId,
        'TXN_AMOUNT': amount,
        'CUST_ID': userEmail,
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': 'WEBSTAGING',
        'CHANNEL_ID': 'WEB',
        'CALLBACK_URL':'http://127.0.0.1:8000/api/comman-function/handlepayment/',
        # 'CALLBACK_URL':'https://visheshsolanki.pythonanywhere.com/api/handlepayment/',
    }

    if check == 1:
        ArticlePaymentHistory.objects.create(
            article = forPayment,
            user = user, 
            ORDER_ID = orderId, 
            TXN_AMOUNT = amount, 
            email = userEmail,
        )
        CheckForPaymentId.objects.create(_id = orderId, forPayment = 1)

        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, settings.PAYTEM_MERCHANT_KEY)
        return param_dict
    


@csrf_exempt
@api_view(['POST', 'GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
def HandlePayRequest(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    try:
        verify = Checksum.verify_checksum(response_dict, settings.PAYTEM_MERCHANT_KEY, checksum)
        if verify:
            idFind = CheckForPaymentId.objects.get(_id = response_dict['ORDERID'])
            findCode = idFind.forPayment
            if findCode == 1:
                obj = ArticlePaymentHistory.objects.get(ORDER_ID = response_dict['ORDERID'])
                obj.gateway = response_dict['GATEWAYNAME'],
                obj.bankname = response_dict['BANKNAME'], 
                obj.TXNID = response_dict['TXNID'], 
                obj.status = response_dict['STATUS'], 
                obj.TXNDATE = response_dict['TXNDATE'],
                obj.RESPCODE = response_dict['RESPCODE'],
                obj.CURRENCY = response_dict['CURRENCY'],
                obj.PAYMENTMODE = response_dict['PAYMENTMODE'],
                obj.MID = response_dict['MID']
                obj.save()

                if response_dict['RESPCODE'] == '01':
                    print('order successful')
                    # url = "https://my-guru-test.herokuapp.com/paymentassessment"
                    url = "http://localhost:3000/"
                    return redirect(url)
                else:
                    print('order was not successful because' + response_dict['RESPMSG'])
                    return 
        return 
    except:
        return 
##============================== End... ================================##