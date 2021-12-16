from django.db.models.aggregates import Count
from django.db.models.expressions import F
from django.db.models.query_utils import Q
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from .models import DefineClasses, IndustryCategory, Reports_10th, Questions, Test, DefinedGrate, ShowGrade, GeneralInformation_10th, Interpretation_10th
from .serializer import DefineClassesSerializer, IndustryCategorySerializer, Reports_10thSerializer, TestSerializer, QuestionsSerializer, ShowGradeSerializer, GeneralInformation_10thSerializer

# Create your views here.

saveCount = ""
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
    que = GeneralInformation_10th.objects.all()
    serializer = GeneralInformation_10thSerializer(que, many=True)
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
    global saveCount

    testV = Reports_10th.objects.filter(Q(industry=indData), Q(user=user))
    
    if testV:
        course_qs = testV
        for course in course_qs:
            VID = course.id
        getUpdate = Reports_10th.objects.get(id=VID)
        if saveCount == 1:
            CW = getUpdate.totalCount + 1
        else:
            CW = getUpdate.totalCount + 0

        # print('................. Ans Count', countValue)
        # print('................. Now Count', getUpdate.totalCount)
        # print('................. Total Count', CW)
        myGrade = ''
        obj = (
            DefinedGrate.objects.filter(one=CW) or DefinedGrate.objects.filter(two=CW) 
            or DefinedGrate.objects.filter(three=CW) or DefinedGrate.objects.filter(four=CW) 
            or DefinedGrate.objects.filter(five=CW) or DefinedGrate.objects.filter(six=CW) 
            or DefinedGrate.objects.filter(seven=CW) or DefinedGrate.objects.filter(eight=CW) 
            or DefinedGrate.objects.filter(nine=CW) or DefinedGrate.objects.filter(ten=CW)
        )
        for i in obj:
            myGrade = i.grade
            interp = Interpretation_10th.objects.filter(grade = myGrade)
            for k in interp:
                interp_Id = k.id

        industryValue = IndustryCategory.objects.filter(industry=indData)
        for i in industryValue:
            industry_Grade = i.industry_Id
            Reports_10th.objects.filter(pk=VID).update(interpretatio = interp_Id,totalCount=CW, grade=myGrade, industry_Grade=industry_Grade)
            saveCount = ""
    else:
        if saveCount == 1:
            query = Reports_10th.objects.create(
                user = user,
                industry = data['industry'],
                question = data['question'],
                a = 1,
                b = data['ans2'],
                c = data['ans3'],
                d = data['ans4'],
                e = data['ans5'],
            )
        else:
            query = Reports_10th.objects.create(
                user = user,
                industry = data['industry'],
                question = data['question'],
                a = 0,
                b = data['ans2'],
                c = data['ans3'],
                d = data['ans4'],
                e = data['ans5'],
            )
        query.save()
        serializer = Reports_10thSerializer(query, many=False)
        context = {'data':serializer.data, 'status':status.HTTP_201_CREATED}
        return Response(context)
    return Response("error")



# @api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# # @permission_classes([IsAdminUser])
# def getResult(request):
#     user = request.user
#     tickets = Reports_10th.objects.filter(Q(user=user)).annotate(total_price=F('totalCount'))
#     countIndstry = Reports_10th.objects.filter(Q(user=user)).count()
#     # print(countIndstry)
#     to = []
#     for t in tickets:
#         p = t.total_price
#         to.append(p)
#     #     print(t.total_price)
#     # print(to)
#     totalAmmount = sum(to)
#     serializer = Reports_10thSerializer(tickets, many=True)
#     context = {'data':serializer.data, 'ind_1':totalAmmount, "countIndustry": countIndstry}
#     # p = TestResult.objects.filter(user=user).delete()
#     return Response(context)


from django.core.mail.message import EmailMultiAlternatives
from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
from django.conf import settings
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@permission_classes([IsAdminUser])
def getResult(request):
    user = request.user
    data = Reports_10th.objects.filter(Q(user=user)).annotate(total_price=F('totalCount'))
    data2 = ShowGrade.objects.all()
    # print('...............', data2)
    # data3 = GeneralInformation_9th.objects.all()
    context = {"mylist": data, "mylist1": data2}
    template = get_template('Test_10th/mytemplate.html')
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
    countIndstry = Reports_10th.objects.filter(Q(user=user)).count()
    # print(countIndstry)
    to = []
    for t in data:
        p = t.total_price
        to.append(p)
    #     print(t.total_price)
    # print(to)
    totalAmmount = sum(to)
    serializer = Reports_10thSerializer(data, many=True)
    context = {'data':serializer.data, 'ind_1':totalAmmount, "countIndustry": countIndstry}
    # p = TestResult.objects.filter(user=user).delete()
    return Response(context)




@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delReuslt(request):
    user = request.user
    Reports_10th.objects.filter(user=user).delete()
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


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def findRightAns(request):
    data = request.data
    _id = data['id']
    value = data['value']
    obj = Questions.objects.get(id=_id)
    curans = obj.rightAns
    op = curans == value
    if op:
        global saveCount
        saveCount = 1
        return Response({"message":"Right Ans!", "status":status.HTTP_200_OK})
    else:
        saveCount = 0
        return Response({"message":"Opps Wrong!", "status":status.HTTP_400_BAD_REQUEST})
    

    