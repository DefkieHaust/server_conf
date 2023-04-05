from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, insta, password=None, is_verified=False, **extra_fields):
        if not insta:
            raise ValueError("insta is required")
        user = self.model(insta=insta, is_verified=is_verified, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password, insta="admin", is_verified=True, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(password=password, insta=insta, is_verified=is_verified, **extra_fields)
