from django import template
from django.utils.html import format_html

register = template.Library()

@register.filter(name='add_class_with_label')
def add_class_with_label(field, css_class):
    """
    Adds a CSS class to form fields and renders the field with its label in a unified manner.
    """
    # Add the CSS class to the field
    field_with_class = field.as_widget(attrs={"class": css_class})

    # Generate the label with a form-label class for styling
    label_html = field.label_tag(attrs={"class": "form-label"})

    # Wrap the label and input in a form-group div
    return format_html('<div class="form-group">{}</br>{}</div>', label_html, field_with_class)


# custom template tag to use in jinja to check user group appartenance
@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists() 
