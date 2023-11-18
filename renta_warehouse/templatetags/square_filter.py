from django import template

register = template.Library()


@register.filter(name='square_less_10')
def square_filter(boxes):
    return [box for box in boxes if box['square'] < 10]


@register.filter(name='square_more_10')
def square_filter(boxes):
    return [box for box in boxes if box['square'] < 10]