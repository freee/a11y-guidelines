{% filter make_heading(2) -%}
Related Guidelines
{%- endfilter %}

{% for gl in guidelines -%}
*  {{ gl.category }}: :ref:`{{ gl.guideline }}`
{% endfor %}

