from django import forms
from django.core.exceptions import ValidationError

from .calculation_logic import ExpressionCalculation


def math_expression_validator(expression):
    """Валидация входного выражения"""
    re_rule = '^0123456789+-*/(). '

    for simvol in expression:
        if simvol not in re_rule:
            raise ValidationError(
                'Недопустимый символ в математическом выражении'
            )

    try:
        calculation = ExpressionCalculation(expression)
        calculation.get_result()
    except Exception:
        raise ValidationError(
            'Ошибка при вычислении математического выражения'
        )


class CalcForm(forms.Form):
    """Создание формы"""
    expression = forms.CharField(
        max_length=100,
        validators=[math_expression_validator],
        label='Введите математическое выражение',
    )
