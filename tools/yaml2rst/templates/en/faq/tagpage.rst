.. _faq-tag-{{ tag }}:

{% filter make_heading(1) -%}
{{ label }}
{%- endfilter %}

{{ label }}のタグが付けられている記事の一覧です。

{% for item in articles %}
*  :ref:`faq-{{ item }}`
{%- endfor %}


