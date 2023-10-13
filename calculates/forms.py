import re

from django import forms
from django.core.exceptions import ValidationError


def math_expression_validator(value):
    re_rule = '[0123456789\\(\\)\\.\\+\\-\\*/]+'

    if not re.match(re_rule, value):
        raise ValidationError(
            'Недопустимый символ в математическом выражении'
        )

    try:
        eval(value)
    except (SyntaxError, TypeError, ZeroDivisionError, NameError):
        raise ValidationError(
            'Ошибка при вычислении математического выражения'
        )


class CalcForm(forms.Form):
    expression = forms.CharField(
        max_length=100,
        validators=[math_expression_validator],
        label='Введите математическое выражение',
    )
