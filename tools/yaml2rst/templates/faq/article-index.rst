.. _faq-article-index:

{% filter make_heading(1) -%}
FAQ記事一覧
{%- endfilter %}

よくある質問と回答（FAQ）の全記事一覧です。

.. toctree::
   :maxdepth: 1
   :titlesonly:
{% for f in files %}
   {{ f.id }}
{%- endfor %}

