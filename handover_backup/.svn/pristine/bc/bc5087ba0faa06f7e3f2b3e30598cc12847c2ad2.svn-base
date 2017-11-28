# -*- coding: utf-8 -*-
from django import template

register = template.Library()

@register.simple_tag
def error_msg(error_list):
    if error_list:
        return error_list[0]
    return ''

@register.filter(name='dump_errors')
def dump_errors(errors): # 显示错误信息
    t = template.Template('''
        {% if errors %}
        <ul class="errors alert alert-error">
        {% for v in errors.itervalues %}
        <li>{{ v | join:'，' }}</li>
        {% endfor %}
        </ul>
        {% endif %}
    ''')
    c = template.Context(dict(errors = errors))

    return t.render(c)
