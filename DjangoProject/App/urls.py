from re import I
from DjangoProject.urls import path
from App import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
    

schema_view = get_schema_view(
   openapi.Info(
      title="Project Management System",
      default_version='v1',
      description="Api's Documentation",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('create-user/', views.register_users , name='register-user'),
    path('create-member/', views.register_member , name='register-member'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/profile/', views.user_profile, name='user-profile'),
    path('client-project/', views.client_project, name='create-project'),
    path('project-detail/<int:pk>/', views.project_detail, name='project-detail'),
    path('general-teams/', views.general_team, name='general-teams'),
    path('team-details/<int:pk>/', views.team_detail, name='team-detail'),
    path('<int:pk>/project-task/', views.project_task, name='project-task'),
    path('task-detail/<int:pk>/', views.task_detail, name='task-detail'),
    
]