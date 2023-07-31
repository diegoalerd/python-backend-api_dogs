from django.contrib import admin
from django.urls import path
from .views import BreedsApiView, BreedsApiDetail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('breeds/', BreedsApiView.as_view()),
    path('breeds/<int:id>', BreedsApiDetail.as_view()), 
]