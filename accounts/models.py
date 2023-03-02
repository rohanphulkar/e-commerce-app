from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin


class MyAccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            email=self.normalize_email(email),
            # username=username,
        )

        user.set_password(password)

        # may have to add 'using=self._db' parameter.
        user.save()
        return user

    def create_superuser(self, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            # username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_verified = True
        user.save()
        return user


class User(AbstractBaseUser,PermissionsMixin):
    first_name = models.CharField(max_length=50,blank=True,null=True)
    last_name = models.CharField(max_length=50,blank=True,null=True)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    image = models.ImageField(upload_to="user/profile/",blank=True,null=True)
    phone = models.CharField(max_length=12,null=True, blank=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
            return self.is_admin

    def has_module_perms(self, app_label):
            return self.is_admin

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_addresse")
    address_line_1 = models.CharField(max_length=100,null=True, blank=True)
    address_line_2 = models.CharField(max_length=100,null=True,blank=True)
    pincode = models.CharField(max_length=7,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    state = models.CharField(max_length=2,null=True,blank=True)

    def __str__(self):
        return self.user.email