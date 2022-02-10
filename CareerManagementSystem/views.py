from urllib import request
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets
from threading import Thread, Condition, RLock
from rest_framework import pagination
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import time
import uuid
from videoCarrer.views import stu_wise_all_Video
from videoCarrer import views as videoViews
from CommanFunctions.paymentView import PaymentClass
from .models import (
    ArticlePaymentHistory, BookSlotPaymentHistory, CarrerType, Carrer, CarrerPage, Counsellor, CounsellorNoView, CounsellorRating, StudentFeaturedArticle, EditorApproveArticle,
    ArticleRating, ArticleNoView, CounsellorSlot, BookUserSlot
    )

from .serializer import (
    CarrerTypeSerializer, CarrerSerializer, CarrerPageSerializer, CounsellorSerializer, CounsellorSlotSerializer, 
    StudentFeaturedArticleSerializer, EditorApproveArticleSerializer, BookUserSlotSerializer
)

##=========================================== Cache ====================================================##

carrerIdContext = {}
carrerSingleData = {}
carrerAllData = ''
carrerPageContext = {}

articleSinglePagination = {}

carrerPageSingle = {}
carrerPageAllData = ''

studentFeacherArticleIdContext = {}
studentFeacherArticleSingleContext = {}
stuArticlesingleDataUWContext = {}
studentFeacherArticleSearchByEditorContext = {}

editorFeacherArticleIdContext = {}
editorFeacherArticleSingleContext = {}
editorsingleDataUWContext = {}

counsellorIdContext = {}
counsellorSingleContext = {}
counsellorsingleDataUWContext = {}

counsellorSearchDataContext = {}
counsellorHomeDataContext = {}

counsollerSlotIdContext = {}

# desboard
desStuWiseArticleContext = {}
desStuWiseSlotContext = {}
stuDesSelfArticleContext = {}
##=========================================== One Function ====================================================##

def get_carre_type(id, check):
    if check == "id":
        global carrerIdContext
        if id in carrerIdContext:
            return carrerIdContext[id].id
        obj = CarrerType.objects.get(id = id)
        carrerIdContext['id'] = obj.id
        return obj.id

    if check == "singleData":
        obj = CarrerType.objects.get(id = id)
        serializer = CarrerTypeSerializer(obj, many=False)
        return serializer.data

    if check == "all":
        obj = CarrerType.objects.all()
        serializer = CarrerTypeSerializer(obj, many=True)
        return serializer.data

def get_carrer(id, check):
    global carrerIdContext
    global carrerSingleData
    global carrerAllData
    if check == "id":
        if id in carrerIdContext:
            return carrerIdContext[id].id
        obj = Carrer.objects.get(id = id)
        return obj.id

    if check == "singleData":
        if id in carrerIdContext:
            if carrerIdContext[id].id in carrerSingleData:
                return carrerIdContext[carrerIdContext[id].id]
            else:
                serializer = CarrerSerializer(carrerIdContext[id].id, many=False)
                carrerSingleData[carrerIdContext[id].id] = serializer.data
                return serializer.data
        else:
            obj = Carrer.objects.get(id = id)
            serializer = CarrerSerializer(obj, many=False)
            carrerSingleData[obj] = serializer.data
            return serializer.data

    if check == "all":
        if carrerAllData != '':
            return carrerAllData
        obj = Carrer.objects.all()
        serializer = CarrerSerializer(obj, many=True)
        carrerAllData = serializer.data
        return serializer.data
    

def get_carrer_page(id, request, check):
    global carrerIdContext
    global carrerPageContext

    if check == "id":
        if id in carrerIdContext:
            return carrerIdContext[id]
        obj = CarrerPage.objects.get(carrer = id)
        return obj.id

    if check == "carrerPage":
        if id in carrerIdContext:
            id = carrerIdContext[id]
        obj = CarrerPage.objects.get(carrer = id)
        serializer = CarrerPageSerializer(obj, many=False)
        return serializer.data


