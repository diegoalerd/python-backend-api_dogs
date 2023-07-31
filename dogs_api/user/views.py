from django.shortcuts import render
from rest_framework import generics, status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView 
from rest_framework.response import Response
from django.http.response import JsonResponse
from .models import User
from .serialize import UserSerializer, MyTokenObtainPairSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserApiPagination(PageNumberPagination):
    page_size = 10


class UserApiView(APIView):
    pagination_class = UserApiPagination

    def get(self, request):
        users = User.objects.all()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(users, request)
        serializer = UserSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    def post(self, request): 
        #res = request.data.get('name')  
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)

class UserApiDetail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None
    def get(self, request, id):
        post = self.get_object(id)
        serializer = UserSerializer(post)  
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    def put(self, request, id):
        post = self.get_object(id)
        if(post==None):
            return Response(status=status.HTTP_200_OK, data={ 'error': 'Not found data'})
        serializer = UserSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, id):
        post = self.get_object(id)
        post.delete()
        response = { 'deleted': True }
        return Response(status=status.HTTP_204_NO_CONTENT, data=response)

@api_view(['POST'])
@permission_classes([AllowAny, ])
def authenticate_user(request):
    try:
        email = request.data['email']
        password = request.data['password']
        user = User.objects.get(email=email, password=password)
        if user:
            try:
                payload = jwt_payload_handler(user)
                token = jwt.encode(payload, settings.SECRET_KEY)
                user_details = {}
                user_details['name'] = "%s %s" % (
                    user.first_name, user.last_name)
                user_details['token'] = token
                user_logged_in.send(sender=user.__class__,
                                    request=request, user=user)
                return Response(user_details, status=status.HTTP_200_OK)
            except Exception as e:
                raise e
        else:
            res = {
                'error': 'No se pudo autenticar la información'}
            return Response(res, status=status.HTTP_400_FORBIDDEN)
    except KeyError:
        res = {'error': 'Por favor introduzca las crednciales email y password'}
        return Response(res)