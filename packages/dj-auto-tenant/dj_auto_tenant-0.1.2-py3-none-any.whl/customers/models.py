# pylint: skip-file
from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
import uuid
class Client(TenantMixin):
    """Client model for creating new tenents."""
    dc_tenant_uuid = models.UUIDField(default=uuid.uuid4, editable=True, primary_key=False)
    name = models.CharField(max_length=100)
    paid_until =  models.DateField(blank=True,null = True)
    on_trial = models.BooleanField(default = True)
    created_on = models.DateField(auto_now_add=True)
    trial_period = models.PositiveSmallIntegerField(default = 15,
    help_text="Number of days for trial")
    active = models.BooleanField(default = True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

class Domain(DomainMixin):
    """domain model to store domain name"""
    pass
