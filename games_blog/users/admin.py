from blog.models import Feedback
from django.contrib import admin
from users.models import Profile


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "birth_date", "slug")
    list_display_links = ("user", "slug")


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("email", "ip_address", "user")
    list_display_links = ("email", "ip_address")



