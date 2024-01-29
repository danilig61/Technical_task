import logging
from datetime import datetime, timezone

from django.contrib.auth import get_user_model
from django.shortcuts import render


from rest_framework import viewsets, generics, permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Folder, Page, Record, FolderPermission, PagePermission, RecordPermission
from .serializer import FolderSerializer, PageSerializer, RecordSerializer, PagePermissionSerializer, \
    RecordPermissionSerializer, FolderPermissionSerializer, UserSerializer

logger = logging.getLogger(__name__)

logging.basicConfig(filename='logs.log', level=logging.INFO)

class CreateUserView(CreateAPIView):
    model = get_user_model()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def form_valid(self, form):
        logger = logging.getLogger(__name__)
        ip_address = self.request.META.get('REMOTE_ADDR')
        user_agent = self.request.META.get('HTTP_USER_AGENT')
        timestamp = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        user_id = self.user.id if self.user else None

        log_message = f"User authenticated - IP: {ip_address}, User-Agent: {user_agent}, Time: {timestamp}, User ID: {user_id}"
        logger.info(log_message)

        response = super().form_valid(form)
        return response


class FolderAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100


class FolderAPIList(generics.ListCreateAPIView):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
    pagination_class = FolderAPIListPagination

    def perform_create(self, serializer):
        folder = serializer.save()
        user = self.request.user
        log_massage = f"ID пользователя в БД: {user.id}, Время: {datetime.now()}  ,ID записи в БД: {folder.id} ,Статус: CREATED"
        logger.info(log_massage)



class FolderAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
    def perform_update(self, serializer):
        folder = serializer.save()
        user = self.request.user
        log_massage = f"ID пользователя в БД: {user.id}, Время: {datetime.now()}  ,ID записи в БД: {folder.id} , Статус: UPDATE"
        logger.info(log_massage)


class FolderAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        user = self.request.user
        log_massage = f"ID пользователя в БД: {user.id}, Время: {datetime.now()}  ,ID записи в БД: {instance.id} , Статус: DELETE"
        logger.info(log_massage)


class PageAPIListPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 200


class PageAPIList(generics.ListCreateAPIView):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    pagination_class = PageAPIListPagination
    def perform_create(self, serializer):
        page = serializer.save()
        user = self.request.user
        log_massage = f"ID пользователя в БД: {user.id}, Время: {datetime.now()}  ,ID записи в БД: {page.id} , Статус: CREATE"
        logger.info(log_massage)


class PageAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    def perform_update(self, serializer):
        page = serializer.save()
        user = self.request.user
        log_massage = f"ID пользователя в БД: {user.id}, Время: {datetime.now()}  ,ID записи в БД: {page.id} , Статус: UPDATE"
        logger.info(log_massage)


class PageAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        user = self.request.user
        log_massage = f"ID пользователя в БД: {user.id}, Время: {datetime.now()}  ,ID записи в БД: {instance.id} , Статус: DELETE"
        logger.info(log_massage)



class RecordAPIListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class RecordAPIList(generics.ListCreateAPIView):
    queryset = Record.objects.filter(is_deleted=False)
    serializer_class = RecordSerializer
    pagination_class = RecordAPIListPagination
    def perform_create(self, serializer):
        record = serializer.save()
        user = self.request.user
        log_massage = f"ID пользователя в БД: {user.id}, Время: {datetime.now()}  ,ID записи в БД: {record.id} , Статус: CREATE"
        logger.info(log_massage)



class RecordAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Record.objects.filter(is_deleted=False)
    serializer_class = RecordSerializer

    def perform_update(self, serializer):
        record = serializer.save()
        user = self.request.user
        log_massage = f"ID пользователя в БД: {user.id}, Время: {datetime.now()}  ,ID записи в БД: {record.id} , Статус: UPDATE"
        logger.info(log_massage)


class RecordAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Record.objects.filter(is_deleted=False)
    serializer_class = RecordSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        user = self.request.user
        log_massage = f"ID пользователя в БД: {user.id}, Время: {datetime.now()}  ,ID записи в БД: {instance.id} , Статус: DELETE"
        logger.info(log_massage)


class FolderPermissionViewSet(viewsets.ModelViewSet):
    queryset = FolderPermission.objects.all()
    serializer_class = FolderPermissionSerializer
    permission_classes = [permissions.IsAuthenticated]


class PagePermissionViewSet(viewsets.ModelViewSet):
    queryset = PagePermission.objects.all()
    serializer_class = PagePermissionSerializer
    permission_classes = [permissions.IsAuthenticated]


class RecordPermissionViewSet(viewsets.ModelViewSet):
    queryset = RecordPermission.objects.all()
    serializer_class = RecordPermissionSerializer
    permission_classes = [permissions.IsAuthenticated]


