from django.contrib import admin

from todo.views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

router = DefaultRouter()
router.register(r'folder-permissions', FolderPermissionViewSet, basename='folder-permissions')
router.register(r'page-permissions', PagePermissionViewSet, basename='page-permissions')
router.register(r'record-permissions', RecordPermissionViewSet, basename='record-permissions')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', CreateUserView.as_view()),
    path('api/', include(router.urls)),
    path('api/v1/folder/', FolderAPIList.as_view()),
    path('api/v1/folder/<int:pk>/', FolderAPIUpdate.as_view()),
    path('api/v1/folderdelete/<int:pk>/', FolderAPIDestroy.as_view()),
    path('api/v1/pages/', PageAPIList.as_view()),
    path('api/v1/pages/<int:pk>/', PageAPIUpdate.as_view()),
    path('api/v1/pagesdelete/<int:pk>/', PageAPIDestroy.as_view()),
    path('api/v1/records/', RecordAPIList.as_view()),
    path('api/v1/records/<int:pk>/', RecordAPIUpdate.as_view()),
    path('api/v1/recordsdelete/<int:pk>/', RecordAPIDestroy.as_view()),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),


]
