from django import forms
from django.core.exceptions import ValidationError

from .calculation_logic import evaluate_expression


def math_expression_validator(value):
    re_rule = '0123456789+-*/() '

    for sim in value:
        if sim not in re_rule:
            raise ValidationError(
                'Недопустимый символ в математическом выражении'
            )

    try:
        evaluate_expression(value)
    except Exception:
        raise ValidationError(
            'Ошибка при вычислении математического выражения'
        )


class CalcForm(forms.Form):
    expression = forms.CharField(
        max_length=100,
        validators=[math_expression_validator],
        label='Введите математическое выражение',
    )
