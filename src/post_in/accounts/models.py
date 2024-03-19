from django.contrib.auth.hashers import make_password, identify_hasher
from django.db.models import (EmailField, CharField, BooleanField, DateTimeField)
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, name=None, full_name=None,
                    is_active=True, is_staff=None, is_admin=None):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('User should have email!')
        if not password:
            raise ValueError('User should enter password!')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.is_active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, name=None):
        user = self.create_user(email, name=name, password=password,
                                is_staff=True, is_admin=True)
        return user

    def create_staffuser(self, email, password=None, name=None):
        user = self.create_user(email, name=name, password=password,
                                is_staff=True, is_admin=False)
        return user


class User(AbstractBaseUser):
    email = EmailField(max_length=255, unique=True)
    name = CharField(max_length=255, blank=True, null=True)
    full_name = CharField(max_length=255, blank=True, null=True)
    staff = BooleanField(default=False)
    is_active = BooleanField(default=True)
    admin = BooleanField(default=False)
    timestamp = DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_short_name(self):
        """if not name return email"""
        if self.name:
            return self.name
        else:
            return self.email

    def get_full_name(self):
        """if not fullname return email"""
        if self.full_name:
            return self.full_name
        else:
            return self.email

    def has_perm(self, perm, obj=None):
        """give permission"""
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    def save(self, *args, **kwargs):
        """if the password is not hashed, then we hash password it with standart function -- make_password;
         in the portable case we check its algorithm with function identify_hasher"""
        try:
            _alg = identify_hasher(self.password)
        except ValueError:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

