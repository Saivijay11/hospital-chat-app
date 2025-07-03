from django.urls import path
from users.views import RegisterView, UserProfileView, UserListView, AllUsersView, CustomLoginView, PatientListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='user-register'),
    path('login/', CustomLoginView.as_view(), name='token_obtain_pair'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('all/', UserListView.as_view(), name='user-list'), 
    path('all-users/', AllUsersView.as_view(), name='all-users'),
    path("patients/", PatientListView.as_view(), name="patients-list")
]
