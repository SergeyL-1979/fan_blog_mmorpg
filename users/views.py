from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from .models import CustomUser
from .forms import UserForm
from board.models import Advertisement


class UserProfile(LoginRequiredMixin, ListView):
    """Кабинет пользователя"""
    model = CustomUser
    template_name = 'users/profile.html'
    context_object_name = 'profile'
    login_url = '/accounts/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = CustomUser.objects.get(username=self.request.user)
        context['ads'] = Advertisement.objects.filter(user__advertisement__in=self.request.user)
        # print(self.request.user.email)
        # print(CustomUser.objects.filter(email=self.request.user.email).exclude(username=self.request.user.username))
        return context

    def handle_response(self, post, username, message):
        user = get_object_or_404(CustomUser, username=username)
        post.responses.remove(user)
        messages.info(self.request, message)

    def post(self, request, *args, **kwargs):
        if request.POST.get('accept_response'):
            accept_data = request.POST.get('accept_response').split(' ')
            post = get_object_or_404(Advertisement, id=accept_data[-1])
            self.handle_response(post, accept_data[0], 'Вы приняли отклик!')
        elif request.POST.get('deny_response'):
            deny_data = request.POST.get('deny_response').split(' ')
            post = get_object_or_404(Advertisement, id=deny_data[-1])
            self.handle_response(post, deny_data[0], 'Вы отклонили отклик!')
        return redirect('profile')

    # def post(self, request, *args, **kwargs):
    #     """Работа формы"""
    #     # Принять отклик
    #     if request.POST.get('accept_response'):
    #         accept_data = request.POST.get('accept_response').split(' ')
    #         post = Advertisement.objects.get(id=accept_data[-1])
    #         user = CustomUser.objects.get(username=accept_data[0])
    #         post.responses.remove(user)
    #         post.accepted_responses.add(user)
    #         messages.info(request, 'Вы приняли отклик!')
    #     # Отклонить отклик
    #     elif request.POST.get('deny_response'):
    #         deny_data = request.POST.get('deny_response').split(' ')
    #         post = Advertisement.objects.get(id=deny_data[-1])
    #         user = CustomUser.objects.get(username=deny_data[0])
    #         post.responses.remove(user)
    #         messages.info(request, 'Вы отклонили отклик!')
    #     return redirect('profile')


class UserProfileEdit(LoginRequiredMixin, UpdateView):
    """Кабинет пользователя"""
    form_class = UserForm
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('profile')
    login_url = '/accounts/login/'

    def get_object(self, **kwargs):
        """Метод get_object чтобы получить информацию об
           объекте который мы собираемся редактировать"""
    #     obj = CustomUser.objects.get(username=self.request.user)
    #     return obj
        return get_object_or_404(CustomUser, username=self.request.user)
