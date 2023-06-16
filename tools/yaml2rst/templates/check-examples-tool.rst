{% for ex in examples -%}
.. _check-example-{{ ex.tool }}-{{ ex.id }}:

{% filter make_heading(2) -%}
:ref:`check-{{ ex.id }}`
{%- endfilter %}

   {{ ex.check | indent(3) }}

{{ ex.technique }}
{% if ex.note is defined %}
{{ ex.note }}
{% endif %}
{% endfor %}
