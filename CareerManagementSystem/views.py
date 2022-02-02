from urllib import request
from numpy import empty
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets
from threading import Thread, Condition
from rest_framework import pagination
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import time


from .models import (
    CarrerType, Carrer, CarrerPage, Counsellor, StudentFeaturedArticle, EditorApproveArticle
    )

from .serializer import (
    CarrerTypeSerializer, CarrerSerializer, CarrerPageSerializer, CounsellorSerializer, 
    StudentFeaturedArticleSerializer, EditorApproveArticleSerializer
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

editorFeacherArticleIdContext = {}
editorFeacherArticleSingleContext = {}
editorsingleDataUWContext = {}

counsellorIdContext = {}
counsellorSingleContext = {}
counsellorsingleDataUWContext = {}


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
    

def get_carrer_page(id, check):
    global carrerIdContext
    global carrerPageSingle
    global carrerSingleData
    global carrerPageAllData

    if check == "id":
        if id in carrerIdContext:
            return carrerIdContext[id].id
        obj = CarrerPage.objects.get(carrer = id)
        return obj.id

    if check == "singleData":
        if id in carrerPageSingle:
            return carrerPageSingle[id]
        obj = CarrerPage.objects.get(carrer = id)
        serializer = CarrerPageSerializer(obj, many=False)
        carrerPageSingle[id] = serializer.data
        return serializer.data

    if check == "all":
        if carrerPageAllData != '':
            return carrerPageAllData
        obj = CarrerPage.objects.all()
        serializer = CarrerPageSerializer(obj, many=True)
        carrerPageAllData = serializer.data
        return serializer.data


def get_student_featured_article(id, request, check):
    global carrerIdContext
    global studentFeacherArticleIdContext
    global studentFeacherArticleSingleContext

    if check == "id":
        if id in studentFeacherArticleIdContext:
            return studentFeacherArticleIdContext[id].id
        obj = StudentFeaturedArticle.objects.get(carrer = id)
        studentFeacherArticleIdContext[id] = obj
        return obj.id

    if check == "userWise":
        obj = StudentFeaturedArticle.objects.filter(user = request.user).order_by('-id')
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
        context = {'editorArticle': serializer.data, 'page': page, 'pages': paginator.num_pages}
        return context

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
    if check == "id":
        if id in editorFeacherArticleIdContext:
            return editorFeacherArticleIdContext[id].id
        obj = EditorApproveArticle.objects.get(id = id)
        editorFeacherArticleIdContext[id] = obj
        return obj.id

    if check == "singleData":
        if id in editorFeacherArticleSingleContext:
            return editorFeacherArticleSingleContext[id]
        obj = EditorApproveArticle.objects.get(id = id)
        serializer = EditorApproveArticleSerializer(obj, many=False)
        editorFeacherArticleSingleContext[id] = serializer.data
        return serializer.data
    
    # if id == "ediArticleId":
    #     obj = EditorApproveArticle.objects.filter(studentArticle = id)
    #     return obj
    
    # if id == "ediArticleIdSerializer":
    #     obj = EditorApproveArticle.objects.filter(studentArticle = id)
    #     serializer = EditorApproveArticleSerializer(obj, many=True)
    #     return serializer.data

    
    if check == "paginationSearch":
        query = request.query_params.get('keyword')
        if query == None:
            query = ''
            obj = EditorApproveArticle.objects.filter(articleApprove = "Approved").order_by('-createAt')[:10]
        else:
            if query in carrerIdContext:
                carrerSearch = carrerIdContext[id].id
            else:
                carrerSearch = Carrer.objects.get(id = query) 
            obj = EditorApproveArticle.objects.filter(carrer=carrerSearch, articleApprove = "Approved").order_by('-createdAt')[:10]
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


def get_counsellor(id, request, check):
    global counsellorIdContext
    global counsellorSingleContext
    global counsellorsingleDataUWContext

    if check == "id":
        if id in counsellorIdContext:
            return counsellorIdContext[id].id
        obj = Counsellor.objects.get(id = id)
        counsellorIdContext[id] = obj
        return obj.id
    
    if check == "singleData":
        if id in counsellorSingleContext:
            return counsellorSingleContext[id]
        obj = Counsellor.objects.get(studentArticle = id)
        serializer = CounsellorSerializer(obj, many=False)
        counsellorSingleContext[id] = serializer.data
        return serializer.data

    if check == "paginationSearch":
        query = request.query_params.get('keyword')
        if query == None:
            query = ''
            obj = Counsellor.objects.filter().order_by('-createAt')[:10]
        if query != '':
            carrerSearch = Counsellor.objects.filter(carrer = query) 
            obj = Counsellor.objects.filter(carrer=carrerSearch).order_by('-createdAt')[:10]
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


##=========================================== Thread Class ====================================================##
class GetCarrerPage:
    def __init__(self, carrId, request):
        self.allData = {}
        Thread.__init__(self)
        self.carrId = carrId
        self.request = request
        self.carrerId = ''
        self.carrerPageId = ''
        self.studentFeaturedId = ''
        self.lock = Condition()

    def get_carrer_th(self):
        self.lock.acquire()
        self.carrerId = get_carrer(self.carrId, 'id')
        self.lock.notify()
        self.lock.release()

    def get_carrer_page_th(self):
        carrerPage = get_carrer_page(self.carrId, 'singleData')
        self.allData['carrerPage'] = carrerPage

    def get_student_featured_article_th(self):
        self.lock.acquire()
        self.studentFeatured = get_student_featured_article(self.carrerId, self.request, 'id')
        self.lock.notify()
        self.lock.release()

    def get_editor_article_th(self):
        self.lock.acquire()
        editorFeaturedSerializer = get_editor_approve_article(self.studentFeatured, self.request, 'paginationSearch')
        self.allData['editorArticle'] = editorFeaturedSerializer
        self.lock.notify()
        self.lock.release()
    
    def get_counsellor_th(self):
        counsellorPage = get_counsellor(self.carrId, self.request, 'paginationSearch')
        self.allData['counsellor'] = counsellorPage



##=========================================== Api View Func ====================================================##
@permission_classes([IsAuthenticated])
# @authentication_classes([JWTAuthentication])
@api_view(['GET'])
def getCarrerPage(request):
    start = time.time()
    global carrerPageContext
    id = '1'
    if id in carrerPageContext:
        end = time.time()
        print(f"Runtime of the program is {end - start}")
        return Response(carrerPageContext[id])
    else:
        classObj = GetCarrerPage(id, request)
        c = Thread(target=classObj.get_carrer_th)
        cp = Thread(target=classObj.get_carrer_page_th)
        sfa = Thread(target=classObj.get_student_featured_article_th)
        efa = Thread(target=classObj.get_editor_article_th)
        coun = Thread(target=classObj.get_counsellor_th)
        c.start()
        cp.start()
        sfa.start()
        efa.start()
        coun.start()

        c.join()
        cp.join()
        sfa.join()
        efa.join()
        coun.join()
        
        carrerPageContext[id] = classObj.allData
        classObj.allData = {}
        end = time.time()
        print(f"Runtime of the program is {end - start}")
        return Response(carrerPageContext)







