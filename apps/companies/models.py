from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import Owner
from apps.common.models.core import CoreModel


class Company(CoreModel):
    name = models.CharField(
        verbose_name=_("Название"), max_length=255, help_text=_("Имя Комании")
    )
    owner = models.ForeignKey(
        Owner, on_delete=models.CASCADE, verbose_name=_("Владелец")
    )
    industry = models.CharField(
        verbose_name=_("Индустрия"), max_length=100, help_text=_("Промышленность")
    )
    address = models.CharField(
        verbose_name=_("Адрес"), max_length=500, help_text=_("Адрес компании")
    )
    phone = models.CharField(
        verbose_name=_("Номер телефона"), max_length=15, help_text=_("Телефонный номер")
    )
    email = models.EmailField(verbose_name=_("Почта"), help_text=_("Электронная почта"))
    website = models.URLField(verbose_name=_("Веб-сайт"), help_text=_("Сайт компании"))
    established_date = models.DateField(
        verbose_name=_("Дата основания"), help_text=_("Дата основания компании")
    )

    class Meta:
        verbose_name = _("Компания")
        verbose_name_plural = _("Компании")

    def __str__(self):
        return self.name
