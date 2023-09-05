{%- set check_heading_level = 4 -%}
{% for gl in guidelines -%}
.. _{{ gl.id }}:

{{ gl.title|make_heading(2) }}

対象プラットフォーム
   {{ gl.platform }}

{{ gl.guideline }}

{% filter make_heading(3) -%}
意図
{%- endfilter %}

{{ gl.intent }}

{% filter make_heading(3) -%}
対応するWCAG 2.1の達成基準
{%- endfilter %}

{% for sc in gl.scs -%}
達成基準{{ sc.sc }}(レベル{{ sc.sc_level }})：
   -  {{ sc.sc_en }}
   -  {{ sc.sc_ja }}
{% endfor %}

{% if gl.info is defined -%}
{% filter make_heading(3) -%}
参考情報
{%- endfilter %}

{% for item in gl.info -%}
*  {{ item }}
{% endfor %}
{%- endif %}

{% filter make_heading(3, 'checklist') -%}
チェック内容
{%- endfilter %}

{% for check in gl.checks -%}
{% filter make_heading(4) -%}
:ref:`check-{{ check.id }}`
{%- endfilter %}

対象
   {{ check.target }}
対象プラットフォーム
   {{ check.platform }}
重篤度
   {{ check.severity }}

{{ check.check }}

{% if check.implementations is defined -%}
{% include 'check-implementation.rst' %}
{%- endif %}
{% if check.procedures is defined %}
{% include 'check-procedure.rst' %}
{% endif %}

{%- endfor %}

{% endfor %}

