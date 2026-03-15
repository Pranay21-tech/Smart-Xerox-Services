from django.conf import settings
from django.urls import path, include
import static
from . import views
from django.conf.urls.static import static


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
    path('pdf-printing/', views.pdf_printing, name='pdf_printing'),
    path("forgot-password/", views.forgot_password, name="forgot_password"),

    # =========================
    # User Login & Register
    # =========================
    path('form/', views.signup, name='form'),
   path("login/", views.user_login, name="login"),
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
path('profile/', views.profile, name='profile'),
path("delete-order/<int:id>/", views.delete_order, name="delete_order"),


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
    path("payment-history/", views.payment_history, name="payment_history"),
    path("update-status/<int:id>/", views.update_order_status, name="update_status"),


# =========================
# FAQ & Chatbot
# =========================
    path('faq/', views.faq_page, name='faq'),
    path('chatbot-response/', views.chatbot_response, name='chatbot_response'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
