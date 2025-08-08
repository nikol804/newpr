from django import template

register = template.Library()


@register.filter
def mul(value, arg):
    """Умножает значение на аргумент."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def div(value, arg):
    """Делит значение на аргумент."""
    try:
        return float(value) / float(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0


@register.filter
def sub(value, arg):
    """Вычитает аргумент из значения."""
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def add(value, arg):
    """Складывает значение с аргументом."""
    try:
        return float(value) + float(arg)
    except (ValueError, TypeError):
        return 0
