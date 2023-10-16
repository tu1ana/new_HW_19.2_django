from django import template

from config import settings

register = template.Library()


@register.filter()
def mymedia(value):
    if value:
        return f'{settings.MEDIA_URL}{value}'
    return f'/{settings.STATIC_URL}default-image.jpg'
    # return '/static/default-image.jpg'
