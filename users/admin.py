from django.contrib import admin
from .models import Profile
from .models import Feedback

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'id')

admin.site.register(Feedback)
