from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Template filter to get a value from a dictionary by key.
    Usage: {{ my_dict|get_item:key_variable }}
    """
    return dictionary.get(key)
