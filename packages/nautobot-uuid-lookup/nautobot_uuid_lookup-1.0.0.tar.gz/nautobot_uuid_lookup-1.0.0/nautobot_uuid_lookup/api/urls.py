"""API Urls for nautobot_uuid_lookup."""

from django.urls import path

from .views import RedirectUUIDView

urlpatterns = [
    path('<uuid:pk>/', RedirectUUIDView.as_view(), name="RedirectUUIDView")
]
