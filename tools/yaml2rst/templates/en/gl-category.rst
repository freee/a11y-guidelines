{%- set check_heading_level = 4 -%}
{% for gl in guidelines -%}
.. _{{ gl.id }}:

{{ gl.title|make_heading(2) }}

{{ gl.guideline }}

Target Platforms
   {{ gl.platform }}
Intent
   {{ gl.intent | indent(3) }}
Corresponding Success Criteria of WCAG 2.1
{%- for sc in gl.scs %}
   *  Success Criterion {{ sc.sc }} (Level {{ sc.level }}): `{{ sc.sc_en_title }} <{{ sc.sc_en_url }}>`_
{% endfor -%}
{% if gl.info is defined -%}
Supplementary Information
{%- for item in gl.info %}
   *  {{ item }}
{%- endfor %}
{%- endif %}
{% if gl.faqs is defined -%}
Related FAQs
{%- for item in gl.faqs %}
   *  :ref:`faq-{{ item }}`
{% endfor %}
{%- endif %}

{% filter make_heading(3, 'checklist') -%}
Checklist Items
{%- endfilter %}

{% for check in gl.checks -%}
{% filter make_heading(4) -%}
:ref:`check-{{ check.id }}`
{%- endfilter %}

{{ check.check }}

Applicable Stages
   {{ check.target }}
Target Platforms
   {{ check.platform }}
Severity
   {{ check.severity }}

{% if check.implementations is defined -%}
{% include 'checks/implementation.rst' %}
{%- endif %}
{% if check.procedures is defined %}
{% include 'checks/procedure.rst' %}
{% endif %}
{%- endfor %}
{% endfor %}

