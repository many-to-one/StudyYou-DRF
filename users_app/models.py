from django.db import models

from django.contrib.auth.models import(
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)    
from rest_framework_simplejwt.tokens import RefreshToken        


class CustomUserManager(BaseUserManager):

    def create_superuser(self, email, username, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, password, **other_fields)

    def create_user(self, email, username, password, **other_fields):

        if not email:
            raise ValueError('You must provide an email address')

        email = self.normalize_email(email)
        user = self.model(
            email=email, 
            username=username,
            **other_fields
            )
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    username=models.CharField(
        max_length=25,
        unique=True,
        null=True,
        db_index=True
    )
    email=models.EmailField(
        max_length=25,
        unique=True,
        null=True,
        db_index=True
    )
    congregation=models.CharField(
        max_length=250,
        null=True,
        db_index=True
    )
    language=models.CharField(
        max_length=5,
        null=True,
        db_index=True
    )
    groupe = models.CharField(
        max_length=5,
        null=True,
        db_index=True
    )
    admin = models.BooleanField(
        default=False,
    )
    editor = models.BooleanField(
        default=False,
        verbose_name=('Congregation menegment')
    )
    service = models.BooleanField(
        default=False,
        verbose_name=('Service (microphones, music, duty)')
    )
    leader = models.BooleanField(
        default=False,
        verbose_name=('Leader')
    )
    helper = models.BooleanField(
        default=False,
        verbose_name=('Helper (service, prayers)')
        )
    lector = models.BooleanField(
        default=False,
        )
    school_leader = models.BooleanField(
        default=False,
        )
    ministry_event = models.BooleanField(
        default=False,
        verbose_name=('Ministry (Leader of ministry meetings)')
        )
    report = models.BooleanField(
        default=False,
        verbose_name=('Report')
    )
    stand = models.BooleanField(
        default=False,
        verbose_name=('Ministry with Stand')
    )
    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(
        default=False
        )
    is_staff = models.BooleanField(
        default=False
        )
    is_active = models.BooleanField(
        default=False
        )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }