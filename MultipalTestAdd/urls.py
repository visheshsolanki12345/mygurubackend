from django.urls import path, include
from MultipalTestAdd import views

urlpatterns = [
    path('class/', views.testSelect, name="class"),
    path('class-section/<int:pk>/', views.classSection, name="class-section"),
    path('save-result/', views.saveResult, name="save-result"),
    path('result/', views.getResult, name="result"),
    # path('test-backup/', views.testBackup, name="test-backup"),
    path('delete-result/', views.delReuslt, name="delete-result"),
    path('get-backup/', views.get_backup_func, name="get-backup"),
    path('delete-backup/', views.delBackup, name="delete-backup"),
    path('student-panding-test/', views.pandingTest, name="student-panding-test"),
    path('test-info/', views.testInfo, name="test-info"),
    path('test-payment-done/', views.paymentAndTest, name="test-payment-done"),
    path('buy-test/', views.buyTest, name="buy-test"),
    path('payment-decriment/', views.paymentDecriment, name="payment-decrimen"),
    path('payment-router/', views.checkPaymentRouter, name="payment-router"),
    path('test/', views.saveBackup_all, name="test"),

    # path('self/', views.findSection, name="self"),

    # // payment URL
    path('handlepayment/', views.HandlePaytemRequest, name='HandleRequest'),

    # path('self/', views.self, name="self"),
]


