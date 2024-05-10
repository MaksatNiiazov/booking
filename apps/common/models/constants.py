from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.common.models.core import SingletonModel


# class Constants(SingletonModel):
#     is_moder = models.BooleanField(verbose_name=_('Режим модерации'), blank=True, default=False)
#
#     class Meta:
#         verbose_name = _('Константа')
#         verbose_name_plural = _('Константы')
