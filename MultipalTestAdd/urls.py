from django.urls import path, include
from MultipalTestAdd import views

urlpatterns = [
    path('class/', views.testSelect, name="title"),
    path('save-result/', views.saveResult, name="save-result"),
    path('result/', views.getResult, name="result"),
    path('test-backup/', views.testBackup, name="test-backup"),
    path('delete-result/', views.delReuslt, name="delete-result"),
    path('get-backup/', views.backupGet, name="get-backup"),
    path('delete-backup/', views.delBackup, name="delete-backup"),
    path('student-panding-test/', views.pandingTest, name="student-panding-test"),
    path('test-info/', views.testInfo, name="test-info"),
    path('test-payment-done/', views.paymentAndTest, name="test-payment-done"),
    path('buy-test/', views.buyTest, name="buy-test"),
    path('payment-decriment/', views.paymentDecriment, name="payment-decrimen"),

    # // payment URL
    path('handlepayment/', views.HandlePaytemRequest, name='HandleRequest'),




    # path('self/', views.self, name="self"),
]


