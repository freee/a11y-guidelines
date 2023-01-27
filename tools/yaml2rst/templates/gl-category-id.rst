.. _{{ id }}:

{{ title|make_header("*", True) }}

優先度
   {{ priority }}
対象プラットフォーム
   {{ platform }}

{{ guideline }}

{% filter make_header('=') -%}
意図
{%- endfilter %}

{{ intent }}

{% filter make_header('=') -%}
対応するWCAG 2.1の達成基準
{%- endfilter %}

{% for sc in scs -%}
SC {{ sc.sc }}：
   -  {{ sc.sc_en }}
   -  {{ sc.sc_ja }}
{% endfor %}

{% if info is defined -%}
{% filter make_header('=') -%}
参考情報
{%- endfilter %}

{% for item in info -%}
*  {{ item }}
{% endfor %}
{%- endif %}

{% filter make_header('=', False, 'checklist') -%}
チェック内容
{%- endfilter %}

{% for check in checks -%}
{% filter make_header('-') -%}
:ref:`check-{{ check.id }}`
{%- endfilter %}

対象
   {{ check.target }}
対象プラットフォーム
   {{ check.platform }}
重篤度
   {{ check.severity }}


{{ check.check }}
{% if check.procedure is defined %}
{% filter make_header('^') -%}
チェック手順
{%- endfilter %}

{{ check.procedure }}
{% endif %}
{% if check.implementations is defined -%}
{% for impl in check.implementations -%}
{% filter make_header('^') -%}
実装方法の例：{{ impl.title }}
{%- endfilter %}

{% for ex in impl.examples -%}
{{ ex.platform }}
   {{ ex.method | indent(3) }}

{% endfor %}
{%- endfor %}
{%- endif %}
{% if check.techniques is defined -%}
{% filter make_header('^') -%}
チェック方法の例
{%- endfilter %}

{% for technique in check.techniques -%}
{% filter make_header('"') -%}
{{ technique.tool_display_name }}によるチェック
{%- endfilter %}

{{ technique.technique }}
{% if technique.note is defined %}
{{ technique.note }}
{% endif %}
{% endfor %}
{%- endif %}
{%- endfor %}
