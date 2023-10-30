from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Field, HTML, Column, MultiField

from mmorpg.models import Ad, Respond, Category
from django.forms.widgets import Textarea
# from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class AdFormList(forms.ModelForm):

    class Meta:
        model = Ad
        fields = ['author', 'category', 'title', 'description']
        labels = {'author': 'Author:', 'category': 'Category:', 'title': 'Title:', 'description': 'Description:'}


class AdFormCreate(forms.ModelForm):
    title = forms.CharField(max_length=150)
    # description = forms.CharField(widget=CKEditorWidget())
    description = forms.CharField(widget=CKEditorUploadingWidget())
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Ad
        fields = ['title', 'category', 'description']
        labels = {'title': 'Title:', 'category': 'Category:', 'description': 'Description:'}

    # def __init__(self, *args, **kwargs):
    #     super(AdFormCreate, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_method = 'post'
    #     self.helper.layout = Layout(
    #         Row(
    #             Field('title', css_class='col-md-3 form-control'),
    #             Field('category', column="2", type="checkbox", css_class='form-check-input'),
    #         ),
    #         Row(
    #             Field('description', css_class='col-md-12'),
    #         )
    #     )
    #
    #     self.helper.add_input(Submit('submit', 'Add post', css_class='btn btn-success'))


class AdFormUpdate(forms.ModelForm):
    # в класс мета как обычно надо написать модель по которой будет строится форма и нужные нам поля. Мы уже делали
    # что-то похожее с фильтрами.
    title = forms.CharField(max_length=150)
    # description = forms.CharField(widget=CKEditorWidget())
    description = forms.CharField(widget=CKEditorUploadingWidget())
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Ad
        fields = ['title', 'category', 'description']
        labels = {'title': 'Title:', 'category': 'Category:', 'description': 'Description:'}

    # def __init__(self, *args, **kwargs):
    #     super(AdFormUpdate, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_method = 'post'
    #     self.helper.layout = Layout(
    #         Row(
    #             Field('title', css_class='col-md-3 form-control'),
    #             Field('category', type="checkbox", css_class='form-check-input'),
    #         ),
    #         Row(
    #             Field('description', css_class='col-md-12'),
    #         )
    #     )
    #
    #     self.helper.add_input(Submit('submit', 'Edit post', css_class='btn btn-success'))


class RespondFormCreate(forms.ModelForm):
    content = forms.CharField(widget=Textarea)

    class Meta:
        model = Respond
        fields = ['content']
        labels = {'content': 'Comment:'}

    def __init__(self, *args, **kwargs):
        super(RespondFormCreate, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Field('content', css_class='form-control'),
            ),
            HTML('<br>'),
        )

        self.helper.add_input(Submit('submit', 'Add comment', css_class='btn btn-success'))


class RespondFormList(forms.ModelForm):
    # В класс мета, как обычно, надо написать модель по которой будет строится форма и нужные нам поля.
    # Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = Respond
        fields = ['ad_post', 'author', 'content', 'approved']
        labels = {'ad_post': 'AdPost', 'author': 'Author:', 'content': 'Comment:', 'approved': 'Approved'}
