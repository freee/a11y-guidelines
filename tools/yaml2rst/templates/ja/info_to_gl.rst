{% filter make_heading(2) -%}
関連ガイドライン項目
{%- endfilter %}

{% for gl in guidelines -%}
*  {{ gl.category }}： :ref:`{{ gl.guideline }}`
{% endfor %}

