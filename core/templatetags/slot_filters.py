from django import template

register = template.Library()


@register.filter
def emp_exists(slot, emp):
    return slot.shift.emp_exists(emp)
