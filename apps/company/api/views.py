from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from api.utils.validate import is_valid_uuid

from api.company.paginations import MyCustomPagination
from apps.accounts.models import Owner
from api.company.serializers import OwnerSerializer

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter


@extend_schema_view(
    post=extend_schema(
        description=_('URL для запроса создания владельцем'),
        summary=_('Создания владельца'),
    ),
)
class OwnerCreateView(generics.CreateAPIView):
    queryset = Owner.objects.all()
    model = Owner
    serializer_class = OwnerSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth'

    def post(self, request, *args, **kwargs):
        if Owner.objects.filter(user=request.user).exists():
            return Response(data={'detail': _('You already owner')}, status=HTTP_400_BAD_REQUEST)
        data = super().post(request, *args, **kwargs)
        return Response(status=HTTP_200_OK)


@extend_schema_view(
    get=extend_schema(
        description=_('URL получения списка людей которые хотят быть владельцем'),
        summary=_('Лист владельца')
    ),
)
class OwnerApplications(generics.ListAPIView):
    queryset = Owner.objects.filter(is_active=False).order_by('-created')
    pagination_class = MyCustomPagination
    serializer_class = OwnerSerializer
    permission_classes = [IsAdminUser]


@extend_schema_view(
    get=extend_schema(
        description=_('URL для подтверждения владельца'),
        summary=_('подтверждения владельца'),
        parameters=[
            OpenApiParameter(
                name='users_id',
                description=_('Users id'),
                type={'type': 'array', 'items': {'type': 'uuid'}},
                location=OpenApiParameter.QUERY,
            )
        ]
    ),
)
class ConfirmOwners(generics.GenericAPIView):
    queryset = Owner.objects.filter(is_active=False)
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        owners = request.query_params.getlist('users_id')
        if not all(list(map(is_valid_uuid, owners))):
            return Response({'detail': _('Неправильный UUID')}, status=HTTP_400_BAD_REQUEST)
        owners = Owner.objects.filter(user__uuid__in=owners).update(is_active=True)
        return Response(status=HTTP_200_OK)
