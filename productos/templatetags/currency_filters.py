from django import template
from django.template.defaultfilters import floatformat

register = template.Library()

@register.filter(name='format_cop')
def format_cop(value):
    """
    Formatea un número como precio en pesos colombianos (COP)
    Ejemplo: 1000000 -> $1.000.000
    """
    try:
        value = float(value)
        # Formatear el número con puntos como separador de miles
        formatted = "{:,.0f}".format(value).replace(",", ".")
        return f"${formatted}"
    except (ValueError, TypeError):
        return value

@register.filter(name='multiply')
def multiply(value, arg):
    """
    Multiplica dos números
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
