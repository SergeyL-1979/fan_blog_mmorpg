from django.contrib import admin

from board.models import Category, Advertisement, Response, PrivatePage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'pk']


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'title', 'created_at', ]


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    # list_display = ['advertisement', 'user', 'text', 'created_at', ]
    list_display = ['text', 'created_at', 'display_accepted_responses']

    def display_accepted_responses(self, obj):
        return ", ".join([str(user) for user in obj.accepted_responses.all()])

    display_accepted_responses.short_description = 'Accepted Responses'


@admin.register(PrivatePage)
class PrivatePageAdmin(admin.ModelAdmin):
    list_display = ['user', ]


