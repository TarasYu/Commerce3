from django import template


register = template.Library()

@register.filter(name= 'name_as_str')
def name_as_str(value):
   return value.__str__()