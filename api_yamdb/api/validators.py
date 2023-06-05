import re

from rest_framework.serializers import ValidationError


def check_username(value):
    value = value.lower()
    if value == 'me':
        raise ValidationError('Нельзя использовать этого пользователя')
    checked_value = re.match('^[\\w.@+-]+', value)
    if checked_value is None or checked_value.group() != value:
        raise ValidationError('Допускается использовать только буквы, цифры'
                              'и символы @ . + - _.')
    return value
