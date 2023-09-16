from django.core.exceptions import PermissionDenied


class CompanyOwnerTestMixin:
    """
    Миксин для проверки, связан ли объект с организацией текущего пользователя.
    Класс объекта должен реализовывать метод get_owner_company_id, который возвращает id организации
    """

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user.company_id != obj.get_owner_company_id():
            raise PermissionDenied(f"Объект не принадлежит организации пользователя")
        return obj
