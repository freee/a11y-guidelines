The information below is automatically generated based on the content of the develop branch of the `axe-core GitHub repository <https://github.com/dequelabs/axe-core/>`_ as of the time indicated below. Please note that it may not always match the content of axe DevTools.

Version
   {{ version }}
Updated
   {{ timestamp }}

{% for rule in rules -%}
.. _axe-rule-{{ rule.id }}:

{% filter make_heading(2) -%}
{{ rule.help.en }}{% if rule.translated is defined %} （{{ rule.help.ja }}）{% endif -%}
{%- endfilter %}

{{ rule.description.en }}

CF: `Explanation on Deque University <{{ deque_url }}{{ major_version }}/{{ rule.id }}>`__

{% if rule.scs is defined -%}
{% filter make_heading(3) -%}
Related WCAG 2.1 Success Criteria
{%- endfilter %}

{% for sc in rule.scs -%}
*  Success Criterion {{ sc.sc }}: `{{ sc.sc_en_title }} <{{ sc.sc_en_url }}>`_
{% endfor %}
{%- endif %}
{% if rule.guidelines is defined -%}
{% filter make_heading(3) -%}
Related Guidelines
{%- endfilter %}

{% for gl in rule.guidelines -%}
*  {{ gl.category }}: :ref:`{{ gl.guideline }}`
{% endfor %}
{%- endif %}
{% endfor %}
