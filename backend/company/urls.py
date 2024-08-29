from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path



from . import views

urlpatterns = [
    path('api/contact/', views.company_create, name='company-create'),
    path('api/login/', views.login_view, name='login'),
    path('api/get-info/<str:username>/', views.get_company_info, name='get-info'),
    path('api/update-info/<str:username>/', views.update_company_info, name='update-info'),
]
