.. _faq-{{ id }}:

{{ title|make_heading(1) }}

Last Updated: {{ updated_year }}-{{ updated_month }}-{{ updated_day }}

Tags:
{%- for tag in tags -%}
{%- if loop.first %} {% endif -%}:ref:`faq-tag-{{ tag }}`{%- if not loop.last %} , {% endif -%}
{%- endfor %}

{% filter make_heading(2) -%}
Question / Problem
{%- endfilter %}

{{ problem }}

{% filter make_heading(2) -%}
Answer / Conclusion
{%- endfilter %}

{{ solution }}

{% filter make_heading(2) -%}
Explanation
{%- endfilter %}

{{ explanation }}

{% if guidelines is defined -%}
{%- filter make_heading(2) -%}
Related Guidelines
{%- endfilter %}

{% for gl in guidelines -%}
*  {{ gl.category }}: :ref:`{{ gl.guideline }}`
{% endfor %}
{%- endif %}

{% if checks is defined -%}
{%- filter make_heading(2) -%}
Related Checklist Items
{%- endfilter %}

{% for check in checks -%}
:ref:`check-{{ check.id }}`
   {{ check.check | indent(3) }}
{% endfor %}
{%- endif %}

{% if info is defined -%}
{%- filter make_heading(2) -%}
Related Supplementary Information
{%- endfilter %}

{% for i in info -%}
*  {{ i }}
{% endfor %}
{%- endif %}

