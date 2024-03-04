{% for proc in check.procedures -%}
{% filter make_heading(check_heading_level + 1) -%}
チェック手順： {{ proc.platform }}
{%- endfilter %}

{{ proc.procedure }}

{% if proc.techniques is defined -%}

{% for technique in proc.techniques -%}
{% filter make_heading(check_heading_level + 2) -%}
{{ technique.tool_display_name }}によるチェック方法の例
{%- endfilter %}

{{ technique.technique }}
{% if technique.note is defined %}
{{ technique.note }}
{% endif %}
{% if technique.YouTube is defined %}
参考動画： `{{ technique.YouTube.title }} <https://www.youtube.com/watch?v={{ technique.YouTube.id }}>`_

.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/embed/{{ technique.YouTube.id }}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

{% endif %}
{% endfor %}
{%- endif %}
{%- endfor %}
