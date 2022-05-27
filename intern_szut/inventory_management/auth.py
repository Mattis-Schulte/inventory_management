from django.contrib.auth.backends import BaseBackend
from inventory_management.models import MyUser

class AuthenticationBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, user_data=None, user_role=None):
        if username and password and user_data and user_role:
            try:
                user = MyUser.objects.get(person_id=user_data['PersonId'])

                if not user.is_active:
                    return None

                if user.allow_auto_role and not user.is_superuser:
                    if user_role == 1:
                        user.is_guest = False
                        user.is_staff = True
                        user.is_admin = False
                    elif user_role == 2:
                        user.is_guest = False
                        user.is_staff = False
                        user.is_admin = False
                    elif user_role == 3:
                        user.is_guest = False
                        user.is_staff = True
                        user.is_admin = True
                    elif user_role == 4:
                        user.is_guest = True
                        user.is_staff = False
                        user.is_admin = False

                user.set_password(password)
                user.first_name = user_data['FirstName']
                user.last_name = user_data['LastName']
                user.language = user_data['Language']
                user.profile_image_url = user_data['ProfileImageUrl']
                user.use_12_hour_time_format = user_data['Use12HTimeFormat']

                user.save()
            except MyUser.DoesNotExist:
                user = MyUser(person_id=user_data['PersonId'], username=username, first_name=user_data['FirstName'], last_name=user_data['LastName'], email=username + '@schule.bremen.de', language=user_data['Language'], profile_image_url=user_data['ProfileImageUrl'], use_12_hour_time_format=user_data['Use12HTimeFormat'])
                if user_role == 1:
                    user.is_staff = True
                elif user_role == 3:
                    user.is_staff = True
                    user.is_admin = True
                elif user_role == 4:
                    user.is_guest = True
                user.set_password(password)
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return MyUser.objects.get(id=user_id)
        except MyUser.DoesNotExist:
            return None