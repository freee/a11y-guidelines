.. _faq-index:

{% filter make_heading(1) -%}
よくある質問と回答（FAQ）
{%- endfilter %}

.. toctree::
   :maxdepth: 1
   :titlesonly:
   :hidden:

   articles/index
   tags/index

{% filter make_heading(2) -%}
タグ一覧
{%- endfilter %}

{% for f in tags -%}
*  :ref:`faq-tag-{{ f }}`
{% endfor %}

{% filter make_heading(2) -%}
FAQ記事一覧
{%- endfilter %}

{% for f in files -%}
*  :ref:`faq-{{ f.id }}`
{% endfor %}

