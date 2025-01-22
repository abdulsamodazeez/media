from django.urls import path
from .views import (
    UserListView,
    UserCreateView,
    UserEditView,
    UserActivityLogsView,
    SocialMediaAccountsView,
    HealthCheckView,
    PostingConfigurationsView,
)

app_name = 'user_management'

urlpatterns = [
    # User Management
    path('', UserListView.as_view(), name='user_list'),  # /users/
    path('create/', UserCreateView.as_view(), name='user_create'),  # /users/create/
    path('edit/<int:pk>/', UserEditView.as_view(), name='user_edit'),  # /users/edit/<id>/
    path('activity/', UserActivityLogsView.as_view(), name='user_activity_logs'),  # /users/activity/
    # Social Media Accounts
    path('accounts/', SocialMediaAccountsView.as_view(), name='list_accounts'),  # /users/accounts/
    path('accounts/add/', SocialMediaAccountsView.as_view(), name='add_account'),  # /users/accounts/add/
    path('accounts/remove/<int:pk>/', SocialMediaAccountsView.as_view(), name='remove_account'),  # /users/accounts/remove/<id>/
    path('accounts/health-check/', HealthCheckView.as_view(), name='health_check'),  # /users/accounts/health-check/
    # Posting Configurations
    path('posting-configs/', PostingConfigurationsView.as_view(), name='get_posting_configs'),  # /users/posting-configs/
    path('posting-configs/update/', PostingConfigurationsView.as_view(), name='update_posting_config'),  # /users/posting-configs/update/
]
