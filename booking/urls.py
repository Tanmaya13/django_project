from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('show-service/<int:sid>/', views.services_show, name='services'),
    path('allServices/', views.allServices, name='all'),
    path('show-service/<int:id>/take/', views.take, name='take'),
    path('product/<int:pid>/<str:msg>/', views.show_product_msg, name='product'),
    path('product/<int:pid>//', views.show_product, name='product'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('signIn/', views.signIn, name='signIn'),
    path('logIn/', views.loginUser, name='login'),
    path('book/', views.makeBooking, name='book'),
    path('mybookings/', views.bookings, name='mybookings'),
    path('booking/<int:bid>/', views.show_booking, name='booking'),
    path('logout/', views.logout, name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)