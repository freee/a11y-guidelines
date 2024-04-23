.. _faq-article-index:

{% filter make_heading(1) -%}
{%- if lang == 'ja' -%}
FAQ記事一覧
{%- elif lang == 'en' -%}
FAQ Articles
{%- endif -%}
{%- endfilter %}

{% if lang == 'ja' -%}
よくある質問と回答（FAQ）の全記事一覧です。
{%- elif lang == 'en' -%}
This is a list of all the FAQ articles in the system.
{%- endif %}

.. toctree::
   :maxdepth: 1
   :titlesonly:
{% for article in articles %}
   {{ article.id }}
{%- endfor %}

{% if lang == 'ja' -%}
.. translated:: true
{% endif %}
