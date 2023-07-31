from django.shortcuts import render
from rest_framework import generics, status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView 
from rest_framework.response import Response
from django.http.response import JsonResponse
from .models import Breeds
from .serialize import BreedsSerializer 
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination


class BreedsApiPagination(PageNumberPagination):
    page_size = 10


class BreedsApiView(APIView):
    pagination_class = BreedsApiPagination

    @permission_classes([IsAuthenticated])
    def get(self, request):
        breeds = Breeds.objects.all()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(breeds, request)
        serializer = BreedsSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    def post(self, request): 
        #res = request.data.get('name')  
        serializer = BreedsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)

class BreedsApiDetail(APIView):
    
    def get_object(self, pk):
        try:
            return Breeds.objects.get(pk=pk)
        except Breeds.DoesNotExist:
            return None
    def get(self, request, id):
        post = self.get_object(id)
        serializer = BreedsSerializer(post)  
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    def put(self, request, id):
        post = self.get_object(id)
        if(post==None):
            return Response(status=status.HTTP_200_OK, data={ 'error': 'Not found data'})
        serializer = BreedsSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, id):
        post = self.get_object(id)
        post.delete()
        response = { 'deleted': True }
        return Response(status=status.HTTP_204_NO_CONTENT, data=response)

