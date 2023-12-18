.. _faq-tag-{{ tag }}:

{% filter make_heading(1) -%}
{{ label }}
{%- endfilter %}

{% for item in articles %}
*  :ref:`faq-{{ item }}`
{%- endfor %}


