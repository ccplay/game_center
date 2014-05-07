# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from comment.models import Comment
from account.models import User as Player
from mobapi2.serializers import ModelWithRouterSerializer as ModelSerializer


class AccountRelatedProfileMixin(object):
    def get_profile_icon_url(self, obj):
        try:
            return obj.profile.icon.url
        except:
            pass
        return None

    def get_profile_email(self, obj):
        try:
            return obj.profile.email
        except:
            pass
        return None

    def get_profile_phone(self, obj):
        try:
            return obj.profile.phone
        except:
            pass
        return None

    def get_comment_count(self, obj):
        try:
            return Comment.objects.visible().filter(user=obj).count()
        except:
            return 0

    def get_profile_bookmark_count(self, obj):
        try:
            return obj.profile.bookmarks.published().count()
        except:
            pass
        return 0


class AccountDetailSerializer(AccountRelatedProfileMixin, ModelSerializer):

    email = serializers.SerializerMethodField('get_profile_email')
    phone = serializers.SerializerMethodField('get_profile_phone')
    icon = serializers.SerializerMethodField('get_profile_icon_url')

    comment_count = serializers.SerializerMethodField('get_comment_count')

    bookmark_count = serializers \
        .SerializerMethodField('get_profile_bookmark_count')

    class Meta:
        model = Player
        fields = (
            'username',
            'icon',
            'comment_count',
            'bookmark_count',
        )


class MultiAppAuthTokenSerializer(AuthTokenSerializer):

    username = serializers.CharField()
    password = serializers.CharField()

    app = serializers.CharField(default=None)

    def validate(self, attrs):
        app = attrs.get('app')
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password, app=app)

            if user:
                if not user.is_active:
                    raise serializers.ValidationError('User account is disabled.')
                attrs['user'] = user
                return attrs
            else:
                raise serializers.ValidationError('Unable to login with provided credentials.')
        else:
            raise serializers.ValidationError('Must include "username" and "password"')
