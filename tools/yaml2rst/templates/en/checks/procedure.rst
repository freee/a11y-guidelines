{% for proc in check.procedures -%}
{% filter make_heading(check_heading_level + 1) -%}
Check Procedure: {{ proc.platform }}
{%- endfilter %}

{{ proc.procedure }}

{% if proc.techniques is defined -%}

{% for technique in proc.techniques -%}
{% filter make_heading(check_heading_level + 2) -%}
An Example of Performin the Check with {{ technique.tool_display_name }}
{%- endfilter %}

{{ technique.technique }}
{% if technique.note is defined %}
{{ technique.note }}
{% endif %}
{% if technique.YouTube is defined %}
Reference Videos: `{{ technique.YouTube.title }} <https://www.youtube.com/watch?v={{ technique.YouTube.id }}>`_

.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/embed/{{ technique.YouTube.id }}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

{% endif %}
{% endfor %}
{%- endif %}
{%- endfor %}
