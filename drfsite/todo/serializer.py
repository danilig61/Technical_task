from .models import Folder, Page, Record, FolderPermission, PagePermission, RecordPermission

from rest_framework import serializers
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('email', 'username', 'password', 'password_confirm')

    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Пароли не совпадают!")

        return data

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )

        return user


class FolderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Folder
        fields = "__all__"


class PageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Page
        fields = "__all__"


class RecordSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Record
        fields = "__all__"


class FolderPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FolderPermission
        fields = ['id', 'folder', 'user', 'can_read']


class PagePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagePermission
        fields = ['id', 'page', 'user', 'can_read', 'can_edit', 'can_create', 'can_delete']


class RecordPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordPermission
        fields = ['id', 'record', 'user', 'can_read', 'can_edit', 'can_create', 'can_delete']
