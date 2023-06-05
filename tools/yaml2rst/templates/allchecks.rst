{% for check in allchecks -%}
.. _check-{{ check.id }}:

{% filter make_header('*', True) -%}
チェックID：{{ check.id }}
{%- endfilter %}

対象
   {{ check.target }}
対象プラットフォーム
   {{ check.platform }}
重篤度
   {{ check.severity }}

関連ガイドライン
{%- for ref in check.gl_refs %}
   *  {{ ref.category }}： :ref:`{{ ref.glref }}`
{%- endfor %}

{{ check.check }}

{% if check.inforefs is defined -%}
{% filter make_header('=') -%}
参考情報
{%- endfilter %}

{% for item in check.inforefs -%}
*  {{ item }}
{% endfor %}
{%- endif %}

{% if check.implementations is defined -%}
{% for impl in check.implementations -%}
{% filter make_header('=') -%}
実装方法の例：{{ impl.title }}
{%- endfilter %}

{% for ex in impl.examples -%}
{{ ex.platform }}
   {{ ex.method | indent(3) }}

{% endfor %}
{%- endfor %}
{%- endif %}
{% if check.procedures is defined %}
{% for proc in check.procedures -%}
{% filter make_header('=') -%}
チェック手順： {{ proc.platform }}
{%- endfilter %}

{{ proc.text }}

{% if proc.techniques is defined -%}

{% for technique in proc.techniques -%}
{% filter make_header('-') -%}
{{ technique.tool_display_name }}によるチェック方法の例
{%- endfilter %}

{{ technique.technique }}
{% if technique.note is defined %}
{{ technique.note }}
{% endif %}
{% endfor %}
{%- endif %}
{%- endfor %}
{% endif %}
{%- endfor %}
