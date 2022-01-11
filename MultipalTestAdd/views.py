from django.db.models.aggregates import Count
from django.db.models.query_utils import Q
from rest_framework import serializers, status
from rest_framework import response
from rest_framework.fields import MultipleChoiceField, empty
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from .PayTm import Checksum
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Sum
import uuid

from .models import (
    Career, NewClass, ResultTitle, SelectNumber, ShowGrade, Section, Interpretation, TestBackupOneQuizeCorrect, Title,
     ImageOptionsTest, OneOptionsTest, Reports, 
    OptionsTest, AddTest, TestCategory, ThreeOptionsTest, FiveOptionsTest,TestBackupOneImageQuizeCorrect, PaymentHistory,
    TestBackupMultipalQuize, TestBackupFiveQuize, TestBackupThreeQuize
    )

from .serializer import (
    AddTestSerializer, FiveOptionsTestSerializer, ImageOptionsTestSerializer, 
    NewClassSerializer, OneOptionsTestSerializer, OptionsTestSerializer, ResultTitleSerializer, TestBackupFiveQuizeSerializer, 
    TestBackupMultipalQuizeSerializer, TestBackupOneImageQuizeCorrectSerializer, TestBackupOneQuizeCorrectSerializer, 
    TestBackupThreeQuizeSerializer, ThreeOptionsTestSerializer, TitleSerializer,
    ReportsSerializer,ShowGradeSerializer, InterpretationSerializer
)


# # Create your views here.
oneOption = 'One Quiz Correct Test'
imageTest = "One Images Quiz Correct Test"
allOption = "Mulitpal Quiz Select Test"
threeOption = "Three Quiz Test"
fiveOption = "Five Quiz Test"


@api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
def testSelect(request):
    que = NewClass.objects.all()
    serializer = NewClassSerializer(que, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def testInfo(request):
    data = request.data
    user = request.user
    filterByClass = data['id']
    typeTest = ''
    Class = ''
    signal = ''

    if filterByClass == None:
        return Response(status.HTTP_404_NOT_FOUND)
    
    dis = AddTest.objects.filter(className = filterByClass)
    for i in dis:
        typeTest = i.typeOfTest.selectTest
        Class = i.className.newClass

    try:
        obj = PaymentHistory.objects.filter(user = user, typeOfTest = typeTest, Class = Class).latest('paymentCount')
        if obj:
            if obj.paymentCount == '1':
                signal = "201"
    except:
        pass

    serializers = AddTestSerializer(dis, many=True)
    context = {"discreption" : serializers.data, "signal" : signal}
    return Response(context)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def paymentAndTest(request):
    user = request.user
    data = request.data
    filterByClass = data['id']
    typeTest = ''
    Class = ''
    Amount = ''

    if filterByClass == None:
        return Response(status.HTTP_404_NOT_FOUND)

    dis = AddTest.objects.filter(className = filterByClass)
    for i in dis:
        typeTest = i.typeOfTest.selectTest
        Class = i.className.newClass
        Amount = i.title.price
    try:
        obj = PaymentHistory.objects.filter(user = user, typeOfTest = typeTest, Class = Class).latest('paymentCount')
        if obj:
            if obj.paymentCount == '1':
                    testData = testFunc(typeTest, dis)
                    return Response(testData)
            else:
                payFuncObj = PaytemFunc(str(uuid.uuid4()), str(Amount) ,user.email, user, typeTest, Class)
                return Response(payFuncObj)
    except:
        pass
    payFuncObj = PaytemFunc(str(uuid.uuid4()), str(Amount) ,user.email, user, typeTest, Class)
    return Response(payFuncObj)



def PaytemFunc(orderId, amount, userEmail, user, typeOfTest, Class):
    param_dict={
        'MID': settings.PAYTEM_MID,
        'ORDER_ID': orderId,
        'TXN_AMOUNT': amount,
        'CUST_ID': userEmail,
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': 'WEBSTAGING',
        'CHANNEL_ID': 'WEB',
        'CALLBACK_URL':'http://127.0.0.1:8000/api/handlepayment/',
        # 'CALLBACK_URL':'https://visheshsolanki.pythonanywhere.com/api/handlepayment/',
    }
    PaymentHistory.objects.create(
        user = user, 
        ORDER_ID = orderId, 
        TXN_AMOUNT = amount, 
        typeOfTest = typeOfTest, 
        Class = Class,
        email = userEmail,
    )
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, settings.PAYTEM_MERCHANT_KEY)
    return param_dict
    

