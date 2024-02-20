from django import template

register = template.Library()


@register.filter(name='add_id')
def add_id(subject_form, new_id):
    return subject_form.as_widget(attrs={'id': new_id})