def get_student_featured_article(id, request, check):
    global carrerIdContext
    global studentFeacherArticleIdContext
    global studentFeacherArticleSingleContext
    global studentFeacherArticleSearchByEditorContext
    global stuDesSelfArticleContext

    if check == "id":
        if id in studentFeacherArticleIdContext:
            return studentFeacherArticleIdContext[id].id
        obj = StudentFeaturedArticle.objects.get(carrer = id)
        studentFeacherArticleIdContext[id] = obj
        return obj.id

    if check == "userWise":
        if request.user.id in stuDesSelfArticleContext:
            return stuDesSelfArticleContext[request.user.id]
        obj = StudentFeaturedArticle.objects.filter(user = request.user).order_by('-id')
        serializer = StudentFeaturedArticleSerializer(obj, many=True)
        stuDesSelfArticleContext[request.user.id]  = serializer.data
        return serializer.data


    if check == "editorBye":
        query = request.query_params.get('keyword')
        if query == None:
            query = ''
            obj = StudentFeaturedArticle.objects.filter().order_by('-createAt')[:10]
        else:
            if query in carrerIdContext:
                query = carrerIdContext[id]
            carrerSearch = Carrer.objects.get(id = query) 
            carrerIdContext[id] = carrerSearch
            obj = StudentFeaturedArticle.objects.filter(carrer=carrerSearch).order_by('-createdAt')[:10]
            
        page = request.query_params.get('page')
        paginator = Paginator(obj,10)

        try:
            obj = paginator.page(page)
        except PageNotAnInteger:
            obj = paginator.page(1)
        except EmptyPage:
            obj = paginator.page(paginator.num_pages)

        if page == None:
            page = 1

        page = int(page)
        serializer = StudentFeaturedArticleSerializer(obj, many=True)
        context = {'studentArticle': serializer.data, 'page': page, 'pages': paginator.num_pages}
        return context
    
    if check == "editorByeUpdate":
        data = request.data
        file = request.FILES
        try:
            StudentFeaturedArticle.objects.filter(id = id).update(
                title=data['title'],
                heading=data['heading'],
                description=data['description'],
                thumbnailImage=file['thumbnailImage'],
                bannerImage=file['bannerImage'],
            )
            return True
        except:
            return False
    

    if check == "userWiseSingleData":
        if id in stuArticlesingleDataUWContext:
            return stuArticlesingleDataUWContext[id]
        obj = StudentFeaturedArticle.objects.filter(id = id)
        serializer = StudentFeaturedArticleSerializer(obj, many=True)
        stuArticlesingleDataUWContext[id] = serializer.data
        return serializer.data
    
    if check == "delete":
        if id in studentFeacherArticleSingleContext:
            del studentFeacherArticleSingleContext[id]
        elif id in stuArticlesingleDataUWContext:
            del stuArticlesingleDataUWContext[id]
        StudentFeaturedArticle.objects.filter(id = id).delete()
        return True


