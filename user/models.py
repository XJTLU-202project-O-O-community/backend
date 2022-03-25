from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
# Create your models here.


class UserAccount(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32)

    #存入的密码经过md5加密（前端去加密）
    password = models.CharField(max_length=32)
    email = models.EmailField()


class User(models.Model):
    id = models.OneToOneField("user.UserAccount", on_delete=models.CASCADE, primary_key=True)
    photo = models.ImageField(upload_to="photo/", default='photo/default.jpg', null=False)
    username = models.CharField(max_length=32, null=False,unique=True)
    actual_name = models.CharField(max_length=32, null=True)
    gender = models.CharField(max_length=2, null=True)
    birth = models.DateField(null=True)
    signature = models.CharField(max_length=64, default="这个人很神秘，什么都没写", null=True)


class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser):
    '''账号表'''
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=32)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    photo = models.ImageField(upload_to="photo/", default='photo/default.jpg', null=False)
    actual_name = models.CharField(max_length=32, null=True)
    gender = models.CharField(max_length=2, null=True)
    birth = models.DateField(null=True)
    signature = models.CharField(max_length=64, default="这个人很神秘，什么都没写", null=True)
    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



