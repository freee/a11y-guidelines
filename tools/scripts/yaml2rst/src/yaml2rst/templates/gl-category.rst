{%- set check_heading_level = 4 -%}
{% for gl in guidelines -%}
.. _{{ gl.id }}:

{{ gl.title|make_heading(2, 'permalink') }}

{{ gl.guideline }}

{% if lang == 'ja' -%}
対象プラットフォーム
{%- elif lang == 'en' -%}
Target Platforms
{%- endif %}
   {{ gl.platform }}
{% if lang == 'ja' -%}
意図
{%- elif lang == 'en' -%}
Intent
{%- endif %}
   {{ gl.intent | indent(3) }}
{% if lang == 'ja' -%}
対応するWCAG 2.1の達成基準
{%- for sc in gl.scs %}
   *  達成基準{{ sc.sc }}(レベル{{ sc.level }})：

      -  `{{ sc.sc_en_title }} <{{ sc.sc_en_url }}>`__
      -  `{{ sc.sc_ja_title }} <{{ sc.sc_ja_url }}>`__

{% endfor -%}
{%- elif lang == 'en' -%}
Corresponding Success Criteria of WCAG 2.1
{%- for sc in gl.scs %}
   *  Success Criterion {{ sc.sc }} (Level {{ sc.level }}): `{{ sc.sc_en_title }} <{{ sc.sc_en_url }}>`__
{% endfor -%}
{%- endif %}
{%- if gl.info is defined -%}
{% if lang == 'ja' -%}
参考情報
{%- elif lang == 'en' -%}
Supplementary Information
{%- endif %}
{%- for item in gl.info %}
   *  {{ item }}
{%- endfor %}
{%- endif %}
{% if gl.faqs is defined -%}
{% if lang == 'ja' -%}
関連FAQ
{%- elif lang == 'en' -%}
Related FAQs
{%- endif %}
{%- for item in gl.faqs %}
   *  :ref:`faq-{{ item }}`
{% endfor %}
{%- endif %}

{% filter make_heading(3, 'checklist') -%}
{% if lang == 'ja' -%}
チェック内容
{%- elif lang == 'en' -%}
Checklist Items
{%- endif %}
{%- endfilter %}

{% for check in gl.checks -%}
{% filter make_heading(4) -%}
:ref:`check-{{ check.id }}`
{%- endfilter %}

{{ check.check }}

{% if lang == 'ja' -%}
対象
{%- elif lang == 'en' -%}
Applicable Stages
{%- endif %}
   {{ check.target }}
{% if lang == 'ja' -%}
対象プラットフォーム
{%- elif lang == 'en' -%}
Target Platforms
{%- endif %}
   {{ check.platform }}
{% if lang == 'ja' -%}
重篤度
{%- elif lang == 'en' -%}
Severity
{%- endif %}
   {{ check.severity }}

{% if check.implementations is defined -%}
{% include 'checks/implementation.rst' %}
{%- endif %}
{% if check.conditions is defined %}
{% include 'checks/procedure.rst' %}
{% endif %}
{%- endfor %}
{% endfor %}
{% if lang == 'ja' -%}
.. translated:: true
{% endif %}
