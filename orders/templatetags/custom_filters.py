from django import template

register = template.Library()

@register.filter
def dict_get(d, key):
    """Get dictionary value safely in templates"""
    if isinstance(d, dict):
        return d.get(key, "")
    return ""

@register.filter
def get_field(form, field_name):
    """Get a field from form by name in templates"""
    try:
        return form[field_name]
    except KeyError:
        return None

@register.filter
def replace_underscore(value):
    return value.replace("_", " ").title()