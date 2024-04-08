{%- set check_heading_level = 4 -%}
{% for gl in guidelines -%}
.. _{{ gl.id }}:

{{ gl.title|make_heading(2) }}

{{ gl.guideline }}

対象プラットフォーム
   {{ gl.platform }}
意図
   {{ gl.intent | indent(3) }}
対応するWCAG 2.1の達成基準
{%- for sc in gl.scs %}
   *  達成基準{{ sc.sc }}(レベル{{ sc.level }})：

      -  `{{ sc.sc_en_title }} <{{ sc.sc_en_url }}>`_
      -  `{{ sc.sc_ja_title }} <{{ sc.sc_ja_url }}>`_

{% endfor -%}
{% if gl.info is defined -%}
参考情報
{%- for item in gl.info %}
   *  {{ item }}
{%- endfor %}
{%- endif %}
{% if gl.faqs is defined -%}
関連FAQ
{%- for item in gl.faqs %}
   *  :ref:`faq-{{ item }}`
{% endfor %}
{%- endif %}

{% filter make_heading(3, 'checklist') -%}
チェック内容
{%- endfilter %}

{% for check in gl.checks -%}
{% filter make_heading(4) -%}
:ref:`check-{{ check.id }}`
{%- endfilter %}

{{ check.check }}

対象
   {{ check.target }}
対象プラットフォーム
   {{ check.platform }}
重篤度
   {{ check.severity }}

{% if check.implementations is defined -%}
{% include 'checks/implementation.rst' %}
{%- endif %}
{% if check.procedures is defined %}
{% include 'checks/procedure.rst' %}
{% endif %}
{%- endfor %}
{% endfor %}


.. translated:: true

