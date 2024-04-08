.. _faq-tag-index:

{% filter make_heading(1) -%}
FAQタグ一覧
{%- endfilter %}

よくある質問と回答（FAQ）に付けられているタグの一覧です。
タグをクリックすると、そのタグが付けられたFAQ記事の一覧が表示されます。

.. toctree::
   :maxdepth: 1
   :titlesonly:
{% for tag in tags %}
   {{ tag.tag }}
{%- endfor %}


.. translated:: true

