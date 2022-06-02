from django.contrib.auth.backends import ModelBackend
from inventory_management.models import MyUser
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _


class AuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, user_data=None, user_role=None):
        if username and password and user_data and user_role:
            admin_group, __ = Group.objects.get_or_create(name=_('Admins'))
            staff_group, __ = Group.objects.get_or_create(name=_('Mitarbeiter'))
            students_group, __ = Group.objects.get_or_create(name=_('Schüler'))
            guest_group, __ = Group.objects.get_or_create(name=_('Gäste'))

            try:
                user = MyUser.objects.get(person_id=user_data['PersonId'])

                if not user.is_active:
                    return None

                # Apply manual override
                if user.is_admin:
                    staff_group.user_set.remove(user)
                    students_group.user_set.remove(user)
                    admin_group.user_set.add(user)
                    guest_group.user_set.remove(user)
                elif user.is_staff:
                    staff_group.user_set.add(user)
                    students_group.user_set.remove(user)
                    admin_group.user_set.remove(user)
                    guest_group.user_set.remove(user)
                elif user.is_guest:
                    staff_group.user_set.remove(user)
                    students_group.user_set.remove(user)
                    admin_group.user_set.remove(user)
                    guest_group.user_set.add(user)
                else:
                    staff_group.user_set.remove(user)
                    students_group.user_set.add(user)
                    admin_group.user_set.remove(user)
                    guest_group.user_set.remove(user)

                user.set_password(password)
                user.first_name = user_data['FirstName']
                user.last_name = user_data['LastName']
                user.language = user_data['Language']
                user.profile_image_url = user_data['ProfileImageUrl']
                user.use_12_hour_time_format = user_data['Use12HTimeFormat']
                user.save()
            except MyUser.DoesNotExist:
                user = MyUser(person_id=user_data['PersonId'], username=username, first_name=user_data['FirstName'], last_name=user_data['LastName'], email=username + '@schule.bremen.de', language=user_data['Language'], profile_image_url=user_data['ProfileImageUrl'], use_12_hour_time_format=user_data['Use12HTimeFormat'])
                user.set_password(password)
                user.save()

            # Apply automatic override
            if user.allow_auto_role and not user.is_superuser:
                if user_role == 1:
                    user.is_guest = False
                    user.is_staff = True
                    user.is_admin = False
                    staff_group.user_set.add(user)
                elif user_role == 2:
                    user.is_guest = False
                    user.is_staff = False
                    user.is_admin = False
                    students_group.user_set.add(user)
                elif user_role == 3:
                    user.is_guest = False
                    user.is_staff = True
                    user.is_admin = True
                    admin_group.user_set.add(user)
                elif user_role == 4:
                    user.is_guest = True
                    user.is_staff = False
                    user.is_admin = False
                    guest_group.user_set.add(user)
                user.save()

            return user
        return None

    def get_user(self, user_id):
        try:
            return MyUser.objects.get(id=user_id)
        except MyUser.DoesNotExist:
            return None
