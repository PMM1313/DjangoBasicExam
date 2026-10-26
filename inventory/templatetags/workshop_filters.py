from django import template

register = template.Library()

# simple but for showcase
@register.filter
def stock_status(equipment):
    if equipment.quantity < equipment.minimum_stock:
        return "Low stock"
    return "In stock"