{% for impl in check.implementations -%}
{% filter make_heading(check_heading_level + 1) -%}
{%- if lang == 'ja' -%}
実装方法の例：{{ impl.title }}
{%- elif lang == 'en' -%}
Implementation Example: {{ impl.title }}
{%- endif -%}
{%- endfilter %}

{% for method in impl.methods -%}
{{ method.platform }}
   {{ method.method | indent(3) }}
{% endfor %}
{% endfor %}
