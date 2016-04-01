from django.contrib import admin

from autostew_web_users.models import SteamUser, SafetyClass


@admin.register(SteamUser)
class SteamUserAdmin(admin.ModelAdmin):
    list_filter = ['safety_class']
    list_display = [
        'display_name',
        'steam_id',
        'elo_rating',
        'safety_rating',
        'safety_class',
    ]
    search_fields = ['display_name', 'steam_id']


@admin.register(SafetyClass)
class SafetyClassAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'order',
        'class_below',
        'raise_to_this_class_threshold',
        'drop_from_this_class_threshold'
    ]
