{%- if lang == 'ja' -%}
{%- set separator = '、' -%}
{%- set colon = '：' -%}
{%- elif lang == 'en' -%}
{%- set separator = ',' -%}
{%- set colon = ':' -%}
{%- endif -%}
.. _faq-{{ id }}:

{{ title|make_heading(1) }}

{% if lang == 'ja' -%}
最終更新：{{ updated_year }}年{{ updated_month }}月{{ updated_day }}日

タグ：
{%- elif lang == 'en' -%}
Last Updated: {{ updated_year }}-{{ updated_month }}-{{ updated_day }}

Tags:
{%- endif -%}
{%- for tag in tags -%}
{%- if loop.first %} {% endif -%}:ref:`faq-tag-{{ tag }}`{%- if not loop.last %} {{ separator }} {% endif -%}
{%- endfor %}

{% filter make_heading(2) -%}
{%- if lang == 'ja' -%}
質問/問題
{%- elif lang == 'en' -%}
Question / Problem
{%- endif -%}
{%- endfilter %}

{{ problem }}

{% filter make_heading(2) -%}
{%- if lang == 'ja' -%}
回答/結論
{%- elif lang == 'en' -%}
Answer / Conclusion
{%- endif -%}
{%- endfilter %}

{{ solution }}

{% filter make_heading(2) -%}
{%- if lang == 'ja' -%}
解説
{%- elif lang == 'en' -%}
Explanation
{%- endif -%}
{%- endfilter %}

{{ explanation }}
{% if related_faqs is defined %}
{% filter make_heading(2) -%}
{%- if lang == 'ja' -%}
関連FAQ
{%- elif lang == 'en' -%}
Related FAQs
{%- endif -%}
{%- endfilter %}

{% for faq in related_faqs -%}
*  :ref:`faq-{{ faq }}`
{% endfor %}
{%- endif -%}
{% if guidelines is defined %}
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
{%- endif -%}
{% if checks is defined %}
{% filter make_heading(2) -%}
{%- if lang == 'ja' -%}
関連チェック内容
{%- elif lang == 'en' -%}
Related Checklist Items
{%- endif -%}
{%- endfilter %}

{% for check in checks -%}
:ref:`check-{{ check.id }}`
   {{ check.check | indent(3) }}
{% endfor %}
{%- endif -%}
{% if info is defined %}
{% filter make_heading(2) -%}
{%- if lang == 'ja' -%}
関連する参考情報
{%- elif lang == 'en' -%}
Related Supplementary Information
{%- endif -%}
{%- endfilter %}

{% for i in info -%}
*  {{ i }}
{% endfor %}
{%- endif %}
{% if lang == 'ja' -%}
.. translated:: true
{% endif %}
