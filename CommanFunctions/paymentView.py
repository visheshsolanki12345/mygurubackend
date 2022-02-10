from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from .PayTm import Checksum
from django.conf import settings
from threading import Thread, Condition, RLock, Event
import uuid
from CareerManagementSystem.models import (
    ArticlePaymentHistory, BookSlotPaymentHistory, 
    EditorApproveArticle, BookUserSlot, CounsellorSlot
)
from videoCarrer.models import VideoPaymentHistory
from CareerManagementSystem import views
from .models import CheckForPaymentId
from CareerManagementSystem import views

articleCheckPayment = []
videoCheckPayment = []


class PaymentClass:
    def __init__(self):
        self.data = ''
        Thread.__init__(self)

    def PaytemFunc(self, check, forPayment, request, amount):
        orderId = str(uuid.uuid4())
        user = request.user
        email = request.user.email
        global articleCheckPayment
        if check == 1:
            if forPayment in articleCheckPayment:
                self.data = 308
                return 
            else:
                if ArticlePaymentHistory.objects.filter(article = forPayment, RESPCODE = "01").exists():
                    articleCheckPayment.append(forPayment)
                    self.data = 308
                    return 
            ArticlePaymentHistory.objects.create(
                article = forPayment,
                user = user, 
                ORDER_ID = orderId, 
                TXN_AMOUNT = amount, 
                email = email,
            )
            CheckForPaymentId.objects.create(_id = orderId, forPayment = 1)

        elif check == 2:
            if forPayment in videoCheckPayment:
                self.data = 308
                return 
            else:
                if VideoPaymentHistory.objects.filter(video = forPayment, RESPCODE = "01").exists():
                    videoCheckPayment.append(forPayment)
                    self.data = 308
                    return 
            VideoPaymentHistory.objects.create(
                video = forPayment,
                user = user, 
                ORDER_ID = orderId, 
                TXN_AMOUNT = amount, 
                email = email,
            )
            CheckForPaymentId.objects.create(_id = orderId, forPayment = 2)

        elif check == 3:
            BookSlotPaymentHistory.objects.create(
                user = user, 
                ORDER_ID = orderId, 
                TXN_AMOUNT = amount, 
                email = email,
                counsId = str(forPayment.id)
            )
            CheckForPaymentId.objects.create(_id = orderId, forPayment = 3)

        param_dict={
            'MID': settings.PAYTEM_MID,
            'ORDER_ID': orderId,
            'TXN_AMOUNT': amount,
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'http://127.0.0.1:8000/api/comman-function/handlepayment/',
            # 'CALLBACK_URL':'https://visheshsolanki.pythonanywhere.com/api/handlepayment/',
        }

        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, settings.PAYTEM_MERCHANT_KEY)
        self.data = param_dict
        return 
        


class PayHendel:
    def __init__(self):
        self.signal = ''
        self.RedirectUrl = ''
        self.paymentFor = ''
        Thread.__init__(self)
        
    def payment_check(self, request):
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
                    ArticlePaymentHistory.objects.filter(ORDER_ID = response_dict['ORDERID']).update(
                        gateway = response_dict['GATEWAYNAME'],
                        bankname = response_dict['BANKNAME'],
                        TXNID = response_dict['TXNID'],
                        status = response_dict['STATUS'],
                        TXNDATE = response_dict['TXNDATE'],
                        RESPCODE = response_dict['RESPCODE'],
                        CURRENCY = response_dict['CURRENCY'],
                        PAYMENTMODE = response_dict['PAYMENTMODE'],
                        MID = response_dict['MID'],
                    )
                    obj = ArticlePaymentHistory.objects.get(ORDER_ID = response_dict['ORDERID'])
                    self.RedirectUrl = f"http://localhost:3000/article-page/{obj.article.id}"

                elif findCode == 2:
                    VideoPaymentHistory.objects.filter(ORDER_ID = response_dict['ORDERID']).update(
                        gateway = response_dict['GATEWAYNAME'],
                        bankname = response_dict['BANKNAME'],
                        TXNID = response_dict['TXNID'],
                        status = response_dict['STATUS'],
                        TXNDATE = response_dict['TXNDATE'],
                        RESPCODE = response_dict['RESPCODE'],
                        CURRENCY = response_dict['CURRENCY'],
                        PAYMENTMODE = response_dict['PAYMENTMODE'],
                        MID = response_dict['MID'],
                    )
                    obj = VideoPaymentHistory.objects.get(ORDER_ID = response_dict['ORDERID'])
                    self.RedirectUrl = f"http://localhost:3000/video-page/{obj.video.id}"

                elif findCode == 3:
                    if response_dict['RESPCODE'] == '01':
                        objGetId = BookSlotPaymentHistory.objects.get(ORDER_ID = response_dict['ORDERID'])
                        obj = CounsellorSlot.objects.get(id = objGetId.counsId)
                        signal = views.booking_th(objGetId.user, obj)
                        if signal == True:
                            bookObj = BookUserSlot.objects.get(counsellorSlot = obj)
                        BookSlotPaymentHistory.objects.filter(ORDER_ID = response_dict['ORDERID']).update(
                            slotBook = bookObj,
                            gateway = response_dict['GATEWAYNAME'],
                            bankname = response_dict['BANKNAME'],
                            TXNID = response_dict['TXNID'],
                            status = response_dict['STATUS'],
                            TXNDATE = response_dict['TXNDATE'],
                            RESPCODE = response_dict['RESPCODE'],
                            CURRENCY = response_dict['CURRENCY'],
                            PAYMENTMODE = response_dict['PAYMENTMODE'],
                            MID = response_dict['MID'],
                        )
                        obj = BookSlotPaymentHistory.objects.get(ORDER_ID = response_dict['ORDERID'])
                        self.RedirectUrl = f"http://localhost:3000/counsellor-page/{obj.slotBook.counsellorSlot.counsellor.id}"
                    else:
                        return
                if response_dict['RESPCODE'] == '01':
                    self.signal = True
                    return
                else:
                    print('order was not successful because' + response_dict['RESPMSG'])
                    self.signal = False
                    return 
            self.signal = False
            return 
        except:
            self.signal = False
            return 


@csrf_exempt
@api_view(['POST', 'GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
def HandlePayRequest(request):
    classObj = PayHendel()
    pht = Thread(target=classObj.payment_check, args=(request,))
    pht.start()
    pht.join()
    if classObj.signal == True:
        return redirect(classObj.RedirectUrl)
    return redirect("http://localhost:3000/error")

            
##============================== End... ================================##