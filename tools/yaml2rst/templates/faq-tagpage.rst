.. _faq-tag-{{ tag }}:

{% filter make_heading(1) -%}
{{ label }}に関連するよくある質問と回答（FAQ）
{%- endfilter %}

{% for item in articles %}
*  :ref:`{{ item }}`
{%- endfor %}


