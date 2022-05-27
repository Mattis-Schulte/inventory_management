from django.contrib.auth.backends import BaseBackend
from inventory_management.models import MyUser

class AuthenticationBackend(BaseBackend):
    def authenticate(self, request, person_id=None, user_name=None, first_name=None, last_name=None, user_role=None):
        if person_id and user_name and first_name and last_name and user_role:
            try:
                user = MyUser.objects.get(person_id=person_id)
                if not user.is_active:
                    return None
            except MyUser.DoesNotExist:
                user = MyUser(person_id=person_id, username=user_name, first_name=first_name, last_name=last_name, email=user_name + '@schule.bremen.de')
                if user_role == 1:
                    user.is_staff = True
                elif user_role == 3:
                    user.is_staff = True
                    user.is_admin = True
                elif user_role == 4:
                    user.is_guest = True
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return MyUser.objects.get(id=user_id)
        except MyUser.DoesNotExist:
            return None