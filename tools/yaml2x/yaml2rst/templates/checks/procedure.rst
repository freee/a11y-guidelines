{% for cond in check.conditions -%}
{% filter make_heading(check_heading_level + 1) -%}
{%- if lang == 'ja' -%}
チェック手順： {{ cond.platform }}
{%- elif lang == 'en' -%}
Check Procedure: {{ cond.platform }}
{%- endif -%}
{%- endfilter %}

{% if lang == 'ja' -%}
以下の{{ cond.condition }}ことを確認する。
{%- elif lang == 'en' -%}
Verify that {{ cond.condition }} below.
{%- endif %}

{% if cond.procedures is defined -%}

{% for proc in cond.procedures -%}
{% filter make_heading(check_heading_level + 2) -%}
{%- if lang == 'ja' -%}
{{ proc.id }}：{{ proc.tool_display_name }}によるチェック方法の例
{%- elif lang == 'en' -%}
{{ proc.id }}: An Example of Performin the Check with {{ proc.tool_display_name }}
{%- endif -%}
{%- endfilter %}

{{ proc.procedure }}
{% if proc.note is defined %}
{{ proc.note }}
{% endif %}
{% if proc.YouTube is defined %}
{% if lang == 'ja' -%}
参考動画：
{%- elif lang == 'en' -%}
Reference Videos:
{%- endif %} `{{ proc.YouTube.title }} <https://www.youtube.com/watch?v={{ proc.YouTube.id }}>`__

.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/embed/{{ proc.YouTube.id }}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

{% endif %}
{% endfor %}
{%- endif %}
{%- endfor %}
