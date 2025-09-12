from django.contrib import admin

from fees.models import Payment, Collect

admin.site.register(Payment)
admin.site.register(Collect)
