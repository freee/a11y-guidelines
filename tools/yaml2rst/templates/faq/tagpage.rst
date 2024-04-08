.. _faq-tag-{{ tag }}:

{% filter make_heading(1) -%}
{{ label }}
{%- endfilter %}

{% if lang == 'ja' -%}
{{ label }}のタグが付けられている記事の一覧です。
{%- elif lang == 'en' -%}
Here is a list of FAQ articles tagged with {{ label }}.
{%- endif %}

{% for item in articles %}
*  :ref:`faq-{{ item }}`
{%- endfor %}

{% if lang == 'ja' -%}
.. translated:: true
{% endif %}
