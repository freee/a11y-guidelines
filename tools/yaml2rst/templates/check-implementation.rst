{% for impl in check.implementations -%}
{% filter make_heading(check_heading_level + 1) -%}
実装方法の例：{{ impl.title }}
{%- endfilter %}

{% for ex in impl.examples -%}
{{ ex.platform }}
   {{ ex.method | indent(3) }}
{% endfor %}
{% endfor %}
