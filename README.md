## Fork of [Django Bulma (timonweb)](https://github.com/timonweb/django-bulma) 
This fork moves more functionality into the templates, instead of adding CSS in python code.  
It is also more extensible, since templates can be included and blocks can be overriden.

For the added functionality, look at section [New Additions](#new-additions)

# A Bulma Theme for Django Projects

![Django Bulma](https://raw.githubusercontent.com/timonweb/django-bulma/master/test_project/static/images/django-bulma-logo.png)

A Django base theme based on Bulma ([bulma.io](https://bulma.io/)). Bulma is a modern CSS framework based on Flexbox.

*** work in progress ***

## Installation

1. Install the python package django-bulma from pip

  ``pip install django-bulma``

  Alternatively, you can install download or clone this repo and call ``pip install -e .``.

2. Add to INSTALLED_APPS in your **settings.py**:

  `'bulma',`

3. If you want to use the provided base template, extend from **bulma/base.html**:

  ```
  {% extends 'bulma/base.html' %}

  {% block title %}Bulma Site{% endblock %}

  {% block content %}
    Content goes here...
  {% endblock content %}

  ```
  
4. If you want to customize bulma sass and your own components:

    4.1 Copy bulma static files into your project's **STATIC_ROOT**:

    ```
    python manage.py copy_bulma_static_into_project
    ```  
    You should see **bulma** dir appeared in your **STATIC_ROOT**. It contains
    two dirs:
    * **sass** - this is the place where you can put your own sass code and customize
    bulma variables
    * **css** - this is where compiled sass output goes, you should link this file
    in your base.html 

    4.2 Install npm packages for sass compilation to work:    
    
    ```
    python manage.py bulma install
    ```
    
    4.3 Start sass watch mode:
    ```
    python manage.py bulma start
    ```

5. For forms, in your templates, load the `bulma_tags` library and use the `|bulma` filters:

    ##### Example template
    
    ```django

    {% load bulma_tags %}

    {# Display a form #}

    <form action="/url/to/submit/" method="post">
       {% csrf_token %}
       {{ form|bulma }}
       <div class="field">
         <button type="submit" class="button is-primary">Login</button>
       </div>
       <input type="hidden" name="next" value="{{ next }}"/>
    </form>
    ```

## Included templates

**django-bulma** comes with:
* a base template,
* django core registration templates,

## Bugs and suggestions

If you have found a bug or if you have a request for additional functionality, please use the issue tracker on GitHub.

[https://github.com/nkay08/django-bulma/issues](https://github.com/nkay08/django-bulma/issues)

# New Additions
The form and fields can be rendered in exactly the same way as before. 
However, fields can now also be used by simply including a template. 
## Templates
- `bulma/forms/field.html`: The basic field template that is included by django-bulma's `form.html`
- `bulma/forms/field_include.html`: Can be included directly with a `with field=form.<your_field>` statement. Does NOT add markup classes, but they can be provided manually.
- `bulma/forms/bulma_field_include.html`: Can be included directly with a `with field=form.<your_field>` statement, and adds markup classes like the `bulma` template filter
- `bulma/forms/bulma_inline_field_include.html`: Can be included directly with a `with field=form.<your_field>` statement, and adds markup classes like the `bulma_inline` template filter
- `bulma/forms/bulma_horizontal_field_include.html`: Can be included directly with a `with field=form.<your_field>` statement, and adds markup classes like the `bulma_horizontal` template filter

You can customize the fields, e.g. by extending `bulma/forms/field_include.html` and overriding its blocks and then changing the respective setting.

## Settings
You can specify which templates `django-bulma` uses for rendering forms and fields, and thus allow extensibility and customization.
These affect `django-bulma`'s rendering template filters, but also all field templates that are prefixed with `bulma_`.

Options for `settings.py`:
- `BULMA_FIELD_TEMPLATE`: Specifies which field template is used by bulma rendering. Default `"bulma/forms/field_include.html"`.
- `BULMA_FIELD_WRAPPER_TEMPLATE`: Specifies which field wrapper template is used by bulma rendering. This wrapper coverts some context dicts to flat variables. Default `"bulma/forms/field.html"`.
- `BULMA_FORM_TEMPLATE`: Specifies which form template is used by bulma rendering. Default `"bulma/forms/form.html"`.
- `BULMA_FORMSET_TEMPLATE`: Specifies which formset template is used by bulma rendering. Default `"bulma/forms/formset.html"`. 
    
## Bulma CSS

- Inline icons: You can now generate inputs that have inline icons
    - Add `has-icons-left` or `has-icons-right` or both as `classes_value` when including or providing them as parameter when using the `bulma` template tag 
    - You can specify the icon css class with the context `icon_left_class` and `icon_right_class` (currently only possible when including template)


