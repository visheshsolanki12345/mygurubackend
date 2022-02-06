from django.urls import path, include
from CommanFunctions import paymentView
urlpatterns = [
    path('handlepayment/', paymentView.HandlePayRequest, name='HandleRequest'),
]
