from django.contrib import admin
from django.urls import path
from .views import UserApiView, UserApiDetail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', UserApiView.as_view()),
    path('user/<int:id>', UserApiDetail.as_view()), 
]