def get_editor_approve_article(id, request, check):
    global editorFeacherArticleIdContext
    global editorFeacherArticleSingleContext
    global stuArticlesingleDataUWContext
    global editorsingleDataUWContext
    global carrerIdContext
    global desStuWiseArticleContext

    if check == "id":
        if id in editorFeacherArticleIdContext:
            return editorFeacherArticleIdContext[id].id
        obj = EditorApproveArticle.objects.get(id = id)
        editorFeacherArticleIdContext[id] = obj
        return obj.id
    
    if check == "carrerPage":
        if id in carrerIdContext:
            carrerId = carrerIdContext[id]
        carrerId = Carrer.objects.get(id = id)
        obj = EditorApproveArticle.objects.filter(carrer = carrerId, articleApprove = "Approved", rating__gte=4).order_by('-createAt')[:10]
        serializer = EditorApproveArticleSerializer(obj, many=True)
        return serializer.data


    if check == "singleData":
        if id in editorFeacherArticleIdContext:
            obj = editorFeacherArticleIdContext[id]
        else:    
            obj = EditorApproveArticle.objects.get(id = id)
            editorFeacherArticleIdContext[id] = obj
        if obj.paymentChoices == "Paid":
            classObj = PaymentClass()
            pt = Thread(target=classObj.PaytemFunc, args=(1, obj, request, str(obj.ammount)))
            pt.start()
            pt.join()
            payFuncObj = classObj.data
            if payFuncObj != 308:
                return payFuncObj
            else:
                t = Thread(target=no_view_article, args=(request.user, id))
                t.start()
                t.join()
                if id in editorFeacherArticleSingleContext:
                    return editorFeacherArticleSingleContext[id]
                serializer = EditorApproveArticleSerializer(obj, many=False)
                editorFeacherArticleSingleContext[id] = serializer.data
                return serializer.data
        else:
            t = Thread(target=no_view_article, args=(request.user, id))
            t.start()
            t.join()
            if id in editorFeacherArticleSingleContext:
                return editorFeacherArticleSingleContext[id]
            serializer = EditorApproveArticleSerializer(obj, many=False)
            editorFeacherArticleSingleContext[id] = serializer.data
            return serializer.data
    
    
    if check == "paginationSearch":
        query = request.query_params.get('keyword')
        if query == None:
            obj = EditorApproveArticle.objects.filter(articleApprove = "Approved").order_by('-createAt')[:10]
        else:
            if query in carrerIdContext:
                carrerSearch = carrerIdContext[query]
            carrerSearch = Carrer.objects.get(id = query) 
            carrerIdContext[query] = carrerSearch
            obj = EditorApproveArticle.objects.filter(carrer=carrerSearch, articleApprove = "Approved").order_by('-createAt')[:10]
        page = request.query_params.get('page')
        paginator = Paginator(obj,1)

        try:
            obj = paginator.page(page)
        except PageNotAnInteger:
            obj = paginator.page(1)
        except EmptyPage:
            obj = paginator.page(paginator.num_pages)

        if page == None:
            page = 1
        page = int(page)
        serializer = EditorApproveArticleSerializer(obj, many=True)
        context = {'editorArticle': serializer.data, 'page': page, 'pages': paginator.num_pages}
        return context


    if check == "userWise":
        obj = EditorApproveArticle.objects.filter().order_by('-createAt')
        page = request.query_params.get('page')
        paginator = Paginator(obj,10)

        try:
            obj = paginator.page(page)
        except PageNotAnInteger:
            obj = paginator.page(1)
        except EmptyPage:
            obj = paginator.page(paginator.num_pages)

        if page == None:
            page = 1

        page = int(page)
        serializer = EditorApproveArticleSerializer(obj, many=True)
        context = {'editorArticle': serializer.data, 'page': page, 'pages': paginator.num_pages}
        return context

    if check == "userWiseSingleData":
        if id in editorsingleDataUWContext:
            return editorsingleDataUWContext[id]
        obj = EditorApproveArticle.objects.filter(id = id)
        serializer = EditorApproveArticleSerializer(obj, many=True)
        editorsingleDataUWContext[id] = serializer.data
        return serializer.data

    if check == "userWiseDelete":
        if id in editorsingleDataUWContext:
            del editorsingleDataUWContext[id] 
        if id in editorFeacherArticleSingleContext:
            del editorFeacherArticleSingleContext[id] 
        EditorApproveArticle.objects.filter(id = id).delete()
        return True
    

    if check == "desStuWiseArticle":
        if request.user.id in desStuWiseArticleContext:
            return desStuWiseArticleContext[request.user.id]
        else:
            getId = list(ArticlePaymentHistory.objects.filter(user = request.user, RESPCODE = "01").values_list('article', flat=True))
            obj = EditorApproveArticle.objects.filter(id__in=getId)
            serializer = EditorApproveArticleSerializer(obj, many=True)
            desStuWiseArticleContext[request.user.id] = serializer.data
            return serializer.data
        

def stu_wise_all_slot(request, check):
    global desStuWiseSlotContext
    if check == "desStuWiseSlot":
        if request.user.id in desStuWiseSlotContext:
            return desStuWiseSlotContext[request.user.id]
        else:
            getId = list(BookSlotPaymentHistory.objects.filter(user = request.user, RESPCODE = "01").values_list('slotBook', flat=True))
            obj = BookUserSlot.objects.filter(id__in=getId)
            serializer = BookUserSlotSerializer(obj, many=True)
            desStuWiseSlotContext[request.user.id] = serializer.data
            return serializer.data


