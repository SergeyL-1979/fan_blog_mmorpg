from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect
from django.db.models import Q
from django.views.generic import (
    ListView, DetailView, CreateView,
    TemplateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from mmorpg.models import Ad, Category, Respond, AdCategory
from mmorpg.forms import (
    AdFormList, AdFormCreate,
    AdFormUpdate, RespondFormCreate,
    RespondFormList
)


class AdList(ListView):
    model = Ad
    # template_name = 'mmorpg/ads_list.html'
    context_object_name = 'ads_list'
    ordering = ['-date_posted']
    paginate_by = 2
    # queryset = Ad.objects.order_by('-date_posted')
    # form_class = AdFormList

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now()
        # context['post_count'] = len(Ad.objects.all())
        # context['current_user'] = self.request.user
        context['categories'] = Category.objects.all()
        return context
    #
    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)
    #
    #     if form.is_valid():
    #         form.save()
    #     return super().get(request, *args, **kwargs)


class AdDetail(DetailView):
    model = Ad
    # template_name = 'mmorpg/ads_detail.html'
    context_object_name = 'ad'
    # queryset = Ad.objects.all()
    # form_class = RespondFormList

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user
        context['categories'] = Category.objects.all()
        # context['comment_list'] = Respond.objects.filter(post=self.kwargs['pk'])

        # i = 0
        # list_fh = []
        # list_sh = []
        # for cat in Category.objects.all():
        #     i += 1
        #     if i <= len(Category.objects.all())/2:
        #         list_fh.append(cat)
        #     else:
        #         list_sh.append(cat)
        # context['cat_fh'] = list_fh
        # context['cat_sh'] = list_sh
        return context


# class AdCreateView(LoginRequiredMixin, CreateView):
class AdCreateView(CreateView):
    model = Ad
    # template_name = 'mmorpg/ads_create.html'
    # context_object_name = 'ads_create'
    form_class = AdFormCreate

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), None)

    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     return super().form_valid(form)
    def form_valid(self, form):
        """ Создаем форму, но не отправляем его в БД, пока просто держим в памяти """
        fields = form.save(commit=False)
        """ Через request передаем недостающую форму, которая обязательно 
        делаем на моменте авторизации и создании прав стать автором """
        fields.post_author = User.objects.get(author_user=self.request.user)
        """ Наконец сохраняем в БД """
        fields.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['ads'] = Ad.objects.filter(category=self.object)
        # context['ads_category'] = Ad.objects.filter(category=id)

        # i = 0
        # list_fh = []
        # list_sh = []
        # for cat in Category.objects.all():
        #     i += 1
        #     if i <= len(Category.objects.all())/2:
        #         list_fh.append(cat)
        #     else:
        #         list_sh.append(cat)
        # context['cat_fh'] = list_fh
        # context['cat_sh'] = list_sh
        return context


# class AdUpdateView(LoginRequiredMixin, UpdateView):
class AdUpdateView(UpdateView):
    model = Ad
    template_name = 'mmorpg/ads_update.html'
    context_object_name = 'post_detail'
    form_class = AdFormUpdate

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        # i = 0
        # list_fh = []
        # list_sh = []
        # for cat in Category.objects.all():
        #     i += 1
        #     if i <= len(Category.objects.all())/2:
        #         list_fh.append(cat)
        #     else:
        #         list_sh.append(cat)
        # context['cat_fh'] = list_fh
        # context['cat_sh'] = list_sh
        return context


# class AdDeleteView(LoginRequiredMixin, DeleteView):
class AdDeleteView(DeleteView):
    model = Ad
    template_name = 'mmorpg/ads_delete.html'
    context_object_name = 'post'
    success_url = 'mmorpg:ads_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        # i = 0
        # list_fh = []
        # list_sh = []
        # for cat in Category.objects.all():
        #     i += 1
        #     if i <= len(Category.objects.all())/2:
        #         list_fh.append(cat)
        #     else:
        #         list_sh.append(cat)
        # context['cat_fh'] = list_fh
        # context['cat_sh'] = list_sh
        return context


class SearchResultsListView(ListView):  # search
    model = Ad
    context_object_name = 'posts'
    template_name = 'mmorpg/search_results.html'

    def get_queryset(self):  # new
        query = self.request.GET.get('q')
        return Ad.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        context['categories'] = Category.objects.all()

        # i = 0
        # list_fh = []
        # list_sh = []
        # for cat in Category.objects.all():
        #     i += 1
        #     if i <= len(Category.objects.all())/2:
        #         list_fh.append(cat)
        #     else:
        #         list_sh.append(cat)
        # context['cat_fh'] = list_fh
        # context['cat_sh'] = list_sh
        return context


