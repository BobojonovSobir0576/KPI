from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin
from kpi_app.forms import *

class NewMyUser(ImportExportModelAdmin,UserAdmin):
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
class MainCategoriesAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('name','unique_id')
    
@admin.register(Categories)
class CategoriesAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('name','main_categories_id','unique_id')
    
@admin.register(Questions)
class QuestionsAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('question','unique_id','date_of_calculation_ball','categories_id')
    
@admin.register(PenaltyPointForQuestions)
class PenaltyPointForQuestionsAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('description','unique_id')
    
@admin.register(UserFileUplaod)
class UserFileUplaodAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('author','unique_id','files','question','date')
    
@admin.register(BallToFile)
class BallToFileAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('unique_id','ball','files','date')
    
@admin.register(PenaltyUplaodFile)
class PenaltyUplaodFileAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('unique_id','ball','files','date')