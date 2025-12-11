from django.urls import path, include
from . import views

urlpatterns = [
    # Public Pages
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),

    # User Login & Register
    path('form/', views.signup, name='form'),
    path('login/', views.user_login, name='login'),
    path('main/', views.main, name='main'),

    # Orders
    path('api/order/', views.create_order, name='create_order'),

    # Admin Area
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin_orders/', views.admin_orders, name='admin_orders'),
    path("logout-admin/", views.logout_admin, name="logout_admin"),

    # Google OAuth
    path('oauth/', include('social_django.urls', namespace='social')),

  ##status update
    path("update-status/<int:order_id>/<str:new_status>/", views.update_order_status, name="update_order_status")

]
