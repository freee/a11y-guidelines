{% filter make_heading(2) -%}
{%- if lang == 'ja' -%}
関連FAQ
{%- elif lang == 'en' -%}
Related FAQs
{%- endif -%}
{%- endfilter %}

{% for faq in faqs -%}
*  :ref:`faq-{{ faq }}`
{% endfor %}

