{% for ex in examples -%}
.. _check-example-{{ ex.tool }}-{{ ex.check_id }}:

{% filter make_heading(2) -%}
:ref:`check-{{ ex.check_id }}`
{%- endfilter %}

   {{ ex.check_text | indent(3) }}

{{ ex.technique }}
{% if ex.note is defined %}
{{ ex.note }}
{% endif %}
{% if ex.YouTube is defined %}
参考動画： `{{ ex.YouTube.title }} <https://www.youtube.com/watch?v={{ ex.YouTube.id }}>`_

.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/embed/{{ ex.YouTube.id }}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

{% endif %}
{% endfor %}
