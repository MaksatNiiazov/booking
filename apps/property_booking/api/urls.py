from django.urls import path

from api.property_booking.views import RecordListCreateView, RecordDetailView, CheckPriceRecordView

urlpatterns = [
    path('records/', RecordListCreateView.as_view(), name='record-list-create'),
    path('records/<uuid:pk>/', RecordDetailView.as_view(), name='record-detail'),
    path('records/check/', CheckPriceRecordView.as_view(), name='record_check'),
]
