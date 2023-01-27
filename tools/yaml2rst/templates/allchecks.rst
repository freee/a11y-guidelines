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
{% if check.procedure is defined %}
{% filter make_header('=') -%}
チェック手順
{%- endfilter %}

{{ check.procedure }}
{% endif %}
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
{% if check.techniques is defined -%}
{% filter make_header('=') -%}
チェック方法の例
{%- endfilter %}

{% for technique in check.techniques -%}
{% filter make_header('-') -%}
{{ technique.tool_display_name }}によるチェック
{%- endfilter %}

{{ technique.technique }}
{% if technique.note is defined %}
{{ technique.note }}
{% endif %}
{% endfor %}
{%- endif %}
{%- endfor %}
