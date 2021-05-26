from django import forms
from django import template
from django.forms import BoundField
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from django.conf import settings

register = template.Library()

BULMA_COLUMN_COUNT = 1

BULMA_FIELD_TEMPLATE = getattr(settings, "BULMA_FIELD_TEMPLATE", "bulma/forms/field_include.html")
BULMA_FIELD_WRAPPER_TEMPLATE = getattr(settings, "BULMA_FIELD_WRAPPER_TEMPLATE", "bulma/forms/field.html")
BULMA_FORM_TEMPLATE = getattr(settings, "BULMA_FORM_TEMPLATE", "bulma/forms/form.html")
BULMA_FORMSET_TEMPLATE = getattr(settings, "BULMA_FORMSET_TEMPLATE", "bulma/forms/formset.html")


@register.simple_tag
def font_awesome():
    """
    The latest FontAwesome CDN link.
    """
    cdn_link = (
        '<link rel="stylesheet" '
        'href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" '
        'integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" '
        'crossorigin="anonymous">'
    )
    return mark_safe(cdn_link)


@register.filter
def bulma(element):
    return bulma(element, label='', single_value='')


@register.simple_tag
def bulma(element, label='', value='', single_value=''):
    markup_classes = bulma_markup_classes(label, value, single_value)
    return render(element, markup_classes)


@register.simple_tag
def bulma_markup_classes(_element, label='', value='', single_value=''):
    markup_classes = {'label': label, 'value': value, 'single_value': single_value}
    return markup_classes


@register.filter
def bulma_inline(element):
    return bulma_inline(element, label='sr-only', single_value='')


@register.simple_tag
def bulma_inline(element, label='', value='', single_value=''):
    markup_classes = bulma_inline_markup_classes(label, value, single_value)
    return render(element, markup_classes)


@register.simple_tag
def bulma_inline_markup_classes(_element, label='', value='', single_value=''):
    markup_classes = {'label': 'sr-only', 'value': value, 'single_value': single_value}
    if label:
        if label not in markup_classes['label']:
            markup_classes['label'] += " %s" % label
    return markup_classes


@register.filter
def bulma_horizontal(element, label_cols='is-2'):
    return bulma_horizontal(element, label_cols=label_cols)


@register.simple_tag
def bulma_horizontal(element, label_cols='is-2', value='', single_value=''):
    markup_classes = bulma_horizontal_markup_classes(label_cols, value, single_value)
    return render(element, markup_classes)


@register.simple_tag
def bulma_horizontal_markup_classes(_element, label_cols='is-2', value='', single_value=''):
    markup_classes = {'label': label_cols, 'value': value, 'single_value': single_value}

    for cl in label_cols.split(' '):
        splitted_class = cl.split('-')

        try:
            value_nb_cols = int(splitted_class[-1])
        except ValueError:
            value_nb_cols = BULMA_COLUMN_COUNT

        if value_nb_cols >= BULMA_COLUMN_COUNT:
            splitted_class[-1] = str(BULMA_COLUMN_COUNT)
        else:
            offset_class = cl.split('-')
            offset_class[-1] = 'offset-' + str(value_nb_cols)
            splitted_class[-1] = str(BULMA_COLUMN_COUNT - value_nb_cols)
            markup_classes['single_value'] += ' ' + '-'.join(offset_class)
            markup_classes['single_value'] += ' ' + '-'.join(splitted_class)

        markup_classes['value'] += ' ' + '-'.join(splitted_class)
    return markup_classes


@register.filter
def add_input_classes(field):
    if not is_checkbox(field) and not is_multiple_checkbox(field) \
            and not is_radio(field) and not is_file(field):
        field_classes = field.field.widget.attrs.get('class', '')
        field_classes += ' control'
        field.field.widget.attrs['class'] = field_classes


def render(element, markup_classes):
    if isinstance(element, BoundField):
        templ = get_template(BULMA_FIELD_WRAPPER_TEMPLATE)
        context = {'field': element,
                   'classes': markup_classes, 'form': element.form}
    else:
        has_management = getattr(element, 'management_form', None)
        if has_management:

            templ = get_template(BULMA_FORMSET_TEMPLATE)
            context = {'formset': element, 'classes': markup_classes}
        else:

            templ = get_template(BULMA_FORM_TEMPLATE)
            context = {'form': element, 'classes': markup_classes}

    return templ.render(context)


@register.filter
def widget_type(field):
    return field.field.widget


@register.filter
def is_select(field):
    return isinstance(field.field.widget, forms.Select)


@register.filter
def is_multiple_select(field):
    return isinstance(field.field.widget, forms.SelectMultiple)


@register.filter
def is_textarea(field):
    return isinstance(field.field.widget, forms.Textarea)


@register.filter
def is_input(field):
    return isinstance(field.field.widget, (
        forms.TextInput,
        forms.NumberInput,
        forms.EmailInput,
        forms.PasswordInput,
        forms.URLInput
    ))


@register.filter
def is_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxInput)


@register.filter
def is_multiple_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxSelectMultiple)


@register.filter
def is_radio(field):
    return isinstance(field.field.widget, forms.RadioSelect)


@register.filter
def is_file(field):
    return isinstance(field.field.widget, forms.FileInput)


@register.filter
def addclass(field, css_class):
    if len(field.errors) > 0:
        css_class += ' is-danger'
    field_classes = field.field.widget.attrs.get('class', '')
    field_classes += f' {css_class}'
    return field.as_widget(attrs={"class": field_classes})


@register.filter
def bulma_message_tag(tag):
    return {
        'error': 'danger'
    }.get(tag, tag)


@register.filter
def optgroups(field):
    values = tuple(str(val) for val in field.value()) if isinstance(field.value(), (list, tuple)) else (
    str(field.value()),)
    attrs = field.field.widget.attrs or {}

    return field.field.widget.optgroups(field.html_name, values, attrs)


@register.simple_tag
def field_template():
    return BULMA_FIELD_TEMPLATE


@register.simple_tag
def field_wrapper_template():
    return BULMA_FIELD_WRAPPER_TEMPLATE


@register.simple_tag
def form_template():
    return BULMA_FORM_TEMPLATE


@register.simple_tag
def formset_template():
    return BULMA_FORMSET_TEMPLATE
