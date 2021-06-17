# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class EmailBackend(object):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # user = User.objects.get(email=username)
            user = User.objects.get(Q(username=username)| Q(email=username))
        except User.MultipleObjectsReturned:
            user = User.objects.filter(email=username).order_by('id').first()
        except User.DoesNotExist:
            return None

        if getattr(user, 'is_active') and user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
