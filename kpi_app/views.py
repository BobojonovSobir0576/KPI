from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render,redirect
from django.contrib.auth.models import *

from kpi_app.serializers import *
from kpi_app.renderers import *

from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework import generics, permissions, status, views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'accsess':str(refresh.access_token)
    }


class UserLoginView(APIView):
    render_classes = [UserRenderers]
    
    def post(self,request,format=None):
        serializers = UserLoginSerializers(data=request.data, partial=True)
        if serializers.is_valid(raise_exception=True):
            username = serializers.data['username']
            password = serializers.data['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                token = get_token_for_user(user)
                return Response({'token':token,'message':serializers.data},status=status.HTTP_200_OK)
            else:
                return Response({'error':{'none_filed_error':['Username or password is not valid']}},status=status.HTTP_404_NOT_FOUND)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    

class UserProfilesView(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    
    def get(self,request,format=None):
        serializer = UserPorfilesSerializers(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    
class UserLogoutView(APIView):
    permission_classes  = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        if self.request.data.get('all'):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response({"status": "OK, goodbye, all refresh tokens blacklisted"})
        refresh_token = self.request.data.get('refresh_token')
        token = RefreshToken(token=refresh_token)
        token.blacklist()
        return Response({"status": "OK, goodbye"})
    

class MainCategoriesView(APIView):
    permission_classes = [IsAuthenticated]
    render_classes = [UserRenderers]
    
    def get(self,request,format = None):
        main_categories = MainCategories.objects.filter_categories(request.user)
        serializers = MainCategoriesSerializers(main_categories,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    

class CategoriesView(APIView):
    permission_classes = [IsAuthenticated]
    render_classes = [UserRenderers]
    
    def get(self,request,unique_id,format = None):
        main_categories = Categories.objects.filter_categories(unique_id)
        serializers = CategoriesSerializers(main_categories,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    
    
class QuestionView(APIView):
    permission_classes = [IsAuthenticated]
    render_classes = [UserRenderers]
    
    def get(self,request,unique_id,format = None):
        categories_get = get_object_or_404(Categories, unique_id = unique_id)
        main_categories = Questions.objects.filter_question(categories_get.unique_id)
        serializers = QuestionSerializers(main_categories,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    

class UserFileUploadView(APIView):
    permission_classes = [IsAuthenticated]
    render_classes = [UserRenderers]
    
    def post(self, request, unique_id, format=None):
        question_get = get_object_or_404(Questions,unique_id = unique_id)
        serializers = UserFileUploadSerializers(data=request.data, partial=True,context = {'user':request.user,'files':request.FILES.get('files'),'unique_id':question_get})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({'msg':'Files is uploaded'},status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
    

class BallToFileUploadView(APIView):
    permission_classes = [IsAuthenticated]
    render_classes = [UserRenderers]
    
    def post(self, request,unique_id, format=None):
        files_get = get_object_or_404(UserFileUplaod,unique_id = unique_id)
        serializers = BallToFileUploadSerializers(data=request.data, partial=True,context = {'user':request.user,'files':files_get})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({'msg':'Files is uploaded'},status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
class PenaltyUplaodFileView(APIView):
    permission_classes = [IsAuthenticated]
    render_classes = [UserRenderers]
    
    def post(self, request,unique_id, format=None):
        files_get = get_object_or_404(UserFileUplaod,unique_id = unique_id)
        serializers = PenaltyUplaodFileSerializers(data=request.data, partial=True,context = {'user':request.user,'files':request.FILES.get('files'),"get_file":files_get})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({'msg':'Files is uploaded'},status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
`       `