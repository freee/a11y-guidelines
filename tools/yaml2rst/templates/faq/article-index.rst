.. _faq-article-index:

{% filter make_heading(1) -%}
FAQ記事一覧
{%- endfilter %}

.. toctree::
   :maxdepth: 1
   :titlesonly:
{% for f in files %}
   {{ f.id }}
{%- endfor %}

