import time
from html5lib import serialize
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
from rest_framework import viewsets


from .models import (
    CarrerType, Carrer, CarrerPage, StudentFeaturedArticle, EditorApproveArticle, Counsellor
    )

from .serializer import (
    CarrerTypeSerializer, CarrerSerializer, CarrerPageSerializer,
    StudentFeaturedArticleSerializer, EditorApproveArticleSerializer
)

from . import views

data = ""

##=========================================== Thread Class ====================================================##
class PostStudentArticle:
    def __init__(self, reqest):
        self.signal = ''
        self.allData = ''
        self.singleData = ''
        Thread.__init__(self)
        try:
            self.request = reqest
            self.user = self.request.user
            self.data = self.request.data
            self.file = self.request.FILES
            self.carrerId = self.data['carrer']
            if self.carrerId in views.carrerIdContext:
                self.obj = views.carrerIdContext[id].id
            else:
                self.obj = Carrer.objects.get(id=self.carrerId)
                views.carrerIdContext[self.carrerId] = self.obj
        except:
            pass
    def create_th(self):
        try:
            StudentFeaturedArticle.objects.create(
                user=self.user,
                carrer=self.obj,
                heading=self.data['heading'],
                description=self.data['description'],
                bannerImage=self.file['bannerImage'],
            )
            self.signal = True
            return
        except:
            self.signal = False
            return
    
    def all_data_th(self):
        self.allData = views.get_student_featured_article("null", self.request, "userWise")
        return
    
    def single_data_th(self, id):
        self.singleData = views.get_student_featured_article(id, self.request, "userWiseSingleData")
        return

    def delete_data_th(self, id):
        self.signal = views.get_student_featured_article(id, self.request, "delete")
        return


class CounsellorRegister:
    def __init__(self, reqest):
        self.signal = ''
        self.allData = ''
        self.singleData = ''
        Thread.__init__(self)
        self.request = reqest

        self.user = self.request.user
        self.data = self.request.data
        try:
            self.carrerId = self.data["carrer"]

            if self.carrerId in views.carrerIdContext:
                self.carrerObj = views.carrerIdContext[self.carrerId]
            else:
                self.carrerObj = Carrer.objects.get(id=self.carrerId)
                views.carrerIdContext[self.carrerId] = self.carrerObj
        except:
            pass

    def all_data_th(self):
        self.allData = views.get_counsellor("null", self.request, "userWise")
        return
    
    def single_data_th(self, id):
        self.singleData = views.get_counsellor(id, self.request, "userWiseSingleData")
        return
    
    def delete_data_th(self, id):
        self.signal = views.get_counsellor(id, self.request, "userWiseDelete")
        return

    def create_th(self):
        find = Counsellor.objects.filter(
            carrer=self.carrerObj, user=self.user)
        if find:
            self.signal = False
            return
        else:
            try:
                Counsellor.objects.create(
                    user=self.user,
                    carrer=self.carrerObj,
                    title=self.data['title'],
                    qualification=self.data['qualification'],
                    mobile=self.data['mobile'],
                    experience=self.data['experience'],
                    college=self.data['college'],
                    designation=self.data['designation'],
                    address=self.data['address'],
                    pincode=self.data['pincode'],
                    area=self.data['area'],
                    aboutUs=self.data['aboutUs'],
                    language=self.data['language'],
                    price=self.data['price'],
                    # dateOfBirth = self.data['dateOfBirth'],
                    gender=self.data['gender'],
                )
                self.signal = True
                return
            except:
                self.signal = False
                return

    def update_th(self):
        try:
            Counsellor.objects.filter(id = self.data['id']).update(
                carrer=self.carrerObj,
                title=self.data['title'],
                qualification=self.data['qualification'],
                mobile=self.data['mobile'],
                experience=self.data['experience'],
                college=self.data['college'],
                designation=self.data['designation'],
                address=self.data['address'],
                pincode=self.data['pincode'],
                area=self.data['area'],
                aboutUs=self.data['aboutUs'],
                language=self.data['language'],
                price=self.data['price'],
                # dateOfBirth = self.data['dateOfBirth'],
                gender=self.data['gender'],
            )
            self.signal = True
            return
        except:
            self.signal = False
            return 

class GetEditorArticleAdminView:
    def __init__(self):
        self.allData = ''
        self.singleData = ''
        self.signal = ''
        Thread.__init__(self)
    
    def get_edi_article_all(self, id, request, check):
        self.allData = views.get_editor_approve_article(id, request, check)
        return
    
    def get_edi_article_single(self, id, request, check):
        self.singleData = views.get_editor_approve_article(id, request, check)
        return
    
    def get_edi_article_delete(self, id, request, check):
        self.signal = views.get_editor_approve_article(id, request, check)
        return
        
    
    def create_th(self, stuId, request):
        data = request.data
        stuIdReturn = views.get_student_featured_article(stuId, request, "id")
        try:
            EditorApproveArticle.objects.create(
                user = request.user,
                studentArticle = stuIdReturn,
                paymentChoices = data['paymentChoices'],
                articleApprove  = data['articleApprove'],
                ammount = data['ammount']
            )
            return True
        except:
            return False

    def update_th(self, id, request):
        data = request.data
        try:
            EditorApproveArticle.objects.filter(id = id).update(
                paymentChoices = data['paymentChoices'],
                articleApprove  = data['articleApprove'],
                ammount = data['ammount']
            )
            return True
        except:
            return False


