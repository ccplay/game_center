# -*- coding: utf-8 -*-
__author__ = 'me'

import pytz
from django.utils.timezone import datetime, timedelta
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import TokenAuthentication
from account.models import User as Player

class ExpiringTokenAuthentication(TokenAuthentication):

    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise AuthenticationFailed('User inactive or deleted')

        # This is required for the time comparison
        utc_now = datetime.utcnow()
        utc_now = utc_now.replace(tzinfo=pytz.utc)

        if token.created < utc_now - timedelta(hours=24):
            raise AuthenticationFailed('Token has expired')

        return token.user, token

class PlayerTokenAuthentication(TokenAuthentication):

    def authenticate_credentials(self, key):
        user, token = super(PlayerTokenAuthentication, self) \
            .authenticate_credentials(key)
        if user:
            user.__class__ = Player
        return (user, token)

