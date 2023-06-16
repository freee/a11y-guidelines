{% for proc in check.procedures -%}
{% filter make_heading(check_heading_level + 1) -%}
チェック手順： {{ proc.platform }}
{%- endfilter %}

{{ proc.text }}

{% if proc.techniques is defined -%}

{% for technique in proc.techniques -%}
{% filter make_heading(check_heading_level + 2) -%}
{{ technique.tool_display_name }}によるチェック方法の例
{%- endfilter %}

{{ technique.technique }}
{% if technique.note is defined %}
{{ technique.note }}
{% endif %}
{% endfor %}
{%- endif %}
{%- endfor %}
