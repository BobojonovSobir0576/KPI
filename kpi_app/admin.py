from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from kpi_app.forms import *

class NewMyUser(UserAdmin):
    add_form = CreasteUser
    form = ChangeUser
    model = CustomUser
    list_display = ['username','first_name','last_name','unique_id',]
    fieldsets = UserAdmin.fieldsets + (
        (None,{'fields':('position',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None,{'fields':('position',)}),
    )
admin.site.register(CustomUser,NewMyUser)


@admin.register(MainCategories)
class MainCategoriesAdmin(admin.ModelAdmin):
    list_display = ('name','unique_id')
    
@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name','main_categories_id','unique_id')
    
@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('question','unique_id','date_of_calculation_ball','categories_id')
    
@admin.register(PenaltyPointForQuestions)
class PenaltyPointForQuestionsAdmin(admin.ModelAdmin):
    list_display = ('description','unique_id')
    
@admin.register(UserFileUplaod)
class UserFileUplaodAdmin(admin.ModelAdmin):
    list_display = ('author','unique_id','files','question','date')
    
@admin.register(BallToFile)
class BallToFileAdmin(admin.ModelAdmin):
    list_display = ('unique_id','ball','files','date')
    
@admin.register(PenaltyUplaodFile)
class PenaltyUplaodFileAdmin(admin.ModelAdmin):
    list_display = ('unique_id','ball','files','date')