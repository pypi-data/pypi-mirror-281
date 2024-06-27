from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Client)
admin.site.register(Domain)

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('id', 'tenant', 'domain','is_primary')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name','dc_tenant_uuid', 'schema_name', 'is_active',
                    'created_on',)