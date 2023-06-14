from django.db import models
from django.contrib.auth.models import AbstractUser,Group
from kpi_app.querysets.managers import *
import uuid




class CustomUser(AbstractUser):
    unique_id = models.UUIDField('ID',default=uuid.uuid4, editable=False, unique=True)
    position = models.CharField('Lavozim',max_length=150,null=True,blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = "Baholovchi va Foydalanuvchilar"
        verbose_name_plural = "Baholovchi va Foydalanuvchilar"
        

class MainCategories(models.Model):
    unique_id = models.UUIDField('ID',default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField('Asosiy Kategoriya',max_length=150)
    author = models.ManyToManyField(CustomUser,verbose_name='Baholovchi tanlash')
    
    objects = MainCategoriesManager()
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Bosh kategoriya"
        verbose_name_plural = "Bosh kategoriya"
    

class Categories(models.Model):
    unique_id = models.UUIDField("ID",default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField("Kategoriya",max_length=150)
    main_categories_id = models.ForeignKey(MainCategories, on_delete=models.CASCADE,verbose_name='Asosiy Kategoriyaning IDsi')
    
    objects = CategoriesManager()
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Bosh kategoriyaga tegishli Kategoriyalar"
        verbose_name_plural = "Bosh kategoriyaga tegishli Kategoriyalar"


class PenaltyPointForQuestions(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    description = models.TextField('Jarima ballar(asoslovchi hujjat asosida) ')
    
    def __str__(self):
        return self.description
    
    class Meta:
        verbose_name = "Savollarning Jarima Ballari"
        verbose_name_plural = "Savollarning Jarima Ballari"
        

class Questions(models.Model):
    unique_id = models.UUIDField("ID",default=uuid.uuid4, editable=False, unique=True)
    question = models.TextField("Amalga oshiradigan ishlar")
    date_of_calculation_ball = models.CharField("Natijalarni hisoblab borish muddati",max_length=50)
    ball_of_question = models.IntegerField("Ball",default=0)
    description = models.TextField("Ballarni hisoblash metodikasi",)
    categories_id = models.ForeignKey(Categories, on_delete=models.CASCADE,verbose_name='Kategoriyaning IDsi')
    penalty_id = models.ManyToManyField(PenaltyPointForQuestions,verbose_name='Jarimalar izohi')
    
    objects = QuestionsManager()
    
    def __str__(self):
        return self.question
    
    class Meta:
        verbose_name = "Kategoriyaning Savollari"
        verbose_name_plural = "Kategoriyaning Savollari"
        

class UserFileUplaod(models.Model):
    unique_id = models.UUIDField("ID", default=uuid.uuid4, editable=False, unique=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,verbose_name='Avtor')
    files = models.FileField(upload_to='user_files',verbose_name='Fayl')
    question = models.ForeignKey(Questions, on_delete=models.CASCADE,verbose_name='Qaysi savolga yuborilgani')
    date = models.DateField(auto_now_add=True,auto_created=False,verbose_name='Kiritilgan sana')
    
    def __str__(self):
        return f"{self.author.first_name} {self.author.last_name}"
    
    class Meta:
        verbose_name = "Foydalanuvchi qo'shgan ma'lumotlari"
        verbose_name_plural = "Foydalanuvchi qo'shgan ma'lumotlari"
    
    

class BallToFile(models.Model):
    unique_id = models.UUIDField("ID", default=uuid.uuid4, editable=False, unique=True)
    author = models.ManyToManyField(CustomUser,verbose_name='Avtor')
    ball = models.FloatField(default=0,verbose_name="Qo'yilgan ball")
    total_ball = models.IntegerField(default=0)
    files = models.ForeignKey(UserFileUplaod, on_delete = models.CASCADE,verbose_name="Yuklangan faylgan ball qo'yilgan")
    date = models.DateField(auto_created=False,auto_now_add=True,verbose_name="Ball")
    
    def __str__(self):
        return f"{self.author}"
    
    class Meta:
        verbose_name = "Baholovchi qo'shilgan ma'lumotga ball qo'shishi"
        verbose_name_plural = "Baholovchi qo'shilgan ma'lumotga ball qo'shishi"


class PenaltyUplaodFile(models.Model):
    unique_id = models.UUIDField("ID", default=uuid.uuid4, editable=False, unique=True)
    author = models.ManyToManyField(CustomUser,verbose_name='Avtor')
    ball = models.FloatField(default=0,verbose_name="Qo'yilgan ball")
    get_file = models.ForeignKey(UserFileUplaod, on_delete = models.CASCADE,verbose_name="Yuklangan faylgan ball qo'yilgan")
    files = models.FileField(upload_to='penalty_file',verbose_name="Jarima ballni isbotlash uchun Fayl yuklanganligi")
    date = models.DateField(auto_created=False,auto_now_add=True,verbose_name="Ball")
    
    def __str__(self):
        return f"{self.author}"
    
    class Meta:
        verbose_name = "Jarima Ballari"
        verbose_name_plural = "Jarima Ballari"