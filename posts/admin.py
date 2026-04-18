from django.contrib import admin
from .models import LunchPost, Profile

@admin.register(LunchPost)
class LunchPostAdmin(admin.ModelAdmin):
    list_display  = ('restaurant', 'name', 'meal', 'time', 'slots', 'joined', 'area', 'created_at')
    list_filter   = ('meal', 'area')
    search_fields = ('restaurant', 'name', 'area', 'note')
    ordering      = ('-created_at',)
    readonly_fields = ('created_at',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display  = ('user', 'bio')
    search_fields = ('user__username', 'bio')