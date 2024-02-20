{%- set check_heading_level = 2 -%}
{% for check in allchecks -%}
.. _check-{{ check.id }}:

{% filter make_heading(2) -%}
チェックID：{{ check.id }}
{%- endfilter %}

{{ check.check }}

対象
   {{ check.target }}
対象プラットフォーム
   {{ check.platform }}
重篤度
   {{ check.severity }}
関連ガイドライン項目
{%- for ref in check.guidelines %}
   *  {{ ref.category }}： :ref:`{{ ref.guideline }}`
{%- endfor %}
{% if check.faqs is defined -%}
関連FAQ
{%- for item in check.faqs %}
   *  :ref:`faq-{{ item }}`
{%- endfor %}
{%- endif %}
{% if check.info_refs is defined -%}
参考情報
{%- for item in check.info_refs %}
   *  {{ item }}
{%- endfor %}
{%- endif %}

{% if check.implementations is defined -%}
{% include 'checks/implementation.rst' %}
{%- endif %}
{% if check.procedures is defined %}
{% include 'checks/procedure.rst' %}
{% endif %}
{%- endfor %}
