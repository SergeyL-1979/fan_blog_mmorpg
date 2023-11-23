from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views import generic, View

from .forms import ResponseForm
from .models import Advertisement, Response, Category


class AdListView(generic.ListView):
    model = Advertisement
    context_object_name = 'ads_list'


# class AdDetailView(generic.DetailView):
#     model = Advertisement
#     context_object_name = 'ads_detail'
#     form_class = ResponseForm
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # context['time_now'] = datetime.now()
#         " Отображение категорий в выпадающем статус баре "
#         context['category_name'] = Category.objects.all()
#         # context['comment_list'] = Response.objects.filter(comment_post=self.kwargs['pk'])
#         " Контекст для отображения категории в посте "
#         # context['post_category'] = PostCategory.objects.get(post=self.kwargs['pk']).category
#         " Тут создан фильтр если выбрано несколько категорий на один пост "
#         context['post_category'] = Category.objects.filter(advertisement=self.kwargs['pk'])
#         # context['form'] = self.get_form()
#         context['form'] = ResponseForm()
#         return context
class AdDetailView(View):
    # model = Advertisement
    # context_object_name = 'ads_detail'
    template_name = 'board/advertisement_detail.html'
    form_class = ResponseForm

    def get(self, request, pk, *args, **kwargs):
        advertisement = Advertisement.objects.get(pk=pk)
        category_name = Category.objects.all()
        post_category = Category.objects.filter(advertisement=pk)
        form = self.form_class()
        context = {
            'ads_detail': advertisement,
            'category_name': category_name,
            'post_category': post_category,
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form, pk)
        else:
            return self.form_invalid(form, pk)

    def form_valid(self, form, pk):
        response = form.save(commit=False)
        response.advertisement = Advertisement.objects.get(pk=pk)
        response.user = self.request.user
        response.save()
        return redirect('ads_detail', pk=pk)

    def form_invalid(self, form, pk):
        advertisement = Advertisement.objects.get(pk=pk)
        category_name = Category.objects.all()
        post_category = Category.objects.filter(advertisement=pk)
        context = {
            'ads_detail': advertisement,
            'category_name': category_name,
            'post_category': post_category,
            'form': form,
        }
        return render(self.request, self.template_name, context)

    def get_success_url(self):
        return reverse('ads_detail', kwargs={'pk': self.kwargs.get('pk')})


class CategoryDetail(generic.DetailView):
    model = Category
    # template_name = 'board/category_detail.html'
    context_object_name = 'category_detail'

    def get_context_data(self, **kwargs):
        id = self.kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        " Контекст отображение категорий в выпадающем статус баре "
        context['category_name'] = Category.objects.all()
        " Контекст для списка постов в текущей категории. "
        context['category_ads'] = Advertisement.objects.filter(category=id)
        " Контекст постов данной категории. "
        # context['post_category'] = PostCategory.objects.get(post=self.kwargs['pk']).category
        return context