##=========================================== Api View Class ====================================================##
class StudentArticleAdminViewSet(viewsets.ViewSet):
    # permission_classes = [IsAdminUser]
    # authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        classOj = PostStudentArticle(request)
        st = Thread(target=classOj.all_data_th)
        st.start()
        st.join()
        return Response(classOj.allData)

    def create(self, request):
        classOj = PostStudentArticle(request)
        cr = Thread(target=classOj.create_th)
        cr.start()
        cr.join()
        if classOj.signal == True:
            return Response(status.HTTP_201_CREATED)
        else:
            return Response(status.HTTP_208_ALREADY_REPORTED)

    def retrieve(self, request, pk=None):
        classOj = PostStudentArticle(request)
        sdt = Thread(target=classOj.single_data_th, args=(pk,))
        sdt.start()
        sdt.join()
        return Response(classOj.singleData)
    
    def destroy(self, request, pk=None):
        classOj = PostStudentArticle(request)
        sdt = Thread(target=classOj.delete_data_th, args=(pk,))
        sdt.start()
        sdt.join()
        if classOj.signal == True:
            return Response(status.HTTP_200_OK)


class EditorAdminViewSet(viewsets.ViewSet):
    # permission_classes = [IsAdminUser]
    # authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        classOj = GetEditorArticleAdminView()
        ad = Thread(target=classOj.get_edi_article_all, args=("null", request, "userWise"))
        ad.start()
        ad.join()
        return Response(classOj.allData)

    def create(self, request):
        classOj = GetEditorArticleAdminView()
        stuArtiId = request.data['stuArticleId']
        ct = Thread(target=classOj.create_th, args=(stuArtiId, request))
        ct.start()
        ct.join()
        if classOj.signal == True:
            return Response(status.HTTP_201_CREATED)
        else:
            return Response(status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        classOj = GetEditorArticleAdminView()
        ut = Thread(target=classOj.update_th, args=(pk, request))
        ut.start()
        ut.join()
        if classOj.signal == True:
            return Response(status.HTTP_201_CREATED)
        else:
            return Response(status.HTTP_304_NOT_MODIFIED)
        
    def retrieve(self, request, pk=None):
        classOj = GetEditorArticleAdminView()
        sdt = Thread(target=classOj.get_edi_article_single, args=(pk, request, "userWiseSingleData"))
        sdt.start()
        sdt.join()
        return Response(classOj.singleData)
    
    def destroy(self, request, pk=None):
        classOj = GetEditorArticleAdminView()
        d = Thread(target=classOj.get_edi_article_delete, args=(pk, request, "userWiseDelete"))
        d.start()
        d.join()
        return Response(classOj.singleData)


class CounsellorAdminViewSet(viewsets.ViewSet):
    # permission_classes = [IsAdminUser]
    # authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        classOj = CounsellorRegister(request)
        ct = Thread(target=classOj.all_data_th)
        ct.start()
        ct.join()
        return Response(classOj.allData)
        

    def create(self, request):
        classOj = CounsellorRegister(request)
        ct = Thread(target=classOj.create_th)
        ct.start()
        ct.join()
        if classOj.signal == True:
            return Response(status.HTTP_201_CREATED)
        else:
            return Response(status.HTTP_208_ALREADY_REPORTED)
    
    def update(self, request):
        classOj = CounsellorRegister(request)
        ut = Thread(target=classOj.update_th)
        ut.start()
        ut.join()
        if classOj.signal == True:
            return Response(status.HTTP_201_CREATED)
        else:
            return Response(status.HTTP_304_NOT_MODIFIED)

    def retrieve(self, request, pk=None):
        classOj = CounsellorRegister(request)
        sdt = Thread(target=classOj.single_data_th, args=(pk,))
        sdt.start()
        sdt.join()
        return Response(classOj.singleData)
    
    def destroy(self, request, pk=None):
        classOj = CounsellorRegister(request)
        sdt = Thread(target=classOj.delete_data_th, args=(pk,))
        sdt.start()
        sdt.join()
        if classOj.signal == True:
            return Response(status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
# @authentication_classes([JWTAuthentication])
@api_view(['GET'])
def get_get_carrer_adminView(request):
    if data != '':
        return Response(data)
    id = ""
    check = "all"

    def th(id, check):
        global data
        data = views.get_carrer(id, check)
        return
    t = Thread(target=th, args=(id, check))
    t.start()
    t.join()
    return Response(data)
