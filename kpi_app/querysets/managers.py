from typing import Optional
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from kpi_app.models import *

# Main Categories
class MainCategoriesQuerySet(models.QuerySet):
    
    def filter_categories(self,user):
        return self.prefetch_related('author').filter(author = user)

class MainCategoriesManager(models.Manager):
    
    def get_queryset(self):
        return MainCategoriesQuerySet(self.model, using=self._db)
    
    def filter_categories(self,user):
        return self.get_queryset().filter_categories(user)
    

# Categories
class CategoriesQuerySet(models.QuerySet):
    
    def filter_categories(self,unique_id):
        return self.prefetch_related('main_categories_id').filter(main_categories_id__unique_id = unique_id)

class CategoriesManager(models.Manager):
    
    def get_queryset(self):
        return CategoriesQuerySet(self.model, using=self._db)
    
    def filter_categories(self,unique_id):
        return self.get_queryset().filter_categories(unique_id)
    

# Questions
class QuestionsQuerySet(models.QuerySet):
    
    def filter_question(self,unique_id):
        return self.prefetch_related('categories_id').filter(categories_id__unique_id = unique_id)

class QuestionsManager(models.Manager):
    
    def get_queryset(self):
        return QuestionsQuerySet(self.model, using=self._db)
    
    def filter_question(self,unique_id):
        return self.get_queryset().filter_question(unique_id)