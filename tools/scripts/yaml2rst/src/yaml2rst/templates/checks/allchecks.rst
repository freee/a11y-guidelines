{%- set check_heading_level = 2 -%}
{%- if lang == 'ja' -%}
{%- set colon = '：' -%}
{%- elif lang == 'en' -%}
{%- set colon = ':' -%}
{%- endif -%}
{% for check in allchecks -%}
.. _check-{{ check.id }}:

{% filter make_heading(2, 'permalink') -%}
{%- if lang == 'ja' -%}
チェックID：{{ check.id }}
{%- elif lang == 'en' -%}
Check ID: {{ check.id }}
{%- endif -%}
{%- endfilter %}

{{ check.check }}

{% if lang == 'ja' -%}
対象
{%- elif lang == 'en' -%}
Applicable Stages
{%- endif %}
   {{ check.target }}
{% if lang == 'ja' -%}
対象プラットフォーム
{%- elif lang == 'en' -%}
Target Platforms
{%- endif %}
   {{ check.platform }}
{% if lang == 'ja' -%}
重篤度
{%- elif lang == 'en' -%}
Severity
{%- endif %}
   {{ check.severity }}
{% if lang == 'ja' -%}
関連ガイドライン項目
{%- elif lang == 'en' -%}
Related Guidelines
{%- endif -%}
{%- for ref in check.guidelines %}
   *  {{ ref.category }}{{ colon }} :ref:`{{ ref.guideline }}`
{%- endfor %}
{% if check.faqs is defined -%}
{% if lang == 'ja' -%}
関連FAQ
{%- elif lang == 'en' -%}
Related FAQs
{%- endif -%}
{%- for item in check.faqs %}
   *  :ref:`faq-{{ item }}`
{%- endfor %}
{%- endif %}
{% if check.info_refs is defined -%}
{% if lang == 'ja' -%}
参考情報
{%- elif lang == 'en' -%}
Supplementary Information
{%- endif -%}
{%- for item in check.info_refs %}
   *  {{ item }}
{%- endfor %}
{%- endif %}

{% if check.implementations is defined -%}
{% include 'checks/implementation.rst' %}
{%- endif %}
{% if check.conditions is defined %}
{% include 'checks/procedure.rst' %}
{% endif %}
{%- endfor %}
{% if lang == 'ja' -%}
.. translated:: true
{% endif %}
