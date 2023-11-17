from django.contrib import admin
from chef.models import Chef

# Register your models here.


class ChefAdmin(admin.ModelAdmin):
    list_display = ("user", "chef_name", "is_approved", "created_at")
    list_display_links = ("user", "chef_name")
    list_editable = ("is_approved",)


admin.site.register(Chef, ChefAdmin)