def get_counsellor(id, request, check):
    global counsellorIdContext
    global counsellorSingleContext
    global counsellorsingleDataUWContext
    global carrerIdContext
    global counsellorHomeDataContext
    global counsellorSearchDataContext

    if check == "id":
        if id in counsellorIdContext:
            return counsellorIdContext[id].id
        obj = Counsellor.objects.get(id = id)
        counsellorIdContext[id] = obj
        return obj.id
    
    if check == "singleData":
        t = Thread(target=no_view_counsellor, args=(request.user, id))
        t.start()
        t.join()
        if id in counsellorSingleContext:
            return counsellorSingleContext[id]
        obj = Counsellor.objects.get(id = id)
        serializer = CounsellorSerializer(obj, many=False)
        counsellorSingleContext[id] = serializer.data
        return serializer.data

    if check == "paginationSearch":
        query = request.query_params.get('keyword')
        if query == None:
            query = ''
            obj = Counsellor.objects.filter().order_by('-createAt')
        else:
            if query in carrerIdContext:
                carrerSearch = carrerIdContext[query]
            carrerSearch = Carrer.objects.get(id = query) 
            carrerIdContext[query] = carrerSearch
            obj = Counsellor.objects.filter(carrer=carrerSearch).order_by('-createAt')
        page = request.query_params.get('page')
        paginator = Paginator(obj,1)

        try:
            obj = paginator.page(page)
        except PageNotAnInteger:
            obj = paginator.page(1)
        except EmptyPage:
            obj = paginator.page(paginator.num_pages)

        if page == None:
            page = 1

        page = int(page)
        serializer = CounsellorSerializer(obj, many=True)
        context = {'counsellor': serializer.data, 'page': page, 'pages': paginator.num_pages}
        return context


    if check == "carrerPage":
        if id in carrerIdContext:
            id = carrerIdContext[id]
        id = Carrer.objects.get(id = id) 
        obj = Counsellor.objects.filter(carrer=id, rating__gte=4).order_by('-id')[:10]
        serializer = CounsellorSerializer(obj, many=True)
        return serializer.data

    
    if check == "userWise":
        obj = Counsellor.objects.filter(user = request.user).order_by('-id')
        page = request.query_params.get('page')
        paginator = Paginator(obj,10)

        try:
            obj = paginator.page(page)
        except PageNotAnInteger:
            obj = paginator.page(1)
        except EmptyPage:
            obj = paginator.page(paginator.num_pages)

        if page == None:
            page = 1

        page = int(page)
        serializer = CounsellorSerializer(obj, many=True)
        context = {'counsellor': serializer.data, 'page': page, 'pages': paginator.num_pages}
        return context


    if check == "userWiseSingleData":
        if id in counsellorsingleDataUWContext:
            return counsellorsingleDataUWContext[id]
        obj = Counsellor.objects.filter(id = id, user = request.user)
        serializer = CounsellorSerializer(obj, many=True)
        counsellorsingleDataUWContext[id] = serializer.data
        return serializer.data

    if check == "userWiseDelete":
        if id in counsellorsingleDataUWContext:
            del counsellorsingleDataUWContext[id]   
        Counsellor.objects.filter(id = id, user = request.user).delete()
        return True


def no_view_counsellor(user, pk):
    obj = Counsellor.objects.get(id = pk)
    if CounsellorNoView.objects.filter(counsellor = obj, user = user).exists():
        return
    else:
        CounsellorNoView.objects.create(
            user = user, 
            counsellor = obj,
            noView = 1,
        )
        totalView = obj.noView + 1
        obj.noView = totalView
        obj.save()
        return

def no_view_article(user, pk):
    obj = EditorApproveArticle.objects.get(id = pk)
    if ArticleNoView.objects.filter(editorApproveArticle = obj, user = user).exists():
        return
    else:
        ArticleNoView.objects.create(
            user = user, 
            editorApproveArticle = obj,
            noView = 1,
        )
        totalView = obj.noView + 1
        obj.noView = totalView
        obj.save()
        return


def booking_th(user, obj):
    l = RLock()
    l.acquire(blocking=True)
    try:
        BookUserSlot.objects.create(
            user = user,
            counsellorSlot = obj,
        )
        l.release()
        return True
    except:
        l.release()
        return False

