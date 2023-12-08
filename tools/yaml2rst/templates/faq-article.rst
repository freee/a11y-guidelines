.. _faq-{{ id }}:

{{ title|make_heading(1) }}

タグ：
{%- for tag in tags -%}
{%- if loop.first %} {% endif -%}:ref:`faq-tag-{{ tag }}`{%- if not loop.last %} 、 {% endif -%}
{%- endfor %}

{% filter make_heading(2) -%}
質問/問題
{%- endfilter %}

{{ problem }}

{% filter make_heading(2) -%}
回答/結論
{%- endfilter %}

{{ solution }}

{% filter make_heading(2) -%}
解説
{%- endfilter %}

{{ explanation }}

{% if guidelines is defined -%}
{%- filter make_heading(2) -%}
関連ガイドライン項目
{%- endfilter %}

{% for gl in guidelines -%}
*  :ref:`{{ gl }}`
{%- endfor %}
{%- endif %}

{% if checks is defined -%}
{%- filter make_heading(2) -%}
関連チェック内容
{%- endfilter %}

{% for check in checks -%}
:ref:`check-{{ check.id }}`
   {{ check.check | indent(3) }}
{%- endfor %}
{%- endif %}

{% if info is defined -%}
{%- filter make_heading(2) -%}
関連する参考情報
{%- endfilter %}

{% for i in info -%}
*  :ref:`{{ i }}`
{%- endfor %}
{%- endif %}

