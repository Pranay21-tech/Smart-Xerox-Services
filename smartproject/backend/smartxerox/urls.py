from django.urls import path, include
from . import views
from .views import admin_settings_view, printQueue_admin, send_to_print_queue



urlpatterns = [

    # =========================
    # Public Pages
    # =========================
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('stationery/', views.Stationery, name='stationery'),

    # =========================
    # User Login & Register
    # =========================
    path('form/', views.signup, name='form'),
    path('login/', views.user_login, name='login'),
    path('main/', views.main, name='main'),

    # =========================
    # Orders API
    # =========================
    path('api/order/', views.create_order, name='create_order'),

    # =========================
    # Admin Area
    # =========================
path('admin-login/', views.admin_login, name='admin_login'),
path('admin_orders/', views.admin_orders, name='admin_orders'),
path("logout-admin/", views.logout_admin, name="logout_admin"),
path("settings/", views.admin_settings_view, name="admin_settings"),
path("print-queue/", views.printQueue_admin, name="printQueue_admin"),
path("send-to-print/", views.send_to_print_queue, name="send_to_print_queue"),
path("print-file/<str:order_id>/", views.open_print_file, name="open_print_file"),


    # =========================
    # Google OAuth
    # =========================
    path('oauth/', include('social_django.urls', namespace='social')),

    # =========================
    # Payment
    # =========================
    path("payment/", views.payment_page, name="payment_page"),  
    path("payment/success/", views.payment_success, name="payment_success"),
    path("api/create-order/", views.create_razorpay_order, name="create_razorpay_order"),


# =========================
# FAQ & Chatbot
# =========================
    path('faq/', views.faq_page, name='faq'),
    path('chatbot-response/', views.chatbot_response, name='chatbot_response'),
]
