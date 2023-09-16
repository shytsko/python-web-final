from django.contrib.auth.mixins import AccessMixin


class LoginRequiredMixinEx(AccessMixin):
    """К действиям стандартного миксина добавлена проверка связи пользователя с организацией"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            self.permission_denied_message = "Требуется вход"
            return self.handle_no_permission()
        if request.user.company is None:
            self.permission_denied_message = "Текущий пользователь не связан с организацией"
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
