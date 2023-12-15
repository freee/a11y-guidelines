.. _faq-tag-index:

{% filter make_heading(1) -%}
タグ一覧
{%- endfilter %}

.. toctree::
   :maxdepth: 1
   :titlesonly:
{% for f in tags %}
   {{ f }}
{%- endfor %}