class SearchRespondResultsListView(ListView):  # search
    model = Respond
    context_object_name = 'comments'
    template_name = 'mmorpg/search_comments_results.html'

    def get_queryset(self):  # new
        query = self.request.GET.get('q')
        return Respond.objects.filter(
            Q(post__title__icontains=query) | Q(description__icontains=query)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        context['categories'] = Category.objects.all()

        # i = 0
        # list_fh = []
        # list_sh = []
        # for cat in Category.objects.all():
        #     i += 1
        #     if i <= len(Category.objects.all())/2:
        #         list_fh.append(cat)
        #     else:
        #         list_sh.append(cat)
        # context['cat_fh'] = list_fh
        # context['cat_sh'] = list_sh
        return context


class CategoryDetail(DetailView):
    """ Выводим список категорий. Далее фильтруем посты по категориям и делаем вывод всех постов
    относящихся к данной категории. """
    model = Category
    context_object_name = 'category_detail'
    # template_name = 'mmorpg/category_detail.html'
    # queryset = Category.objects.all()

    def get_context_data(self, **kwargs):
        id = self.kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        " Контекст отображение категорий в выпадающем статус баре "
        context['categories'] = Category.objects.all()
        " Контекст для списка постов в текущей категории. "
        context['ads_category'] = Ad.objects.filter(category=id)
        return context
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['categories'] = Category.objects.all()
    #     context['ads_category'] = Ad.objects.filter(category=self.object)
    #
    #     # i = 0
    #     # list_fh = []
    #     # list_sh = []
    #     # for cat in Category.objects.all():
    #     #     i += 1
    #     #     if i <= len(Category.objects.all())/2:
    #     #         list_fh.append(cat)
    #     #     else:
    #     #         list_sh.append(cat)
    #     # context['cat_fh'] = list_fh
    #     # context['cat_sh'] = list_sh
    #     return context


# class RespondCreateView(LoginRequiredMixin, CreateView):
class RespondCreateView(CreateView):
    model = Respond
    template_name = 'mmorpg/comment_create.html'
    context_object_name = 'comment'
    form_class = RespondFormCreate
    success_url = 'mmorpg:ads_list'

    def form_valid(self, form):
        form.instance.author = self.request.user
        id_post = self.kwargs.get('pk')
        form.instance.post = Ad.objects.get(pk=id_post)
        return super().form_valid(form)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     id_post = self.kwargs.get('pk')
    #     context['post'] = Ad.objects.get(pk=id_post)
    #     context['categories'] = Category.objects.all()
    #
    #     # i = 0
    #     # list_fh = []
    #     # list_sh = []
    #     # for cat in Category.objects.all():
    #     #     i += 1
    #     #     if i <= len(Category.objects.all()) / 2:
    #     #         list_fh.append(cat)
    #     #     else:
    #     #         list_sh.append(cat)
    #     # context['cat_fh'] = list_fh
    #     # context['cat_sh'] = list_sh
    #     return context


# class RespondListView(LoginRequiredMixin, ListView):
class RespondListView(ListView):
    model = Respond
    template_name = 'mmorpg/comments.html'
    context_object_name = 'comments'
    form_class = RespondFormList

    def get_queryset(self):
        queryset = Respond.objects.filter(post__author=self.request.user).order_by('post', '-date_posted')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        i = 0
        list_fh = []
        list_sh = []
        for cat in Category.objects.all():
            i += 1
            if i <= len(Category.objects.all()) / 2:
                list_fh.append(cat)
            else:
                list_sh.append(cat)
        context['cat_fh'] = list_fh
        context['cat_sh'] = list_sh
        return context


# class RespondDeleteView(LoginRequiredMixin, DeleteView):
class RespondDeleteView(DeleteView):
    model = Respond
    template_name = 'mmorpg/comment_delete.html'
    context_object_name = 'comment'
    success_url = 'comment_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        # i = 0
        # list_fh = []
        # list_sh = []
        # for cat in Category.objects.all():
        #     i += 1
        #     if i <= len(Category.objects.all())/2:
        #         list_fh.append(cat)
        #     else:
        #         list_sh.append(cat)
        # context['cat_fh'] = list_fh
        # context['cat_sh'] = list_sh
        return context


@login_required
def comment_approved(request, pk):
    comment = Respond.objects.get(pk=pk)
    comment.approved = True
    comment.save()
    return redirect(request.META.get('HTTP_REFERER'))


# ==================== FLATPAGES DJANGO =============================
# class HomePageView(TemplateView):
#     template_name = "flatpages/home.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['post_count'] = len(Ad.objects.all())
#         context['categories'] = Category.objects.all()
#
#         i = 0
#         list_fh = []
#         list_sh = []
#         for cat in Category.objects.all():
#             i += 1
#             if i <= len(Category.objects.all())/2:
#                 list_fh.append(cat)
#             else:
#                 list_sh.append(cat)
#         context['cat_fh'] = list_fh
#         context['cat_sh'] = list_sh
#         return context
#
#
# class AboutPageView(TemplateView):
#     template_name = "flatpages/about.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['post_count'] = len(Ad.objects.all())
#         context['categories'] = Category.objects.all()
#
#         i = 0
#         list_fh = []
#         list_sh = []
#         for cat in Category.objects.all():
#             i += 1
#             if i <= len(Category.objects.all()) / 2:
#                 list_fh.append(cat)
#             else:
#                 list_sh.append(cat)
#         context['cat_fh'] = list_fh
#         context['cat_sh'] = list_sh
#         return context
#
#
# class ContactsPageView(TemplateView):
#     template_name = "flatpages/contacts.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['post_count'] = len(Ad.objects.all())
#         context['categories'] = Category.objects.all()
#
#         i = 0
#         list_fh = []
#         list_sh = []
#         for cat in Category.objects.all():
#             i += 1
#             if i <= len(Category.objects.all()) / 2:
#                 list_fh.append(cat)
#             else:
#                 list_sh.append(cat)
#         context['cat_fh'] = list_fh
#         context['cat_sh'] = list_sh
#         return context
