from django.urls import path
from kpi_app import views


urlpatterns = [
    path('user_login/',views.UserLoginView.as_view()),
    path('user_profile/',views.UserProfilesView.as_view()),
    path('user_logout/',views.UserLogoutView.as_view()),
    path('main_categories/',views.MainCategoriesView.as_view()),
    path('main_categories_user/',views.MainCategoriesUserView().as_view()),
    path('question/<uuid:unique_id>/',views.QuestionView.as_view()),
    path('user_file_upload/<uuid:unique_id>/',views.UserFileUploadView.as_view()),
    path('user_files_get/<uuid:unique_id>/',views.SendFiles.as_view()),
    path('ball_to_file_upload/<uuid:unique_id>/',views.BallToFileUploadView.as_view()),
    path('penalty_upload_file/<uuid:unique_id>/',views.PenaltyUplaodFileView.as_view()),
    path('send_files/',views.UserGetTotalBall.as_view())
]