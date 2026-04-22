from django import template

register = template.Library()

@register.filter
def get_item(form, key):
    """Access form field by key dynamically in templates."""
    return form[key]