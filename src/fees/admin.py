from django.contrib import admin

from fees.models import Collect, Payment

admin.site.register(Payment)
admin.site.register(Collect)
