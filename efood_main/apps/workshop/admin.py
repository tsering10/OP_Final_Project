from django.contrib import admin
from .models import Workshop

# Register your models here.


class WorkshopAdmin(admin.ModelAdmin):
    list_display = (
        "chef",
        "title",
        "description",
        "date",
        "capacity",
        "price",
        "address",
    )


admin.site.register(Workshop, WorkshopAdmin)
