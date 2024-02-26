.. _faq-index:

{% filter make_heading(1) -%}
よくある質問と回答（FAQ）
{%- endfilter %}

ここでは、freee社内外から寄せられた質問の中で、比較的一般化できるものを「よくある質問と回答（FAQ）」としてまとめています。

各FAQ記事には、その内容に関連するキーワードをタグとして付与しています。
また、関連するガイドライン項目、チェック内容や参考情報へのリンクも掲載しています。

.. toctree::
   :maxdepth: 1
   :titlesonly:
   :hidden:

   articles/index
   tags/index

{% filter make_heading(2) -%}
タグ一覧
{%- endfilter %}

{% for tag in tags -%}
*  :ref:`faq-tag-{{ tag.tag }}`
{% endfor %}

{% filter make_heading(2) -%}
FAQ記事一覧
{%- endfilter %}

{% for article in articles -%}
*  :ref:`faq-{{ article.id }}` （{{ article.updated_year }}年{{ article.updated_month }}月{{ article.updated_day }}日更新）
{% endfor %}


.. translated:: true

