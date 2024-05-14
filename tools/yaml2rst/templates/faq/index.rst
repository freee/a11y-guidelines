.. _faq-index:

{% filter make_heading(1) -%}
{%- if lang == 'ja' -%}
よくある質問と回答（FAQ）
{%- elif lang == 'en' -%}
Frequently Asked Questions (FAQ)
{%- endif -%}
{%- endfilter %}

{% if lang == 'ja' -%}
ここでは、freee社内外から寄せられた質問の中で、比較的一般化できるものを「よくある質問と回答（FAQ）」としてまとめています。

各FAQ記事には、その内容に関連するキーワードをタグとして付与しています。
また、関連するガイドライン項目、チェック内容や参考情報へのリンクも掲載しています。
{%- elif lang == 'en' -%}
Here, we have compiled questions that can be relatively generalized from those received both internally and externally from freee, as "Frequently Asked Questions and Answers (FAQ)."

Each FAQ article is tagged with keywords related to its content. Additionally, links to related guidelines, checklist items, and supplemenmtary information are also provided.
{%- endif %}

.. toctree::
   :maxdepth: 1
   :titlesonly:
   :hidden:

   articles/index
   tags/index

{% filter make_heading(2) -%}
{%- if lang == 'ja' -%}
タグ一覧
{%- elif lang == 'en' -%}
List of Tags
{%- endif -%}
{%- endfilter %}

{% for tag in tags -%}
*  :ref:`faq-tag-{{ tag.tag }}`
{% endfor %}

{% filter make_heading(2) -%}
{%- if lang == 'ja' -%}
FAQ記事一覧
{%- elif lang == 'en' -%}
List of FAQ Articles
{%- endif -%}
{%- endfilter %}

{% for article in articles -%}
{%- if lang == 'ja' -%}
*  :ref:`faq-{{ article.id }}` （{{ article.updated_str }}更新）
{%- elif lang == 'en' -%}
*  :ref:`faq-{{ article.id }}` (updated on {{ article.updated_str }})
{%- endif %}
{% endfor %}
{% if lang == 'ja' -%}
.. translated:: true
{% endif %}
