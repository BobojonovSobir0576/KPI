from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User,Group
from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.exceptions import AuthenticationFailed

from kpi_app.models import *



class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class UserLoginSerializers(serializers.ModelSerializer):
    username = serializers.CharField(max_length=250)
    password = serializers.CharField(max_length=250)
    
    class Meta:
        model = CustomUser
        fields = ['username','password']
        

class UserPorfilesSerializers(serializers.ModelSerializer):
    groups = GroupSerializer(read_only=True, many=True)
    
    class Meta:
        model = CustomUser
        fields = ['username','groups','first_name','last_name',]
        


class MainCategoriesSerializers(serializers.ModelSerializer):
    author = UserPorfilesSerializers(read_only=True,many=True)
    
    class Meta:
        model = MainCategories
        fields = ['unique_id','name','author']
        
class CategoriesSerializers(serializers.ModelSerializer):
    
    main_categories_id = MainCategoriesSerializers(read_only=True)
    
    class Meta:
        model = Categories
        fields = ['unique_id','name','main_categories_id']
        
        
        
class PenaltyPointForQuestionsSerialzers(serializers.ModelSerializer):
    class Meta:
        model = PenaltyPointForQuestions
        fields = ['unique_id','description']
        
class QuestionSerializers(serializers.ModelSerializer):
    
    categories_id = CategoriesSerializers(read_only=True)
    penalty_id = PenaltyPointForQuestionsSerialzers(read_only=True,many=True)
    
    class Meta:
        model = Questions
        fields = ['unique_id','question','date_of_calculation_ball','ball_of_question','description','penalty_id','categories_id']