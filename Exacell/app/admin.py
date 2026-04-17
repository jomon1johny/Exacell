from django.contrib import admin
from .models import Sheet
from .models import CustomUser


admin.site.register(Sheet)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_approved', 'is_staff')
    list_filter = ('is_approved', 'is_staff')
    actions = ['approve_users']

    def approve_users(self, request, queryset):
        queryset.update(is_approved=True)