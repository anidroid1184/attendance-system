from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    if hasattr(field, 'as_widget'):  # Asegúrate de que es un campo de formulario
        return field.as_widget(attrs={"class": css_class})
    return field  # Devuelve el valor original si no es un campo de formulario