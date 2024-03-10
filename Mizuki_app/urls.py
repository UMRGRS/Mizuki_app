from django.urls import path

from . import views

app_name = "Mizuki_app"
urlpatterns = [
    path('waiters/', views.WaitersPage, name='waitersPage'),
    path('<str:message>/waiters/', views.WaitersPage, name="waitersPageMessage"),
    path('kitchen/', views.KitchenPage, name='kitchenPage'),
    path('cashier/', views.CashiersPage, name='cashierPage'),
    path('payment/', views.PaymentPage, name='paymentPage'),
    path('add_prod/', views.AddProd, name='add_prod'),
    path('del_prod/', views.DelProd, name='del_prod'),
    path('cancel_order/', views.CancelOrder, name='cancel_order'),
    path('<int:order_id>/complete_order/', views.CompleteOrder, name='complete_order'),
    path('place_order/', views.PlaceOrder, name='place_order'),
]