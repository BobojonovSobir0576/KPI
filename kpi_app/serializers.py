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
        fields = ['username','groups','first_name','last_name','position']
        


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
        
        

class UserFileUploadSerializers(serializers.ModelSerializer):    
    class Meta:
        model = UserFileUplaod
        fields = ['author','files','question','date']
        
    def create(self, validated_data):
        create = UserFileUplaod.objects.create(
            author = self.context.get('user'),
            question = self.context.get('unique_id'),
            files = self.context.get('files'),
        )
        return create
          
        
        
class BallToFileUploadSerializers(serializers.ModelSerializer):    
    class Meta:
        model = BallToFile
        fields = ['author','files','ball','date']
        
    def create(self, validated_data):
        update = BallToFile.objects.filter(files__unique_id=self.context.get('files').unique_id).first()
        if update:
            update.author.add(self.context.get('user'))
            update.ball  = update.ball + validated_data['ball']
            update.save()
            return update
        else:
            create = BallToFile.objects.create(
                ball = validated_data.get('ball'),
                files = self.context.get('files'),
            )
            create.total_ball = create.total_ball + create.ball
            create.author.add(self.context.get('user'))
            create.save()
            return create
        

class PenaltyUplaodFileSerializers(serializers.ModelSerializer):    
    class Meta:
        model = PenaltyUplaodFile
        fields = ['author','files','ball','date']
        
    def create(self, validated_data):
        update = PenaltyUplaodFile.objects.filter(get_file=self.context.get('get_file')).first()
        if update:
            print('Yes')
            update.author.add(self.context.get('user'))
            update.ball  = update.ball + validated_data['ball']
            update.save()
            
            update_ball_to_file = BallToFile.objects.filter(files = self.context.get('get_file')).first()
            update_ball_to_file.ball = update_ball_to_file.ball - validated_data['ball']
            update_ball_to_file.save()
            return update
        else:
            print('No')
            create = PenaltyUplaodFile.objects.create(
                ball = validated_data.get('ball'),
                files = self.context.get('files'),
                get_file = self.context.get('get_file'),
            )
            create.author.add(self.context.get('user'))
            create.save()
            
            update_ball_to_file = BallToFile.objects.filter(files = self.context.get('get_file')).first()
            update_ball_to_file.ball = update_ball_to_file.ball - validated_data['ball']
            update_ball_to_file.save()
            return create