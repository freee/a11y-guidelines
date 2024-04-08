{%- if lang == 'ja' -%}
{%- set colon = '：' -%}
{%- elif lang == 'en' -%}
{%- set colon = ':' -%}
{%- endif -%}
{% filter make_heading(2) -%}
{%- if lang == 'ja' -%}
関連ガイドライン項目
{%- elif lang == 'en' -%}
Related Guidelines
{%- endif -%}
{%- endfilter %}

{% for gl in guidelines -%}
*  {{ gl.category }}{{ colon }} :ref:`{{ gl.guideline }}`
{% endfor %}

