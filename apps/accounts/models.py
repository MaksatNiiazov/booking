import secrets

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.common import models as core_models
from apps.common.models import CoreModel


class UserManager(core_models.CoreManager, BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must give an email address")

        verification_code = secrets.token_urlsafe(64)

        user = self.model(
            email=email, verification_code=verification_code, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class UserAccount(PermissionsMixin, CoreModel, AbstractBaseUser):
    email = models.EmailField(verbose_name=_("Почта"), unique=True)
    first_name = models.CharField(verbose_name=_("Имя"), max_length=150, blank=True)
    last_name = models.CharField(verbose_name=_("Фамилия"), max_length=150, blank=True)
    is_staff = models.BooleanField(
        verbose_name=_("Статус сотрудника"),
        default=False,
        help_text=_(
            "Определяет, может ли пользователь войти на этот сайт администратора."
        ),
    )
    is_active = models.BooleanField(
        verbose_name=_("Активен"),
        default=True,
        help_text=_(
            "Указывает, следует ли считать этого пользователя активным. "
            "Снимите этот флажок вместо удаления учетных записей."
        ),
    )
    date_joined = models.DateTimeField(
        verbose_name=_("Дата присоединения"), default=timezone.now
    )
    phone_number = models.CharField(
        verbose_name=_("Номер телефона"), max_length=15, blank=True, null=True
    )
    address = models.CharField(
        verbose_name=_("Адрес"), max_length=500, blank=True, null=True
    )
    email_verified = models.BooleanField(
        verbose_name=_("Верификация почты"), default=False
    )
    otp = models.IntegerField(verbose_name=_("OTP"), blank=True, null=True)
    verification_code = models.CharField(
        verbose_name=_("Код подтверждения"), max_length=64, blank=True, null=True
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ("first_name", "last_name")

    def __str__(self):
        return self.email

    def get_short_name(self) -> str:
        return str(self.email)

    def get_full_name(self) -> str:
        if self.first_name and self.last_name:
            full_name = f"{self.first_name} {self.last_name} <{self.email}>"
        else:
            full_name = self.get_short_name()
        return full_name

    @property
    def notification_salutation(self):
        if self.first_name and self.last_name:
            salutation = f"{self.first_name} {self.last_name}"
        else:
            salutation = _("Уважаемый клиент")
        return salutation


class Owner(CoreModel):
    user = models.OneToOneField(
        UserAccount,
        on_delete=models.PROTECT,
        related_name="owner",
        verbose_name=_("Пользователь"),
    )
    inn = models.CharField(max_length=123, verbose_name=_("ИНН"))

    def __str__(self):
        return self.user.get_short_name()

    class Meta:
        verbose_name = _("Владелец")
        verbose_name_plural = _("Владельцы")


