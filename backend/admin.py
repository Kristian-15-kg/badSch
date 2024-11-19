from django.contrib import admin
from .models import Event, Vote

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'court_number', 'week_number', 'year')
    list_filter = ('week_number', 'year', 'court_number')
    search_fields = ('date', 'court_number')

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'timestamp', 'status')
    list_filter = ('status', 'event__week_number', 'event__year')
    search_fields = ('user__username', 'event__date') 