##=========================================== Thread Class ====================================================##
class GetCarrerPage:
    def __init__(self):
        self.allData = {}
        Thread.__init__(self)
        self.lock = Condition()

    def get_carrer_page_th(self, id, request, check):
        carrerPage = get_carrer_page(id, request, check)
        
        self.allData['carrerPage'] = carrerPage

    def get_editor_article_th(self, id, request, check):
        editorFeaturedSerializer = get_editor_approve_article(id, request, check)
        self.allData['article'] = editorFeaturedSerializer
    
    def get_counsellor_th(self, id, request, check):
        counsellorPage = get_counsellor(id, request, check)
        self.allData['counsellor'] = counsellorPage
    
    def get_video_carrer_th(self, id, request, check):
        videoCarrerData = videoViews.get_video_carrer_func(id, request, check)
        self.allData['videoCarrer'] = videoCarrerData



class CounsellorGet:
    def __init__(self):
        self.signal = ''
        self.allData = ''
        self.singleData = ''
        Thread.__init__(self)

    def all_data_th(self, id, request, check):
        self.allData = get_counsellor(id, request, check)
        return
    
    def single_data_th(self, id, request, check):
        self.singleData = get_counsellor(id, request, check)
        return

class EditorGet:
    def __init__(self):
        self.signal = ''
        self.allData = ''
        self.singleData = ''
        Thread.__init__(self)

    def all_data_th(self, id, request, check):
        self.allData = get_editor_approve_article(id, request, check)
        return
    
    def single_data_th(self, id, request, check):
        self.singleData = get_editor_approve_article(id, request, check)
        return


class ShowSlot:
    def __init__(self):
        self.allData = ''
        self.slotBookingSignal = ''
        self.payment = ''
        Thread.__init__(self)

    def show_slot_th(self, user, id):
        global counsellorIdContext
        if id in counsellorIdContext:
            obj = counsellorIdContext[id]
        else:
            obj = Counsellor.objects.get(id = id)
            counsellorIdContext[id] = obj
        slotObj = CounsellorSlot.objects.filter(counsellor = obj)    
        serializer = CounsellorSlotSerializer(slotObj, many=True)
        self.allData = serializer.data
        return

    def booking_pay(self, request, id):
        global counsollerSlotIdContext
        if id in counsollerSlotIdContext:
            obj = counsollerSlotIdContext[id]
        else:
            obj = CounsellorSlot.objects.get(id = id)
            counsollerSlotIdContext[id] = obj
        classObj = PaymentClass()
        pt = Thread(target=classObj.PaytemFunc, args=(3, obj, request, str(obj.counsellor.price)))
        pt.start()
        pt.join()
        if classObj.data != 402:
            self.payment = classObj.data
            return 
        self.payment == 402
        return
        
class StudentDeshBordView:
    def __init__(self):
        self.allData = {}
        Thread.__init__(self)

    def get_edi_article_th(self, id, request, check):
        article = get_editor_approve_article(id, request, check)
        self.allData['article'] = article

    def get_edi_video_th(self, request, check):
        video = stu_wise_all_Video(request, check)
        self.allData['video'] = video

    def get_edi_slot_th(self, request, check):
        slot = stu_wise_all_slot(request, check)
        self.allData['slot'] = slot

    def get_stu_article_th(self, id, request, check):
        stuArticle = get_student_featured_article(id, request, check)
        self.allData['stuArticle'] = stuArticle

##=========================================== Api View Func ====================================================##
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
@api_view(['GET'])
def getCarrerPage(request, id):
    global carrerPageContext
    if id in carrerPageContext:
        return Response(carrerPageContext[id])
    else:
        classObj = GetCarrerPage()
        cp = Thread(target=classObj.get_carrer_page_th, args=(id, request, "carrerPage"))
        efa = Thread(target=classObj.get_editor_article_th, args=(id, request, "carrerPage"))
        coun = Thread(target=classObj.get_counsellor_th, args=(id, request, "carrerPage"))
        vc = Thread(target=classObj.get_video_carrer_th, args=(id, request, "carrerPage"))
        cp.start()
        efa.start()
        coun.start() 
        vc.start()

        cp.join()
        efa.join()
        coun.join()
        vc.join()
        
        carrerPageContext[id] = classObj.allData
        classObj.allData = {}
        return Response(carrerPageContext[id])


