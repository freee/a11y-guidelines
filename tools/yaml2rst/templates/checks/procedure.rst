{% for proc in check.procedures -%}
{% filter make_heading(check_heading_level + 1) -%}
{%- if lang == 'ja' -%}
チェック手順： {{ proc.platform }}
{%- elif lang == 'en' -%}
Check Procedure: {{ proc.platform }}
{%- endif -%}
{%- endfilter %}

{{ proc.procedure }}

{% if proc.techniques is defined -%}

{% for technique in proc.techniques -%}
{% filter make_heading(check_heading_level + 2) -%}
{%- if lang == 'ja' -%}
{{ technique.tool_display_name }}によるチェック方法の例
{%- elif lang == 'en' -%}
An Example of Performin the Check with {{ technique.tool_display_name }}
{%- endif -%}
{%- endfilter %}

{{ technique.technique }}
{% if technique.note is defined %}
{{ technique.note }}
{% endif %}
{% if technique.YouTube is defined %}
{% if lang == 'ja' -%}
参考動画：
{%- elif lang == 'en' -%}
Reference Videos:
{%- endif %} `{{ technique.YouTube.title }} <https://www.youtube.com/watch?v={{ technique.YouTube.id }}>`__

.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/embed/{{ technique.YouTube.id }}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

{% endif %}
{% endfor %}
{%- endif %}
{%- endfor %}
