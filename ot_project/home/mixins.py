from django.urls import reverse_lazy


class ContextExMixin:
    """
    Миксин для объединения часто используемых параметров шаблона
    title - Заголовок страницы, по умолчанию - название организации текущего пользователя
    cancel_url - url для перехода по кнопке "Отмена", по умолчанию - страница организации текущего пользователя
    company - организация текущего пользователя
    """
    title = ''
    cancel_url = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = self.request.user.company
        context['title'] = context['company'].name + self.title
        context['cancel_url'] = self.get_cancel_url()
        return context

    def get_cancel_url(self):
        if self.cancel_url:
            return self.cancel_url
        if self.object:
            return self.object.get_absolute_url()
        return reverse_lazy('company')
