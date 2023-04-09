from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, insta, password=None, is_verified=False, allow_crypto=False, allow_bank=False, **extra_fields):
        if not insta:
            raise ValueError("insta is required")
        user = self.model(insta=insta, is_verified=is_verified, allow_crypto=allow_crypto, allow_bank=allow_bank, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(
                password=password,
                insta="admin",
                is_verified=True,
                **extra_fields
            )
