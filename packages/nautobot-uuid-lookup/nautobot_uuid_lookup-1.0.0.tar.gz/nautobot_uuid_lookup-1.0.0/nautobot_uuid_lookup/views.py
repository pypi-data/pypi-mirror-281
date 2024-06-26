"""Views for nautobot_uuid_lookup."""

from django.apps import apps
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import redirect
from packaging import version

from nautobot.apps.models import BaseModel

if version.parse(settings.VERSION) >= version.parse("2.0"):
    from nautobot.apps.utils import get_permission_for_model
    from nautobot.apps.models import RestrictedQuerySet
else:
    from nautobot.utilities.permissions import get_permission_for_model
    from nautobot.utilities.querysets import RestrictedQuerySet



@login_required
def redirect_uuid(request, pk):
    all_models = apps.get_models()
    uuid_models = []
    for model in all_models:
        if issubclass(model, BaseModel):
            uuid_models.append(model)
    for model in uuid_models:
        try:
            required_permission = get_permission_for_model(model, "view")
            if request.user.has_perm(required_permission):
                queryset = model.objects
                # additionally restrict object permissions if available
                if issubclass(queryset._queryset_class, RestrictedQuerySet):
                    queryset = queryset.restrict(request.user, "view")
                item = queryset.get(id=pk)
                return redirect(item.get_absolute_url())
        except ObjectDoesNotExist:
            continue
    raise Http404("No object with given UUID")
