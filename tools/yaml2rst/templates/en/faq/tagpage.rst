.. _faq-tag-{{ tag }}:

{% filter make_heading(1) -%}
{{ label }}
{%- endfilter %}

Here is a list of FAQ articles tagged with {{ label }}.

{% for item in articles %}
*  :ref:`faq-{{ item }}`
{%- endfor %}


