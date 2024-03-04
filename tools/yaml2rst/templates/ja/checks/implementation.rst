{% for impl in check.implementations -%}
{% filter make_heading(check_heading_level + 1) -%}
実装方法の例：{{ impl.title }}
{%- endfilter %}

{% for method in impl.methods -%}
{{ method.platform }}
   {{ method.method | indent(3) }}
{% endfor %}
{% endfor %}