@csrf_exempt
@api_view(['POST', 'GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
def HandlePaytemRequest(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    try:
        verify = Checksum.verify_checksum(response_dict, settings.PAYTEM_MERCHANT_KEY, checksum)
        if verify:
            PaymentHistory.objects.filter(ORDER_ID = response_dict['ORDERID']).update(
                gateway=response_dict['GATEWAYNAME'],
                bankname=response_dict['BANKNAME'], 
                TXNID=response_dict['TXNID'], 
                status=response_dict['STATUS'], 
                TXNDATE=response_dict['TXNDATE'],
                RESPCODE=response_dict['RESPCODE'],
                CURRENCY=response_dict['CURRENCY'],
                PAYMENTMODE=response_dict['PAYMENTMODE'],
                MID=response_dict['MID'],
                paymentCount = '1',
            )
            if response_dict['RESPCODE'] == '01':
                print('order successful')
                # url = "https://my-guru-test.herokuapp.com/paymentassessment"
                url = "http://localhost:3000/paymentassessment"
                return redirect(url)
            else:
                print('order was not successful because' + response_dict['RESPMSG'])
                return Response(status.HTTP_304_NOT_MODIFIED)
        return Response(status.HTTP_304_NOT_MODIFIED)
    except:
        return Response(status.HTTP_304_NOT_MODIFIED)
##============================== End... ================================##


def testFunc(typeTest, dis):
    context = {}
    try:
        discreption = AddTestSerializer(dis, many=True)
        if typeTest == oneOption:
            que = OneOptionsTest.objects.all()
            serializer = OneOptionsTestSerializer(que, many=True)
            context = {'data':serializer.data, 'discreption':discreption.data}
            return context

        elif typeTest == imageTest:
            que = ImageOptionsTest.objects.all()
            serializer = ImageOptionsTestSerializer(que, many=True)
            context = {'data':serializer.data, 'discreption':discreption.data}
            return context

        elif typeTest == allOption:
            que = OptionsTest.objects.all()
            serializer = OptionsTestSerializer(que, many=True)
            context = {'data':serializer.data, 'discreption':discreption.data}
            return context

        elif typeTest == threeOption:
            que = ThreeOptionsTest.objects.all()
            serializer = ThreeOptionsTestSerializer(que, many=True)
            context = {'data':serializer.data, 'discreption':discreption.data}
            return context

        elif typeTest == fiveOption:
            que = FiveOptionsTest.objects.all()
            serializer = FiveOptionsTestSerializer(que, many=True)
            context = {'data':serializer.data, 'discreption':discreption.data}
            return context
        return Response("No test")
    except:
        Response("Error")


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def testBackup(request):
    user = request.user
    data = request.data

    typeTest = data["typeOfTest"]
    Class = data['Class']
    section = data['section']
    question = data['question']
    object = data['obj']
    lastTime = data['lastTime']


    testID = ''
    sectionID = ''
    questionID = ''
    classID = ''
    addTestID = ''

    classType = NewClass.objects.filter(newClass = Class)
    for i in classType:
        classID = i.id 

    testType = TestCategory.objects.filter(selectTest = typeTest)
    for i in testType:
        testID = i.id

    sectionType = Section.objects.filter(section = section)
    for i in sectionType:
        sectionID = i.id
    
    testAdd = AddTest.objects.filter(className = classID, typeOfTest = testID)
    for i in testAdd:
        addTestID = i.id

    if typeTest == oneOption:
        que = OneOptionsTest.objects.filter(section=sectionID, question=question)
        for i in que:
            upBackup = TestBackupOneQuizeCorrect.objects.filter(user = user ,className = classID, oneQuizeCorrect = i.id)
            if upBackup:
                upBackup.update(userClickObj = object)
                return Response("ok")
            op = TestBackupOneQuizeCorrect.objects.create(user = user, userClickObj = object)
            TestBackupOneQuizeCorrect.objects.filter(id=op.id).update(
                typeOfTest = testID,
                className = classID,
                oneQuizeCorrect = i.id,
                testDiscription = addTestID,
                lastTime = lastTime,
                )
            return Response("ok")

    elif typeTest == imageTest:
        qu = question.split("/media/")
        que = ImageOptionsTest.objects.filter(section=sectionID, question=qu[1])
        for i in que:
            upBackup = TestBackupOneImageQuizeCorrect.objects.filter(user = user ,className = classID, imageOneQuizeCorrect = i.id)
            if upBackup:
                upBackup.update(userClickObj = object)
                return Response("ok")
            op = TestBackupOneImageQuizeCorrect.objects.create(user = user, userClickObj = object)
            TestBackupOneImageQuizeCorrect.objects.filter(id=op.id).update(
                typeOfTest = testID,
                className = classID,
                imageOneQuizeCorrect = i.id,
                testDiscription = addTestID,
                lastTime = lastTime,
                )
            return Response("ok")

    elif typeTest == allOption:
        que = OptionsTest.objects.filter(section=sectionID, question=question)
        for i in que:
            upBackup = TestBackupMultipalQuize.objects.filter(user = user ,className = classID, multipalQuize = i.id, userClickObj=object)
            if upBackup:
                upBackup.delete()
                return Response("ok")
            op = TestBackupMultipalQuize.objects.create(user = user, userClickObj = object)
            TestBackupMultipalQuize.objects.filter(id=op.id).update(
                typeOfTest = testID,
                className = classID,
                multipalQuize = i.id,
                testDiscription = addTestID,
                lastTime = lastTime,
                )
            return Response("ok")
    elif typeTest == fiveOption:
        que = FiveOptionsTest.objects.filter(section=sectionID, question=question)
        for i in que:
            upBackup = TestBackupFiveQuize.objects.filter(user = user ,className = classID, fiveQuize = i.id)
            if upBackup:
                upBackup.update(userClickObj = object)
                return Response("ok")
            op = TestBackupFiveQuize.objects.create(user = user, userClickObj = object)
            TestBackupFiveQuize.objects.filter(id=op.id).update(
                typeOfTest = testID,
                className = classID,
                fiveQuize = i.id,
                testDiscription = addTestID,
                lastTime = lastTime,
                )
            return Response("ok")
            
    elif typeTest == threeOption:
        que = ThreeOptionsTest.objects.filter(section=sectionID, question=question)
        for i in que:
            upBackup = TestBackupThreeQuize.objects.filter(user = user ,className = classID, threeQuize = i.id)
            if upBackup:
                upBackup.update(userClickObj = object)
                return Response("ok")
            op = TestBackupThreeQuize.objects.create(user = user, userClickObj = object)
            TestBackupThreeQuize.objects.filter(id=op.id).update(
                typeOfTest = testID,
                className = classID,
                threeQuize = i.id,
                testDiscription = addTestID,
                lastTime = lastTime,
                )
            return Response("ok")

    else:
        return Response("not found question")
    

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def backupGet(request):
    user = request.user
    data = request.data
    typeTest = data["typeOfTest"]
    Class = data['Class']

    if Class == None or typeTest == None:
        return Response(status.HTTP_404_NOT_FOUND)

    classID = ''

    classType = NewClass.objects.filter(newClass = Class)
    for i in classType:
        classID = i.id 

    if typeTest == oneOption:
        que = TestBackupOneQuizeCorrect.objects.filter(user = user ,className = classID)
        serializer = TestBackupOneQuizeCorrectSerializer(que, many=True)
        return Response(serializer.data)

    elif typeTest == imageTest:
        que = TestBackupOneImageQuizeCorrect.objects.filter(user = user ,className = classID)
        serializer = TestBackupOneImageQuizeCorrectSerializer(que, many=True)
        return Response(serializer.data)

    elif typeTest == allOption:
        que = TestBackupMultipalQuize.objects.filter(user = user ,className = classID)
        serializer = TestBackupMultipalQuizeSerializer(que, many=True)
        return Response(serializer.data)

    elif typeTest == threeOption:
        que = TestBackupThreeQuize.objects.filter(user = user ,className = classID)
        serializer = TestBackupThreeQuizeSerializer(que, many=True)
        return Response(serializer.data)

    elif typeTest == fiveOption:
        que = TestBackupFiveQuize.objects.filter(user = user ,className = classID)
        serializer = TestBackupFiveQuizeSerializer(que, many=True)
        return Response(serializer.data)
    

@api_view(['GET'])
# @authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def ResultGenerator(request):
    user = request.user
    data = request.data
    # typeOfTest = data["typeOfTest"]
    # Class = data['Class']

    typeOfTest = threeOption
    Class = '6'

    classID = ''

    context = {}
    countNo = []
    sec = ''
    classType = NewClass.objects.filter(newClass = Class)
    for i in classType:
        classID = i.id
         
    if typeOfTest == threeOption:
        que = TestBackupThreeQuize.objects.filter(user = user ,className = classID)
        for i in que:
            if i.threeQuize.section:
                if i.threeQuize.a:
                    context[i.threeQuize.section] = 1
                    # countNo.append(1)
                if i.threeQuize.b:
                    # countNo.append(1)
                    context[i.threeQuize.section] = 1
                if i.threeQuize.c:
                    # countNo.append(1)
                    context[i.threeQuize.section] = 1
                    # sec = i.threeQuize.section
            
    return Response("ok")
     
        

    # if typeOfTest == oneOption:
    #     que = TestBackupOneQuizeCorrect.objects.filter(user = user ,className = classID)
    #     serializer = TestBackupOneQuizeCorrectSerializer(que, many=True)
    #     return Response(serializer.data)

    # elif typeOfTest == imageTest:
    #     que = TestBackupOneImageQuizeCorrect.objects.filter(user = user ,className = classID)
    #     serializer = TestBackupOneImageQuizeCorrectSerializer(que, many=True)
    #     return Response(serializer.data)

    # elif typeOfTest == allOption:
    #     que = TestBackupMultipalQuize.objects.filter(user = user ,className = classID)
    #     serializer = TestBackupMultipalQuizeSerializer(que, many=True)
    #     return Response(serializer.data)


    # elif typeOfTest == fiveOption:
    #     que = TestBackupFiveQuize.objects.filter(user = user ,className = classID)

    


def CountSum(typeOfTest):
    countNo = []
    if typeOfTest == allOption:
        myObj = OptionsTest.objects.filter()
        for i in myObj:
            if i.a:
                countNo.append(1)
            if i.b:
                 countNo.append(1)
            if i.c:
                 countNo.append(1)
            if i.d:
                 countNo.append(1)
            if i.e:
                 countNo.append(1)
            else:
                continue
    if typeOfTest == fiveOption:
        myObj = FiveOptionsTest.objects.filter()
        for i in myObj:
            if i.a:
                countNo.append(1)
            if i.b:
                 countNo.append(1)
            if i.c:
                 countNo.append(1)
            if i.d:
                 countNo.append(1)
            if i.e:
                 countNo.append(1)
            else:
                continue
    if typeOfTest == threeOption:
        myObj = ThreeOptionsTest.objects.filter()
        for i in myObj:
            if i.a:
                countNo.append(1)
            if i.b:
                 countNo.append(1)
            if i.c:
                 countNo.append(1)
            else:
                continue
    if typeOfTest == oneOption:
        pass

    if typeOfTest == imageTest:
        pass
    return sum(countNo)


def convertTuple(tup):
    str = ''
    for item in tup:
        str = str + item
    return str


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def saveResult(request):
    user = request.user
    data = request.data

    typeOfTest = data["typeOfTest"]
    Class = data['Class']
    section = data['section']
    question = data['question']
    marks = data['marks']
    classID = ''
    secID = ''

    # print(typeOfTest)
    # print(Class)
    # print(section)
    # print(question)
    # print(marks)

    if Class == None or typeOfTest == None:
        return Response(status.HTTP_404_NOT_FOUND)

    secObj = Section.objects.filter(section = section)
    for i in secObj:
        secID = i.id

    classObj = NewClass.objects.filter(newClass = Class)
    for i in classObj:
        classID = i.id
    
    sec = Section.objects.filter(section=section)
    for i in sec:
        secID = i.id
    
    try:
        carrer = data['carrer']
    except:
        carrer = 'null'
    context = {}
    totalMarks = marks

    
    obj = Reports.objects.filter(user=user, Class=Class, section=section, typeOftest=typeOfTest) or Reports.objects.filter(user=user, Class=Class, section=section, typeOftest=typeOfTest, question = question)
    if obj:  
        for i in obj:
            totalMarks = i.totalCount + int(marks)
    setSignal = ''
    que = ShowGrade.objects.filter(className = classID, section = secID)
    for i in que:
        context = i.the_json
    for key in context:
        p = f"{key}, {context[key]}"
        str = convertTuple(p)
        f = str.split('-')[0]
        grade = f.split(',')[0]
        first = f.split(',')[1]
        second = str.split('-')[1]
        array = []
        x = range(int(first), int(second), 1)
        for n in x:
            array.append(n)
            lastV = array[-1]
        array.append(lastV+1)
        nu = int(totalMarks)

        if nu in array:
            array = []
            obj = Reports.objects.filter(user=user, Class=Class, section=section, typeOftest=typeOfTest) or Reports.objects.filter(user=user,Class=Class, section=section, question=question, typeOftest=typeOfTest)
            if obj: 
                for i in obj:
                    _id = i.id
               
                    in_idd = ''
                    interp = Interpretation.objects.filter(className = classID, section = secID)
                    serializer = InterpretationSerializer(interp, many=True)
                    for i in serializer.data:
                        in_idd = i['id']
                        if Class in dict(i['className']).values():
                            if section in dict(i['section']).values():
                                try:
                                    grade in dict(i['selectGrade']).values()
                                    setSignal = 1
                                    break
                                except:
                                    setSignal = 1
                                    break
                        else:
                            continue
                    if setSignal == 1:
                        Reports.objects.filter(id = _id).update(totalCount = totalMarks, grade = grade, interpretatio = in_idd)
                        setSignal = ''
                        return Response("Update")
                    else:
                        Reports.objects.filter(id = _id).update(totalCount = totalMarks, grade = grade)
                        return Response("Update")
            else:
                in_id = ''
                interp = Interpretation.objects.filter(className = classID, section = secID)
                serializer = InterpretationSerializer(interp, many=True)
     
                for i in serializer.data:
                    in_id = i['id']
                    if Class in dict(i['className']).values():
                        if section in dict(i['section']).values():                        
                            try:
                                grade in i['the_json'].values()
                                setSignal = 1
                                break
                            except:
                                setSignal = 1
                                break
                    else:
                        continue
                # secID = ''
                testID = ''
                noID = ''
                carrerID = ''
                countNO = []
                toQuCount = ''
                myArray = []
                if typeOfTest == allOption:
                    toQuCount = OptionsTest.objects.filter(section = secID).count()
                    NoCo = OptionsTest.objects.filter(section = secID)
                    for i in NoCo:
                        myArray.append(i.a)
                        myArray.append(i.b)
                        myArray.append(i.c)
                        if i.d:
                            myArray.append(i.d)
                        if i.e:
                            myArray.append(i.e)
                elif typeOfTest == imageTest:
                    toQuCount = ImageOptionsTest.objects.filter(section = secID).count()
                elif typeOfTest == oneOption:
                    toQuCount = OneOptionsTest.objects.filter(section = secID).count()
                elif typeOfTest == threeOption:
                    toQuCount = ThreeOptionsTest.objects.filter(section = secID).count()
                elif typeOfTest == fiveOption:
                    toQuCount = FiveOptionsTest.objects.filter(section = secID).count()

                typeTest = TestCategory.objects.filter(selectTest=typeOfTest)
                for i in typeTest:
                    testID = i.id


                newTest = AddTest.objects.filter(className=classID, typeOfTest=testID)
                for i in newTest:
                    noID = i.selectNumber.id
                
                noSum = CountSum(typeOfTest)
                noObj = SelectNumber.objects.filter(id=noID)
                for i in noObj:
                    if typeOfTest == allOption:
                        countNO.append(i.a)
                        countNO.append(i.b)
                        countNO.append(i.c)
                        countNO.append(i.d)
                        countNO.append(i.e)

                    elif typeOfTest == threeOption:
                        countNO.append(i.a)
                        countNO.append(i.b)
                        countNO.append(i.c)

                    elif typeOfTest == fiveOption:
                        countNO.append(i.a)
                        countNO.append(i.b)
                        countNO.append(i.c)
                        countNO.append(i.d)
                        countNO.append(i.e)

                    elif typeOfTest == oneOption:
                        countNO.append(i.rightAns)

                    elif typeOfTest == imageTest:
                        countNO.append(i.rightAns)


                if typeOfTest == fiveOption:
                    noSum = max(countNO) * toQuCount
                
                if typeOfTest == allOption:
                    mul = sum(countNO) * len(myArray)
                    noSum = mul / len(countNO)

                elif typeOfTest == threeOption:
                    noSum = max(countNO) * toQuCount
                
                elif typeOfTest == imageTest:
                    noSum = max(countNO) * toQuCount
                
                elif typeOfTest == oneOption:
                    noSum = max(countNO) * toQuCount
                
                if carrer != 'null':
                    obj = Career.objects.filter(newCareer = carrer)
                    for i in obj:
                        carrerID = i.id
                if setSignal == 1:
                    opj = Reports.objects.create(user=user,Class=Class, section=section, question=question, grade=grade, totalCount=marks, industry_Grade=secID, typeOftest=typeOfTest, totalNoQu = noSum)
                    if opj:
                        Reports.objects.filter(id = opj.id).update(interpretatio = in_id, carrer = carrerID)
                    setSignal = ''
                else:
                    opj = Reports.objects.create(user=user, Class=Class, section=section, question=question, grade=grade, totalCount=marks, industry_Grade=secID, typeOftest=typeOfTest, totalNoQu = noSum)
                    if obj:
                        Reports.objects.filter(id = opj.id).update(interpretatio = in_id, carrer = carrerID)
            break
        else:
            continue
    return Response("ok")



@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
# @permission_classes([IsAdminUser])
def getResult(request):
    user = request.user
    data = request.data
    typeOfTest = data["typeOfTest"]
    Class = data['Class']

    if Class == None or typeOfTest == None:
        return Response(status.HTTP_404_NOT_FOUND)

    if typeOfTest == allOption:
        que = Reports.objects.filter(user=user, Class = Class, typeOftest = typeOfTest)
        serializer = ReportsSerializer(que, many=True)
        return Response(serializer.data)
    if typeOfTest == imageTest:
        que = Reports.objects.filter(user=user, Class = Class, typeOftest = typeOfTest)
        serializer = ReportsSerializer(que, many=True)
        return Response(serializer.data)
    if typeOfTest == oneOption:
        que = Reports.objects.filter(user=user, Class = Class, typeOftest = typeOfTest)
        serializer = ReportsSerializer(que, many=True)
        return Response(serializer.data)
    if typeOfTest == threeOption:
        que = Reports.objects.filter(user=user, Class = Class, typeOftest = typeOfTest)
        serializer = ReportsSerializer(que, many=True)
        return Response(serializer.data)
    if typeOfTest == fiveOption:
        que = Reports.objects.filter(user=user, Class = Class, typeOftest = typeOfTest)
        serializer = ReportsSerializer(que, many=True)
        return Response(serializer.data)
    # data2 = ShowGrade.objects.all()
    # context = {"mylist": data, "mylist1": data2}
    # try:
    #     pdfGenMail(context, user.email)
    # except:
    #     pass
    return Response("error")



@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delReuslt(request):
    user = request.user
    data = request.data
    typeOfTest = data["typeOfTest"]
    Class = data['Class']

    if Class == None or typeOfTest == None:
        return Response(status.HTTP_404_NOT_FOUND)
        
    if typeOfTest == allOption:
        Reports.objects.filter(user=user, Class = Class, typeOftest = typeOfTest).delete()
        return Response("Successsfully Data Deleted")
    elif typeOfTest == imageTest:
        Reports.objects.filter(user=user, Class = Class, typeOftest = typeOfTest).delete()
        return Response("Successsfully Data Deleted")
    elif typeOfTest == oneOption:
        Reports.objects.filter(user=user, Class = Class, typeOftest = typeOfTest).delete()
        return Response("Successsfully Data Deleted")
    elif typeOfTest == threeOption:
        Reports.objects.filter(user=user, Class = Class, typeOftest = typeOfTest).delete()
        return Response("Successsfully Data Deleted")
    elif typeOfTest == fiveOption:
        Reports.objects.filter(user=user, Class = Class, typeOftest = typeOfTest).delete()
        return Response("Successsfully Data Deleted")
    else:
        return Response("No Report any test")



@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delBackup(request):
    user = request.user
    data = request.data
    typeOfTest = data["typeOfTest"]
    Class = data['Class']

    if Class == None or typeOfTest == None:
        return Response(status.HTTP_404_NOT_FOUND)

    typeTestID = ''
    classID = ''
    obj = TestCategory.objects.filter(selectTest = typeOfTest)
    for i in obj:
        typeTestID = i.id
    objClass = NewClass.objects.filter(newClass = Class)
    for i in objClass:
        classID = i.id

    if typeOfTest == allOption:
        TestBackupMultipalQuize.objects.filter(user=user, typeOfTest = typeTestID, className = classID).delete()
        return Response("Successsfully backup Delted")
    elif typeOfTest == imageTest:
        TestBackupOneImageQuizeCorrect.objects.filter(user=user, typeOfTest = typeTestID, className = classID).delete()
        return Response("Successsfully backup Delted")
    elif typeOfTest == oneOption:
        TestBackupOneQuizeCorrect.objects.filter(user=user, typeOfTest = typeTestID, className = classID).delete()
        return Response("Successsfully backup Delted")
    elif typeOfTest == threeOption:
        TestBackupThreeQuize.objects.filter(user=user, typeOfTest = typeTestID, className = classID).delete()
        return Response("Successsfully backup Delted")
    elif typeOfTest == fiveOption:
        TestBackupFiveQuize.objects.filter(user=user, typeOfTest = typeTestID, className = classID).delete()
        return Response("Successsfully backup Delted")
    return Response("error")


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def pandingTest(request):
    user = request.user
    context = {}
    allOption = TestBackupMultipalQuize.objects.filter(user=user)
    if allOption:
        for i in allOption:
            context[i.className.id] = i.className.newClass

    imageTest = TestBackupOneImageQuizeCorrect.objects.filter(user=user)
    if imageTest:
        for i in imageTest:
            context[i.className.id] = i.className.newClass

    oneOption = TestBackupOneQuizeCorrect.objects.filter(user=user)
    if oneOption:
        for i in oneOption:
            context[i.className.id] = i.className.newClass

    threeOption = TestBackupThreeQuize.objects.filter(user=user)
    if threeOption:
        for i in threeOption:
            context[i.className.id] = i.className.newClass

    fiveOption = TestBackupFiveQuize.objects.filter(user=user)
    if fiveOption:
        for i in fiveOption:
            context[i.className.id] = i.className.newClass

    return Response(context)




@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def buyTest(request):
    user = request.user
    testID = ""
    classID = ""

    objPayment = PaymentHistory.objects.filter(user = user)
    if objPayment:
        context = {}
        for i in objPayment:
            if str(i.paymentCount) == str(1):
                typeTest = TestCategory.objects.filter(selectTest=i.typeOfTest)
                for p in typeTest:
                    testID = p.id
                classTest = NewClass.objects.filter(newClass=i.Class)
                for k in classTest:
                    classID = k.id
                addTestobj = AddTest.objects.filter(typeOfTest = testID, className = classID)
                for m in addTestobj:
                    context[m.className.id] = m.className.newClass
        return Response(context)
    return Response("No buy test available")


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def paymentDecriment(request):
    user = request.user
    data = request.data
    typeOfTest = data["typeOfTest"]
    Class = data['Class']

    if Class == None or typeOfTest == None:
        return Response(status.HTTP_404_NOT_FOUND)

    obj = PaymentHistory.objects.filter(user = user, typeOfTest = typeOfTest, Class = str(Class)).latest('paymentCount')
    if obj:
        if obj.paymentCount == '1':
            PaymentHistory.objects.filter(id = obj.id).update(paymentCount = '0')
            return Response("Payment Count Updated")

            # elif str(i.paymentCount) == str(2):
            #     obj.update(paymentCount = '1')
            #     return Response("Payment Count Updated")
            
            # if str(i.paymentCount) >= str(2):
            #     int(i.paymentCount) - int(1)
            #     obj.update(paymentCount = countMinus)
            #     return Response("Payment Count Updated")

            # if str(i.paymentCount) == str(0):
            #     return Response("Payment Count Updated")

        return Response("error")
    return Response("No Payment Count Updated")


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def checkPaymentRouter(request):
    user = request.user
    data = request.data
    typeOfTest = data["typeOfTest"]
    Class = data['Class']
    if Class == None or typeOfTest == None:
        return Response(status.HTTP_402_PAYMENT_REQUIRED)
    obj = PaymentHistory.objects.filter(user = user, typeOfTest = typeOfTest, Class = Class).latest('paymentCount')
    if obj:
            if obj.paymentCount == '0':
                return Response(status.HTTP_402_PAYMENT_REQUIRED)
            else:
                return Response(status.HTTP_202_ACCEPTED)
    return Response(status.HTTP_402_PAYMENT_REQUIRED)