class CounsellorViewSet(viewsets.ViewSet):
    # permission_classes = [IsAdminUser]
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        # start = time.time()
        classOj = CounsellorGet()
        ct = Thread(target=classOj.all_data_th, args=("null", request, "paginationSearch"))
        ct.start()
        ct.join()
        # end = time.time()
        # print(f"Runtime of the program is {end - start}")
        return Response(classOj.allData)

    def retrieve(self, request, pk=None):
        classOj = CounsellorGet()
        sdt = Thread(target=classOj.single_data_th, args=(pk, request, "singleData"))
        sdt.start()
        sdt.join()
        return Response(classOj.singleData)


class EditorViewSet(viewsets.ViewSet):
    # permission_classes = [IsAdminUser]
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        classOj = EditorGet()
        ct = Thread(target=classOj.all_data_th, args=("null", request, "paginationSearch"))
        ct.start()
        ct.join()
        return Response(classOj.allData)

    def retrieve(self, request, pk=None):
        classOj = EditorGet()
        sdt = Thread(target=classOj.single_data_th, args=(pk, request, "singleData"))
        sdt.start()
        sdt.join()
        return Response(classOj.singleData)


# @api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# def getAllArticle(request):
#     classOj = EditorGet()
#     ct = Thread(target=classOj.all_data_th, args=("null", request, "paginationSearch"))
#     ct.start()
#     ct.join()
#     return Response(classOj.allData)


signal = ''

@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def articleRating(request, pk):
    data = request.data
    user = request.user
    global signal

    def rating_count(pk):
        global signal
        obj = EditorApproveArticle.objects.get(id = pk)
        if ArticleRating.objects.filter(user = user, editorApproveArticle = obj).exists():
            signal = False
            return 
        else:
            ArticleRating.objects.create(
                user = user,
                editorApproveArticle = obj,
                rating = data['rating'],
            )
            ratingCount = obj.rating
            obj.rating = int(((5 * ratingCount) + data['rating']) / (ratingCount + 1))
            obj.save()
            signal = True
            return 
    t = Thread(target=rating_count, args=(pk,))
    t.start()
    t.join()
    if signal == True:
        signal = ''
        return Response(status.HTTP_201_CREATED)
    else:
        signal = '' 
        return Response(status.HTTP_208_ALREADY_REPORTED)



@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def counsellorRating(request, pk):
    data = request.data
    user = request.user
    global signal
    def rating_count(pk):
        global signal
        obj = Counsellor.objects.get(id = pk)
        if CounsellorRating.objects.filter(user = user, counsellor = obj).exists():
            signal = False
            return 
        else:
            CounsellorRating.objects.create(
                user = user,
                counsellor = obj,
                rating = data['rating'],
            )
            ratingCount = obj.rating
            obj.rating = int(((5 * ratingCount) + data['rating']) / (ratingCount + 1))
            obj.save()
            signal = True
            return 
    t = Thread(target=rating_count, args=(pk,))
    t.start()
    t.join()
    if signal == True:
        signal = ''
        return Response(status.HTTP_201_CREATED)
    else:
        signal = '' 
        return Response(status.HTTP_208_ALREADY_REPORTED)



@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def slotBooking(request, pk):
    user = request.user
    if request.method == "GET":
        classObj = ShowSlot()
        t = Thread(target=classObj.show_slot_th, args=(user, pk))
        t.start()
        t.join()
        return Response(classObj.allData)
    if request.method == "POST":
        classObj = ShowSlot()
        t = Thread(target=classObj.booking_pay, args=(request, pk))
        t.start()
        t.join()
        if classObj.payment != 402:
            return Response(classObj.payment)
        return Response(status.HTTP_406_NOT_ACCEPTABLE)

    

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def studentDeshBord(request):
    classObj = StudentDeshBordView()
    ea = Thread(target=classObj.get_edi_article_th, args=("null", request, "desStuWiseArticle"))
    sv = Thread(target=classObj.get_edi_video_th, args=(request, "desStuWiseVideo"))
    ss = Thread(target=classObj.get_edi_slot_th, args=(request, "desStuWiseSlot"))
    sa = Thread(target=classObj.get_stu_article_th, args=("null", request, "userWise"))

    ea.start()
    sv.start()
    ss.start()
    sa.start()
    
    ea.join()
    sv.join()
    ss.join()
    sa.join()
    return Response(classObj.allData)
    
        