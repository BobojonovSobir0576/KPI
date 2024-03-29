from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize
from django.shortcuts import render,redirect
from django.contrib.auth.models import *
from django.forms.models import model_to_dict

from kpi_app.serializers import *
from kpi_app.renderers import *

from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework import generics, permissions, status, views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import collections, functools, operator

from collections import defaultdict
import json

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
        send_list = []
        main_categories = MainCategories.objects.filter_categories(request.user)
        for i in main_categories:
            get_category = Categories.objects.filter(main_categories_id__unique_id = i.unique_id)
            serialized_data = serialize("json", get_category)
            serialized_data = json.loads(serialized_data)
            send_list.append({
                'main_cate':i.name,
                'categories': serialized_data
            })
        return Response(json.loads(json.dumps(list(send_list))) ,status=status.HTTP_200_OK)
    
    
class MainCategoriesUserView(APIView):
    permission_classes = [IsAuthenticated]
    render_classes = [UserRenderers]
    
    def get(self,request,format = None):
        send_list = []
        main_categories = MainCategories.objects.all()
        for i in main_categories:
            get_category = Categories.objects.filter(main_categories_id__unique_id = i.unique_id)
            serialized_data = serialize("json", get_category)
            serialized_data = json.loads(serialized_data)
            send_list.append({
                'main_cate':i.name, 
                'categories': serialized_data
            })
        return Response(json.loads(json.dumps(list(send_list))) ,status=status.HTTP_200_OK)

    
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
    

class SendFiles(APIView):
    permission_classes = [IsAuthenticated]
    render_classes = [UserRenderers]
    
    def get(self,request,unique_id, format=None):
        categories_get = get_object_or_404(Categories, unique_id = unique_id)
        get_files = UserFileUplaod.objects.filter(question__categories_id = categories_get)
        serializers = FilesSendSerializers(get_files,many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    
    
class UserGetTotalBall(APIView):
    permission_classes = [IsAuthenticated]          
    render_classes = [UserRenderers]
    
    def get(self,request,format=None):
        user = CustomUser.objects.filter(groups__name__in = ['Foydalanuvchi'])
        lists = []
        list_user = []
        for i in user:
            get_files = BallToFile.objects.filter(files__author__unique_id = i.unique_id)
            for k in get_files: 
                lists.append({
                    'ball': k.ball // len(k.author.all()),
                    'name':i.first_name +" "+i.last_name,
                })    
        aggregated_data = {}
                
        for dictionary in lists:
            key = (dictionary['name'])
        
            aggregated_data[key] = aggregated_data.get(key, 0) + dictionary['ball']
            
        lists = [{'name': key, 'ball': value} for key, value in aggregated_data.items()]
        return Response(list(lists),status=status.HTTP_200_OK)
    
    