from django.db.models.aggregates import Count
from django.db.models.expressions import F
from django.db.models.query_utils import Q
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from .models import  IndustryCategory, Interpretation_6th, Reports, Questions, Test, DefinedGrate, ShowGrade, GeneralInformation_6th
from .serializer import IndustryCategorySerializer, ReportsSerializer, TestSerializer, QuestionsSerializer, ShowGradeSerializer, GeneralInformation_6thSerializer


# Create your views here.
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def getStudent(request):
    count = Questions.objects.filter().count()
    que = Test.objects.all()
    serializer = TestSerializer(que, many=True)
    context = {'count':count, 'data':serializer.data}
    return Response(context)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def getTitle(request):
    que = GeneralInformation_6th.objects.all()
    serializer = GeneralInformation_6thSerializer(que, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getQuestion(request):
    paginator = PageNumberPagination()
    paginator.page_size = 1
    que = Questions.objects.all()
    result_page = paginator.paginate_queryset(que, request)
    serializer = QuestionsSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def testResult(request):
    data = request.data
    user = request.user
    indData = data['industry']

    testV = Reports.objects.filter(Q(industry=indData), Q(user=user))

    if testV:
        course_qs = testV
        for course in course_qs:
            VID = course.id
        countValue = (data['ans1'] + data['ans2'] + data['ans3'] + data['ans4'] + data['ans5'])
        getUpdate = Reports.objects.get(id=VID) 
        CW = getUpdate.totalCount + countValue

        # print('................. Ans Count', countValue)
        # print('................. Now Count', getUpdate.totalCount)
        # print('................. Total Count', CW)
        myGrade = ''
        interp_Id = ''
        obj = DefinedGrate.objects.filter(one=CW) or DefinedGrate.objects.filter(two=CW) or DefinedGrate.objects.filter(three=CW) or DefinedGrate.objects.filter(four=CW) or DefinedGrate.objects.filter(five=CW) or DefinedGrate.objects.filter(six=CW) or DefinedGrate.objects.filter(seven=CW) or DefinedGrate.objects.filter(eight=CW) or DefinedGrate.objects.filter(nine=CW) or DefinedGrate.objects.filter(ten=CW)
        for i in obj:
            myGrade = i.grade

        interp = Interpretation_6th.objects.filter(grade = myGrade)
        for k in interp:
            interp_Id = k.id

        industryValue = IndustryCategory.objects.filter(industry=indData)
        for i in industryValue:
            industry_Grade = i.industry_Id
            
        Reports.objects.filter(pk=VID).update(interpretatio = interp_Id, totalCount=CW, grade=myGrade, industry_Grade=industry_Grade)
    else:
        query = Reports.objects.create(
            user = user,
            industry = data['industry'],
            question = data['question'],
            ans1 = data['ans1'],
            ans2 = data['ans2'],
            ans3 = data['ans3'],
            ans4 = data['ans4'],
            ans5 = data['ans5'],
        )
        query.save()
        serializer = ReportsSerializer(query, many=False)
        context = {'data':serializer.data, 'status':status.HTTP_201_CREATED}
        return Response(context)
    return Response("error")


from django.core.mail.message import EmailMultiAlternatives
from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@permission_classes([IsAdminUser])
def getResult(request):
    user = request.user
    data = Reports.objects.filter(Q(user=user)).annotate(total_price=F('totalCount'))
    data2 = ShowGrade.objects.all()
    data3 = GeneralInformation_6th.objects.all()
    context = {"mylist": data, "mylist1": data2, 'mylist3': data3}
    template = get_template('Test_6To9/mytemplate.html')
    html  = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
    pdf = result.getvalue()
    filename = 'Result.pdf'
    mail_subject = 'Recent Result'
    message  = "this is test result"
    # to_email = order_db.user.email
    to_email = user.email
    email = EmailMultiAlternatives(
                        mail_subject,
                        "hello",       # necessary to pass some message here
                        settings.EMAIL_HOST_USER,
                        [to_email]
                    )
    email.attach_alternative(message, "text/html")
    email.attach(filename, pdf, 'application/pdf')
    email.send(fail_silently=False)
    countIndstry = Reports.objects.filter(Q(user=user)).count()
    # print(countIndstry)
    to = []
    for t in data:
        p = t.total_price
        to.append(p)
    #     print(t.total_price)
    # print(to)
    totalAmmount = sum(to)
    serializer = ReportsSerializer(data, many=True)
    context = {'data':serializer.data, 'ind_1':totalAmmount, "countIndustry": countIndstry}
    # p = TestResult.objects.filter(user=user).delete()
    return Response(context)




# @permission_classes([IsAuthenticated])
# def getResult(request):
#     user = request.user
#     data = Reports.objects.filter(Q(user=user))
#     data2 = ShowGrade.objects.all()
#     data3 = GeneralInformation_6th.objects.all()
#     context = {"mylist": data, "mylist1": data2, 'mylist3': data3}
#     template = get_template('Test_6To9/mytemplate.html')
#     html  = template.render(context)
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
#     pdf = result.getvalue()
#     filename = 'Result.pdf'
#     mail_subject = 'Recent Result'
#     message  = "this is test result"
#     # to_email = order_db.user.email
#     to_email = "visheshsolanki12345@gmail.com"
#     email = EmailMultiAlternatives(
#                         mail_subject,
#                         "hello",       # necessary to pass some message here
#                         settings.EMAIL_HOST_USER,
#                         [to_email]
#                     )
#     email.attach_alternative(message, "text/html")
#     email.attach(filename, pdf, 'application/pdf')
#     email.send(fail_silently=False)
#     return render(request, 'Test_6To9/mytemplate.html',context )


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delReuslt(request):
    user = request.user
    Reports.objects.filter(user=user).delete()
    return Response("Successsfully Data Deleted")


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def showGrade(request):
    que = ShowGrade.objects.all()
    serializer = ShowGradeSerializer(que, many=True)
    return Response(serializer.data)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def showIndustry(request):
    que = IndustryCategory.objects.all()
    serializer = IndustryCategorySerializer(que, many=True)
    return Response(serializer.data)