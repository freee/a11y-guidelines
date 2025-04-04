{%- if lang == 'ja' -%}
{%- set colon = '：' -%}
{%- elif lang == 'en' -%}
{%- set colon = ':' -%}
{%- endif -%}
{% if lang == 'ja' -%}
ここで掲載している情報は、 `axe-coreのGitHubリポジトリー <https://github.com/dequelabs/axe-core/>`__ の以下に示す時点におけるdevelopブランチの内容に基づいて自動的に生成したものです。axe DevToolsの内容とは一致していない場合もあることにご注意ください。

バージョン
   {{ version }}
更新日時
   {{ timestamp }}
{%- elif lang == 'en' -%}
The information below is automatically generated based on the content of the develop branch of the `axe-core GitHub repository <https://github.com/dequelabs/axe-core/>`__ as of the time indicated below. Please note that it may not always match the content of axe DevTools.

Version
   {{ version }}
Updated
   {{ timestamp }}
{%- endif %}

{% for rule in rules -%}
.. _axe-rule-{{ rule.id }}:

{% filter make_heading(2, 'permalink') -%}
{%- if lang == 'ja' -%}
{% if rule.translated is defined %}{{ rule.help.ja }} ({% endif -%}{{ rule.help.en }}{%- if rule.translated is defined %}){% endif %}
{%- elif lang == 'en' -%}
{{ rule.help.en }}{% if rule.translated is defined %} （{{ rule.help.ja }}）{% endif -%}
{%- endif -%}
{%- endfilter %}

{% if lang == 'ja' -%}
{{ rule.description.ja }}

参考： `Deque Universityの解説 <{{ deque_url }}{{ major_version }}/{{ rule.id }}>`__
{%- elif lang == 'en' -%}
{{ rule.description.en }}

CF: `Explanation on Deque University <{{ deque_url }}{{ major_version }}/{{ rule.id }}>`__
{%- endif %}
{% if rule.scs is defined %}
{% filter make_heading(3) -%}
{%- if lang == 'ja' -%}
関連するWCAG 2.1の達成基準
{%- elif lang == 'en' -%}
Related WCAG 2.1 Success Criteria
{%- endif -%}
{%- endfilter %}

{% for sc in rule.scs -%}
{%- if lang == 'ja' -%}
*  達成基準 {{ sc.sc }}

   -  `{{ sc.sc_en_title }} <{{ sc.sc_en_url }}>`__
   -  `{{ sc.sc_ja_title }} <{{ sc.sc_ja_url }}>`__
{% elif lang == 'en' -%}
*  Success Criterion {{ sc.sc }}: `{{ sc.sc_en_title }} <{{ sc.sc_en_url }}>`__
{%- endif %}
{% endfor -%}
{%- endif %}
{% if rule.guidelines is defined -%}
{% filter make_heading(3) -%}
{%- if lang == 'ja' -%}
関連ガイドライン項目
{%- elif lang == 'en' -%}
Related Guidelines
{%- endif -%}
{%- endfilter %}

{% for gl in rule.guidelines -%}
*  {{ gl.category }}{{ colon }} :ref:`{{ gl.guideline }}`
{% endfor %}
{%- endif %}
{% endfor %}
{% if lang == 'ja' -%}
.. translated:: true
{% endif %}
