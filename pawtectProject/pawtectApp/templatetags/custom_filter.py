from django import template

register = template.Library()

@register.filter
def get_answer(pet,question_id=None):
    return pet.get_answer(question_id)
