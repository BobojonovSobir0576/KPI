from django.urls import path
from kpi_app import views


urlpatterns = [
    path('user_login/',views.UserLoginView.as_view()),
    # path('user_register/',views.UserRegisterView.as_view()),
    path('user_profile/',views.UserProfilesView.as_view()),
    # path('user_update/<int:id>/',views.UserUpdateView.as_view()), 
    path('user_logout/',views.UserLogoutView.as_view()),
    path('main_categories/',views.MainCategoriesView.as_view()),
    path('categories/<uuid:unique_id>/',views.CategoriesView.as_view()),
    path('question/<uuid:unique_id>/',views.QuestionView.as_view()),
]