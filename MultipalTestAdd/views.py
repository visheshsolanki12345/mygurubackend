from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from .PayTm import Checksum
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import uuid
import collections
from threading import Thread, Condition, RLock, Event
import time


from .models import (
    AddClassSection, Career, NewClass, ResultTitle, SelectNumber, ShowGrade, Section, Interpretation, TestBackupOneQuizeCorrect, Title,
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


@api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
def classSection(request, pk):
    data = request.data
    filterByClass = pk
    if filterByClass == None:
        return Response(status.HTTP_404_NOT_FOUND)
    context = {}
    p = []
    dis = AddTest.objects.filter(className = filterByClass)
    for i in dis:
        context['id'] = i.classSection.id
        context['newClass'] = i.classSection.classSection
        p.append((collections.OrderedDict(context)))
    return Response(p)






@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def testInfo(request):
    data = request.data
    user = request.user
    filterByClass = data['id']
    classSectionLocal = data['classSection']
    typeTest = ''
    Class = ''
    classSection = ''
    classSectionId = ''
    signal = ''
    signal = ''

    if filterByClass == None and classSection == None:
        return Response(status.HTTP_404_NOT_FOUND)
    
    classSec = AddClassSection.objects.filter(id = classSectionLocal)
    for i in classSec:
        classSectionId = i.id 

    dis = AddTest.objects.filter(className = filterByClass, classSection = classSectionId)
    for i in dis:
        typeTest = i.typeOfTest.selectTest
        Class = i.className.newClass
        classSection = i.classSection.classSection

    try:
        obj = PaymentHistory.objects.filter(user = user, typeOfTest = typeTest, Class = Class, classSection = classSection).latest('paymentCount')
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
    classSection = ''

    if filterByClass == None:
        return Response(status.HTTP_404_NOT_FOUND)

    dis = AddTest.objects.filter(className = filterByClass)
    for i in dis:
        typeTest = i.typeOfTest.selectTest
        Class = i.className.newClass
        classSection = i.classSection.classSection
        Amount = i.title.price
    try:
        obj = PaymentHistory.objects.filter(user = user, typeOfTest = typeTest, Class = Class, classSection = classSection).latest('paymentCount')
        if obj:
            if obj.paymentCount == '1':
                    testData = testFunc(typeTest, dis)
                    return Response(testData)
            else:
                payFuncObj = PaytemFunc(str(uuid.uuid4()), str(Amount) ,user.email, user, typeTest, Class, classSection)
                return Response(payFuncObj)
    except:
        pass
    payFuncObj = PaytemFunc(str(uuid.uuid4()), str(Amount) ,user.email, user, typeTest, Class, classSection)
    return Response(payFuncObj)



def PaytemFunc(orderId, amount, userEmail, user, typeOfTest, Class, classSection):
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
        classSection = classSection, 
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


def saveTestBackup(user, typeTest, Class, classSection, section, question, object, lastTime, mark):

    testID = ''
    sectionID = ''
    questionID = ''
    classID = ''
    addTestID = ''
    classSectionId = ''

    classType = NewClass.objects.filter(newClass = Class)
    for i in classType:
        classID = i.id
    
    classSec = AddClassSection.objects.filter(id = classSection)
    for i in classSec:
        classSectionId = i.id 

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
            upBackup = TestBackupOneQuizeCorrect.objects.filter(user = user ,className = classID, classSection = classSectionId, oneQuizeCorrect = i.id)
            if upBackup:
                upBackup.update(userClickObj = object)
                return True
            op = TestBackupOneQuizeCorrect.objects.create(user = user, userClickObj = object)
            TestBackupOneQuizeCorrect.objects.filter(id=op.id).update(
                typeOfTest = testID,
                className = classID,
                classSection = classSectionId, 
                oneQuizeCorrect = i.id,
                testDiscription = addTestID,
                lastTime = lastTime,
                number = mark,
                )
            return True

    elif typeTest == imageTest:
        qu = question.split("/media/")
        que = ImageOptionsTest.objects.filter(section=sectionID, question=qu[1])
        for i in que:
            upBackup = TestBackupOneImageQuizeCorrect.objects.filter(user = user ,className = classID, classSection = classSectionId, imageOneQuizeCorrect = i.id)
            if upBackup:
                upBackup.update(userClickObj = object)
                return True
            op = TestBackupOneImageQuizeCorrect.objects.create(user = user, userClickObj = object)
            TestBackupOneImageQuizeCorrect.objects.filter(id=op.id).update(
                typeOfTest = testID,
                className = classID,
                classSection = classSectionId, 
                imageOneQuizeCorrect = i.id,
                testDiscription = addTestID,
                lastTime = lastTime,
                number = mark,
                )
            return True

    elif typeTest == allOption:
        que = OptionsTest.objects.filter(section=sectionID, question=question)
        for i in que:
            upBackup = TestBackupMultipalQuize.objects.filter(user = user ,className = classID, classSection = classSectionId, multipalQuize = i.id, userClickObj=object)
            if upBackup:
                upBackup.delete()
                return True
            op = TestBackupMultipalQuize.objects.create(user = user, userClickObj = object)
            TestBackupMultipalQuize.objects.filter(id=op.id).update(
                typeOfTest = testID,
                className = classID,
                classSection = classSectionId, 
                multipalQuize = i.id,
                testDiscription = addTestID,
                lastTime = lastTime,
                number = mark,
                )
            return True
    elif typeTest == fiveOption:
        que = FiveOptionsTest.objects.filter(section=sectionID, question=question)
        for i in que:
            upBackup = TestBackupFiveQuize.objects.filter(user = user ,className = classID, classSection = classSectionId, fiveQuize = i.id)
            if upBackup:
                upBackup.update(userClickObj = object)
                return True
            op = TestBackupFiveQuize.objects.create(user = user, userClickObj = object)
            TestBackupFiveQuize.objects.filter(id=op.id).update(
                typeOfTest = testID,
                className = classID,
                classSection = classSectionId, 
                fiveQuize = i.id,
                testDiscription = addTestID,
                lastTime = lastTime,
                number = mark,
                )
            return True
            
    elif typeTest == threeOption:
        que = ThreeOptionsTest.objects.filter(section=sectionID, question=question)
        for i in que:
            upBackup = TestBackupThreeQuize.objects.filter(user = user ,className = classID, classSection = classSectionId, threeQuize = i.id)
            if upBackup:
                upBackup.update(userClickObj = object)
                return True
            op = TestBackupThreeQuize.objects.create(user = user, userClickObj = object)
            TestBackupThreeQuize.objects.filter(id=op.id).update(
                typeOfTest = testID,
                className = classID,
                classSection = classSectionId, 
                threeQuize = i.id,
                testDiscription = addTestID,
                lastTime = lastTime,
                number = mark,
                )
            return True

    else:
        return False
    

def backupGet(user, typeTest, Class, classSection):

    if Class == None or typeTest == None or classSection == None:
        return False

    classID = ''
    classSectionId = ''

    classType = NewClass.objects.filter(newClass = Class)
    for i in classType:
        classID = i.id 

    classSec = AddClassSection.objects.filter(id = classSection)
    for i in classSec:
        classSectionId = i.id

    if typeTest == oneOption:
        que = TestBackupOneQuizeCorrect.objects.filter(user = user ,className = classID, classSection = classSectionId)
        serializer = TestBackupOneQuizeCorrectSerializer(que, many=True)
        return serializer.data

    elif typeTest == imageTest:
        que = TestBackupOneImageQuizeCorrect.objects.filter(user = user ,className = classID, classSection = classSectionId)
        serializer = TestBackupOneImageQuizeCorrectSerializer(que, many=True)
        return serializer.data

    elif typeTest == allOption:
        que = TestBackupMultipalQuize.objects.filter(user = user ,className = classID, classSection = classSectionId)
        serializer = TestBackupMultipalQuizeSerializer(que, many=True)
        return serializer.data

    elif typeTest == threeOption:
        que = TestBackupThreeQuize.objects.filter(user = user ,className = classID, classSection = classSectionId)
        serializer = TestBackupThreeQuizeSerializer(que, many=True)
        return serializer.data

    elif typeTest == fiveOption:
        que = TestBackupFiveQuize.objects.filter(user = user ,className = classID, classSection = classSectionId)
        serializer = TestBackupFiveQuizeSerializer(que, many=True)
        return serializer.data
    


def resultGeneratorBackup(user, typeOfTest, Class, classSection):
    context = {}
    classID = NewClass.objects.get(newClass = Class)
    classSection = AddClassSection.objects.get(id = classSection)
    mysite = []
    
    if typeOfTest == oneOption:
        que = TestBackupOneQuizeCorrect.objects.filter(user = user ,className = classID, classSection = classSection)
        for i in que:
            mysite.append(f"{str(i.oneQuizeCorrect.section)}-{i.number}")

    elif typeOfTest == imageTest:
        que = TestBackupOneImageQuizeCorrect.objects.filter(user = user ,className = classID, classSection = classSection)
        for i in que:
            mysite.append(f"{str(i.imageOneQuizeCorrect.section)}-{i.number}")

    elif typeOfTest == allOption:
        que = TestBackupMultipalQuize.objects.filter(user = user ,className = classID, classSection = classSection)
        for i in que:
            mysite.append(f"{str(i.multipalQuize.section)}-{i.number}")
            
    elif typeOfTest == fiveOption:
        que = TestBackupFiveQuize.objects.filter(user = user ,className = classID, classSection = classSection)
        for i in que:
            mysite.append(f"{str(i.fiveQuize.section)}-{i.number}")

    elif typeOfTest == threeOption:
        que = TestBackupThreeQuize.objects.filter(user = user ,className = classID, classSection = classSection)
        for i in que:
            mysite.append(f"{str(i.threeQuize.section)}-{i.number}")


    xset = []
    for i in mysite:
        k = i.split('-')[0]
        xset.append(k)
    setV = set(xset)
    
    var = 0
    for i in setV:
        for j in mysite:
            if i == j.split('-')[0]:
                var += int(j.split('-')[1])
        context[str(i)] = var
        var = 0
    return context

# @api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
def findSectionResult(user, typeOfTest, Class, classSection):
    classID = ''
    classSectionId = ''
    secID = ''

    classObj = NewClass.objects.filter(newClass = Class)
    for i in classObj:
        classID = i.id
    
    classSec = AddClassSection.objects.filter(id = classSection)
    for i in classSec:
        classSectionId = i.id

    
    arraySet = set()

    if typeOfTest == allOption:
        sectionAll = OptionsTest.objects.all()
        for i in sectionAll:
            arraySet.add(i.section)
    elif typeOfTest == imageTest:
        sectionAll = ImageOptionsTest.objects.all()
        for i in sectionAll:
            arraySet.add(i.section)

    elif typeOfTest == oneOption:
        sectionAll = OneOptionsTest.objects.all()
        for i in sectionAll:
            arraySet.add(i.section)

    elif typeOfTest == threeOption:
        sectionAll = ThreeOptionsTest.objects.all()
        for i in sectionAll:
            arraySet.add(i.section)

    elif typeOfTest == fiveOption:
        sectionAll = FiveOptionsTest.objects.all()
        for i in sectionAll:
            arraySet.add(i.section)
    
    
    for allSecId in arraySet:
        secID = Section.objects.get(section = allSecId)

        countNO = []
        toQuCount = ''
        myArray = []
        noID = ''
        testID = ''
        
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

        newTest = AddTest.objects.filter(className=classID, classSection = classSectionId, typeOfTest=testID)
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
        Reports.objects.create(
            user = user, section = allSecId.section, totalCount = '0', totalNoQu = noSum,
            typeOftest = typeOfTest, classSection = classSection, Class = Class, grade = "Not Attempted"
        )
    return



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


def saveResult(user, typeOfTest, Class, classSection):
    classID = ''
    classSectionId = ''
    secID = ''
    in_id = ''

    classObj = NewClass.objects.filter(newClass = Class)
    for i in classObj:
        classID = i.id
    
    classSec = AddClassSection.objects.filter(id = classSection)
    for i in classSec:
        classSectionId = i.id

    if Class == None or typeOfTest == None or classSection == None:
        return Response(status.HTTP_404_NOT_FOUND)

    argu_one = resultGeneratorBackup(user, typeOfTest, Class, classSection)
    for key1, value1 in argu_one.items():
        sec = Section.objects.filter(section = key1)
        for i in sec:
            secID = i.id
            
        context = {}
        totalMarks = value1
        
        que = ShowGrade.objects.filter(className = classID, classSection = classSectionId, section = secID)
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
                interp = Interpretation.objects.filter(className = classID, classSection = classSectionId, section = secID)
                for i in interp:
                    in_id = i.id
                    carrerID = ''
                    
                    # if carrer != None:
                        # obj = Career.objects.filter(newCareer = carrer)
                        # for i in obj:
                        #     carrerID = i.id
                    
                    Reports.objects.filter(user=user,Class=Class, classSection = classSectionId,section=key1, typeOftest=typeOfTest).update(grade=grade, totalCount=totalMarks,interpretatio = in_id, carrer = carrerID)
                continue
             


def getResultFunc(user, typeOfTest, Class, classSection):

    if Class == None or typeOfTest == None or classSection == None:
        return False


    if typeOfTest == allOption:
        que = Reports.objects.filter(user=user, Class = Class, classSection = classSection, typeOftest = typeOfTest)
        serializer = ReportsSerializer(que, many=True)
        return serializer.data
    if typeOfTest == imageTest:
        que = Reports.objects.filter(user=user, Class = Class, classSection = classSection, typeOftest = typeOfTest)
        serializer = ReportsSerializer(que, many=True)
        return serializer.data
    if typeOfTest == oneOption:
        que = Reports.objects.filter(user=user, Class = Class, classSection = classSection, typeOftest = typeOfTest)
        serializer = ReportsSerializer(que, many=True)
        return serializer.data
    if typeOfTest == threeOption:
        que = Reports.objects.filter(user=user, Class = Class, classSection = classSection, typeOftest = typeOfTest)
        serializer = ReportsSerializer(que, many=True)
        return serializer.data
    if typeOfTest == fiveOption:
        que = Reports.objects.filter(user=user, Class = Class, classSection = classSection, typeOftest = typeOfTest)
        serializer = ReportsSerializer(que, many=True)
        return serializer.data
    # data2 = ShowGrade.objects.all()
    # context = {"mylist": data, "mylist1": data2}
    # try:
    #     pdfGenMail(context, user.email)
    # except:
    #     pass
    return False


def delReuslt(user, typeOfTest, Class, classSection):

    if Class == None or typeOfTest == None or classSection == None:
        return False
        
    if typeOfTest == allOption:
        Reports.objects.filter(user=user, Class = Class, classSection = classSection, typeOftest = typeOfTest).delete()
        return True
    elif typeOfTest == imageTest:
        Reports.objects.filter(user=user, Class = Class, classSection = classSection, typeOftest = typeOfTest).delete()
        return True
    elif typeOfTest == oneOption:
        Reports.objects.filter(user=user, Class = Class, classSection = classSection, typeOftest = typeOfTest).delete()
        return True
    elif typeOfTest == threeOption:
        Reports.objects.filter(user=user, Class = Class, typeOftest = typeOfTest).delete()
        return True
    elif typeOfTest == fiveOption:
        Reports.objects.filter(user=user, Class = Class, classSection = classSection, typeOftest = typeOfTest).delete()
        return True
    else:
        return True



def delBackup(user, typeOfTest, Class, classSection):

    if Class == None or typeOfTest == None or classSection == None:
        return False

    typeTestID = ''
    classID = ''
    classSectionId = ''
    obj = TestCategory.objects.filter(selectTest = typeOfTest)
    for i in obj:
        typeTestID = i.id

    objClass = NewClass.objects.filter(newClass = Class)
    for i in objClass:
        classID = i.id

    classSec = AddClassSection.objects.filter(id = classSection)
    for i in classSec:
        classSectionId = i.id

    if typeOfTest == allOption:
        TestBackupMultipalQuize.objects.filter(user=user, typeOfTest = typeTestID, className = classID, classSection = classSectionId).delete()
        return True
    elif typeOfTest == imageTest:
        TestBackupOneImageQuizeCorrect.objects.filter(user=user, typeOfTest = typeTestID, className = classID, classSection = classSectionId).delete()
        return True
    elif typeOfTest == oneOption:
        TestBackupOneQuizeCorrect.objects.filter(user=user, typeOfTest = typeTestID, className = classID, classSection = classSectionId).delete()
        return True
    elif typeOfTest == threeOption:
        TestBackupThreeQuize.objects.filter(user=user, typeOfTest = typeTestID, className = classID, classSection = classSectionId).delete()
        return True
    elif typeOfTest == fiveOption:
        TestBackupFiveQuize.objects.filter(user=user, typeOfTest = typeTestID, className = classID, classSection = classSectionId).delete()
        return True
    return False


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def pandingTest(request):
    user = request.user
    context = {}
    allOption = TestBackupMultipalQuize.objects.filter(user=user)
    if allOption:
        for i in allOption:
            context[i.className.id] = f"{i.className.newClass} - {i.classSection.classSection}"

    imageTest = TestBackupOneImageQuizeCorrect.objects.filter(user=user)
    if imageTest:
        for i in imageTest:
            context[i.className.id] = f"{i.className.newClass} - {i.classSection.classSection}"

    oneOption = TestBackupOneQuizeCorrect.objects.filter(user=user)
    if oneOption:
        for i in oneOption:
            context[i.className.id] = f"{i.className.newClass} - {i.classSection.classSection}"

    threeOption = TestBackupThreeQuize.objects.filter(user=user)
    if threeOption:
        for i in threeOption:
            context[i.className.id] = f"{i.className.newClass} - {i.classSection.classSection}"

    fiveOption = TestBackupFiveQuize.objects.filter(user=user)
    if fiveOption:
        for i in fiveOption:
            context[i.className.id] = f"{i.className.newClass} - {i.classSection.classSection}"

    return Response(context)




@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def buyTest(request):
    user = request.user
    testID = ""
    classID = ""
    classSectionId = ""

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
                classSec = AddClassSection.objects.filter(classSection = i.classSection)
                for i in classSec:
                    classSectionId = i.id
                addTestobj = AddTest.objects.filter(typeOfTest = testID, className = classID, classSection = classSectionId)
                for m in addTestobj:
                    context[i.className.id] = f"{i.className.newClass} - {i.classSection.classSection}"
        return Response(context)
    return Response("No buy test available")


def paymentDecriment(user, typeOfTest, Class, classSection):
    classSectionMain = ''

    if Class == None or typeOfTest == None or classSection == None:
        return False
    
    classSec = AddClassSection.objects.filter(id = classSection)
    for i in classSec:
        classSectionMain = i.classSection

    obj = PaymentHistory.objects.filter(user = user, typeOfTest = typeOfTest, Class = str(Class), classSection = classSectionMain).latest('paymentCount')
    if obj:
        if obj.paymentCount == '1':
            PaymentHistory.objects.filter(id = obj.id).update(paymentCount = '0')
            return True
        return False
    return True


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def checkPaymentRouter(request):
    user = request.user
    data = request.data
    typeOfTest = data["typeOfTest"]
    Class = data['Class']
    classSection = data['classSection']
    
    if Class == None or typeOfTest == None or classSection == None:
        return Response(status.HTTP_402_PAYMENT_REQUIRED)
    classSec = AddClassSection.objects.filter(id = classSection)
    for i in classSec:
        classSectionMain = i.classSection
    obj = PaymentHistory.objects.filter(user = user, typeOfTest = typeOfTest, Class = Class, classSection = classSectionMain).latest('paymentCount')
    if obj:
            if obj.paymentCount == '0':
                return Response(status.HTTP_402_PAYMENT_REQUIRED)
            else:
                return Response(status.HTTP_202_ACCEPTED)
    return Response(status.HTTP_402_PAYMENT_REQUIRED)



@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_backup_func(request):
    user = request.user
    data = request.data
    typeOfTest = data["typeOfTest"]
    Class = data['Class']
    classSection = data['classSection']
    # lock = Condition()
    # lock.acquire()
    varSerializer = backupGet(user, typeOfTest, Class, classSection)
    # lock.notify()
    # lock.release()
    return Response(varSerializer)
            
    

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def saveBackup_all(request):
    # start = time.time()
    user = request.user
    data = request.data

    typeOfTest = data["typeOfTest"]
    Class = data['Class']
    classSection = data['classSection']
    section = data['section']
    question = data['question']
    marks = data['marks']
    object = data['object']
    carrer = data['carrer']
    lastTime = data['lastTime']

    sb = Thread(target=saveTestBackup, args=(user, typeOfTest, Class, classSection, 
        section, question, object, lastTime, marks))
    sb.start()
    sb.join()
    # end = time.time()
    # print(f"Runtime of the program is {end - start}")
    return Response(status.HTTP_200_OK)



class ResultShowDeleteAll:
    def __init__(self, user, typeOfTest, Class, classSection):
        self.getResultData = []
        Thread.__init__(self)
        self.lock = Condition()
        self.user = user
        self.typeOfTest = typeOfTest
        self.Class = Class    
        self.classSection = classSection    

    def save_section(self):
        self.lock.acquire()
        findSectionResult(
            self.user, self.typeOfTest, self.Class, self.classSection,
        )
        self.lock.notify()
        self.lock.release()

    def save_result(self):
        self.lock.acquire()
        saveResult(
            self.user, self.typeOfTest, self.Class, self.classSection,
        )
        self.lock.notify()
        self.lock.release()

    def get_result(self):
        self.lock.acquire()
        serializerData = getResultFunc(
            self.user, self.typeOfTest, self.Class, self.classSection, 
        )
        for i in serializerData:
            self.getResultData.append(i)
        self.lock.notify()
        self.lock.release()

    def payment_decriment(self):
        paymentDecriment(
            self.user, self.typeOfTest, self.Class, self.classSection, 
        )

    def del_backup(self):
        self.lock.acquire()
        delBackup(
            self.user, self.typeOfTest, self.Class, self.classSection, 
        )
        self.lock.notify()
        self.lock.release()
    
    def del_result(self):
        self.lock.acquire()
        delReuslt(
            self.user, self.typeOfTest, self.Class, self.classSection, 
        )
        self.lock.notify()
        self.lock.release()

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def getResult(request):
    # start = time.time()
    user = request.user
    data = request.data

    typeOfTest = data["typeOfTest"]
    Class = data['Class']
    classSection = data['classSection']

    getResultDelEtc = ResultShowDeleteAll(
        user, typeOfTest, Class, classSection, 
        )
    
    ss = Thread(target=getResultDelEtc.save_section)
    sr = Thread(target=getResultDelEtc.save_result)
    gr = Thread(target=getResultDelEtc.get_result)
    pd = Thread(target=getResultDelEtc.payment_decriment)
    db = Thread(target=getResultDelEtc.del_backup)
    dr = Thread(target=getResultDelEtc.del_result)

    ss.start()
    sr.start()
    gr.start()
    pd.start()
    db.start()
    dr.start()

    ss.join()
    sr.join()
    gr.join()
    pd.join()
    db.join()
    dr.join()
    # end = time.time()
    # print(f"Runtime of the program is {end - start}")
    return Response(getResultDelEtc.getResultData)

    



    



