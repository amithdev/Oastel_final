from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from core.views import check_availability


urlpatterns = [
    path('', views.home, name='home'),
    path('tours/', views.tours, name='tours'),  # 👈 new route
    path('tours/half-day-road-trip/', views.tour_detail_half_day, name='half_day_tour'),
    path('confirm/', views.confirm_adventure, name='confirm_adventure'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-cancel/', views.payment_cancel, name='payment_cancel'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('tours/<slug:slug>/', views.tour_detail_generic, name='tour_detail_generic'),
    path('book-transfers/', views.book_transfers, name='book_transfers'),
    path('confirm-transfer/', views.confirm_transfer, name='confirm_transfer'),
    path('blogs/', views.blogs, name='blogs'),
    path('confirm/<slug:slug>/', views.confirm_tour, name='confirm_tour'),
    
    path('get-max-bookings/', views.get_max_bookings, name='get_max_bookings'),
    path('check-availability/', views.check_availability, name='check_availability'),

    

]


    
   


   



