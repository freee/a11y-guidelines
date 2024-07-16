{% for ex in examples -%}
.. _check-example-{{ ex.tool }}-{{ ex.check_id }}:

{% filter make_heading(2, 'permalink') -%}
:ref:`check-{{ ex.check_id }}`
{%- endfilter %}

   {{ ex.check_text | indent(3) }}

.. _check-{{ ex.id }}:

{% filter make_heading(3, 'permalink') -%}
ID {{ ex.id }}
{%- endfilter %}

{{ ex.procedure }}
{% if ex.note is defined %}
{{ ex.note }}
{% endif %}
{% if ex.YouTube is defined %}
{% if lang == 'ja' -%}
参考動画：
{%- elif lang == 'en' -%}
Reference Videos:
{%- endif %} `{{ ex.YouTube.title }} <https://www.youtube.com/watch?v={{ ex.YouTube.id }}>`__

.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/embed/{{ ex.YouTube.id }}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

{% endif %}
{% endfor %}
{% if lang == 'ja' -%}
.. translated:: true
{% endif %}
