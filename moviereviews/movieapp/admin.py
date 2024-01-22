from django.contrib import admin
from .models import *


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'avatar', 'time_create', 'time_update', 'is_worker', 'user_id', 'status')
    search_fields = ('id', 'user_id')
    list_editable = ('is_worker',)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'Review_title', 'Mark', 'Main_text', 'Moviee_id', 'user_id')
    search_fields = ('id', 'user_id')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Film)
admin.site.register(News)
admin.site.register(Review, ReviewAdmin)


