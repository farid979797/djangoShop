from .models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить объявление", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'contact'},
]

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.filter(parent_category=None)
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)
        context['menu'] = user_menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        if 'cat_selected' in context:
            subcats = Category.objects.filter(parent_category=context['cat_selected'])
            context['subcats'] = subcats
        return context
