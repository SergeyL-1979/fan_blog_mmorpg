from django.contrib import admin
from django import forms
# from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from mmorpg.models import Category, Ad, Respond, AdCategory


class AdAdminForm(forms.ModelForm):
    # description = forms.CharField(widget=CKEditorWidget())
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Ad
        fields = '__all__'


class AdCategoryInline(admin.StackedInline):
    model = AdCategory
    extra = 1


class AdAdmin(admin.ModelAdmin):
    form = AdAdminForm
    inlines = [AdCategoryInline,]
    list_display = ['title', 'author', 'list_category', 'date_posted']
    # list_display_links = ['title', 'author']
    list_filter = ['title', 'author', 'date_posted']
    search_fields = ['title', 'author']


class RespondAdmin(admin.ModelAdmin):
    list_display = ['ad_post', 'author', 'date_posted', 'approved']
    # list_display_links = ('pk',)
    list_filter = ['ad_post__title', 'author', 'date_posted', 'approved']
    search_fields = ['ad_post__title', 'author']


admin.site.register(Category)
admin.site.register(Ad, AdAdmin)
admin.site.register(Respond, RespondAdmin)
