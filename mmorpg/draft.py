class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Post
    # template_name = 'post_create.html'
    form_class = PostForm
    permission_required = ('news.add_post', )

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), None)

    # def handle_no_permission(self):
    #     if self.raise_exception or self.request.user.is_authenticated:
    #         raise PermissionDenied(self.get_permission_denied_message())
    #     return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

    """ Функция для кастомный валидации полей формы модели """
    def form_valid(self, form):
        """ Создаем форму, но не отправляем его в БД, пока просто держим в памяти """
        fields = form.save(commit=False)
        """ Через request передаем недостающую форму, которая обязательно 
        делаем на моменте авторизации и создании прав стать автором """
        fields.post_author = Author.objects.get(author_user=self.request.user)
        """ Наконец сохраняем в БД """
        fields.save()
        return super().form_valid(form)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
    #     context['time_now'] = datetime.now()
    #     return context