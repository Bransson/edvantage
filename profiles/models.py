from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

import uuid



class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, phone_number, matric_no, password, **extra_fields):
        """
        Creates and saves a User with the given phone_number and password.
        """
        if not phone_number:
            raise ValueError('The given phone number must be set')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, phone_number, matric_no, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, phone_number, matric_no, password, **extra_fields)

    def create_superuser(self, username, email, phone_number, matric_no, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')        
        return self._create_user(username, email, phone_number, matric_no, password, **extra_fields)


LevelChoices =(("100Level","100Level"),("200Level","200Level"),("300Level","300Level"),("400Level","400Level"),("500Level","500Level"),)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=100, unique=True)
    matric_no = models.CharField(max_length=13, null = True, blank=True, unique=True)
    phone_number = models.CharField(_('phone number'),max_length=20, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    institution = models.CharField(max_length=100, blank=True, null=True)
    program_of_study = models.CharField(max_length=100, blank=True, null=True)
    academic_level = models.CharField(choices=LevelChoices, max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(default="default_image.jpg" ,upload_to="profile_pics/", blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)   
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),)    
    is_active = models.BooleanField(_('active'), default=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'email', 'matric_no']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name
    
    """
    before saving:
    if there a profile picture is been passed in and the profile object has one:
        then we wanna delete the picture from the object
    and if not:
        we wanna set the profile picture to the dafult one

    
    this works incase there was no previous profile picture or if you wanna change the profile picture

    """
    def save(self, *args, **kwargs):
        try:
            profile_object= CustomUser.objects.get(pk=self.pk)

            if self.profile_picture:

                if profile_object.profile_picture:
                    if profile_object.profile_picture.url != "/media/default_image.jpg":
                        profile_object.profile_picture.delete()

            else:
                self.profile_picture = 'default_image.jpg'
        except:
            pass

        return super(CustomUser, self).save(*args, **kwargs)



# @receiver(user_signed_up)
# def populate_profile(sociallogin, user, **kwargs):


#     # if sociallogin.account.provider == 'facebook':
#     #     user_data = user.socialaccount_set.filter(provider='facebook')[0].extra_data
#     #     picture_url = "http://graph.facebook.com/" + sociallogin.account.uid + "/picture?type=large"
#     #     phone_number = user_data['phone_number']
#     #     full_name = user_data['name']

#     if sociallogin.account.provider == 'google':
#         user_data = user.socialaccount_set.filter(provider='google')[0].extra_data
#         picture_url = user_data['picture']
#         phone_number = user_data['phone_number']
#         # username = user_data['given_name']
#         # # full_name = user_data['name']
#         first_name = user_data['given_name']
#         last_name = user_data['family_name']
        

#     # cu = CustomUser(username=username, phone_number=phone_number, profile_picture=picture_url, first_name=first_name, last_name=last_name, is_active=True)
#     # cu.save()
#         cu= CustomUser.objects.filter(phone_number=phone_number, first_name=first_name, last_name=last_name).first()
#         # print(f"google account   phone_number: {phone_number},     first name: {first_name},  last name: {last_name}")
#         cu.is_active = True
#         cu.save()
