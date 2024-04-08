{% filter make_heading(2) -%}
関連FAQ
{%- endfilter %}

{% for faq in faqs -%}
*  :ref:`faq-{{ faq }}`
{% endfor %}

