{% filter make_heading(2) -%}
Related FAQs
{%- endfilter %}

{% for faq in faqs -%}
*  :ref:`faq-{{ faq }}`
{% endfor %}

