{%- set check_heading_level = 2 -%}
{% for check in allchecks -%}
.. _check-{{ check.id }}:

{% filter make_heading(2) -%}
Check ID: {{ check.id }}
{%- endfilter %}

{{ check.check }}

Applicable Stages
   {{ check.target }}
Target Platforms
   {{ check.platform }}
Severity
   {{ check.severity }}
Related Guidelines
{%- for ref in check.guidelines %}
   *  {{ ref.category }}: :ref:`{{ ref.guideline }}`
{%- endfor %}
{% if check.faqs is defined -%}
Related FAQs
{%- for item in check.faqs %}
   *  :ref:`faq-{{ item }}`
{%- endfor %}
{%- endif %}
{% if check.info_refs is defined -%}
Supplementary Information
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
