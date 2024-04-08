.. _faq-tag-index:

{% filter make_heading(1) -%}
{%- if lang == 'ja' -%}
FAQタグ一覧
{%- elif lang == 'en' -%}
List of FAQ Tags
{%- endif -%}
{%- endfilter %}

{% if lang == 'ja' -%}
よくある質問と回答（FAQ）に付けられているタグの一覧です。
タグをクリックすると、そのタグが付けられたFAQ記事の一覧が表示されます。
{%- elif lang == 'en' -%}
Here is a list of tags associated with the Frequently Asked Questions and Answers (FAQ).
Clicking on a tag will display a list of FAQ articles that have been tagged with it.
{%- endif %}

.. toctree::
   :maxdepth: 1
   :titlesonly:
{% for tag in tags %}
   {{ tag.tag }}
{%- endfor %}

{% if lang == 'ja' -%}
.. translated:: true
{% endif %}
