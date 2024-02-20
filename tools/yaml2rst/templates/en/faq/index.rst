.. _faq-index:

{% filter make_heading(1) -%}
Frequently Asked Questions (FAQ)
{%- endfilter %}

Here, we have compiled questions that can be relatively generalized from those received both internally and externally from freee, as "Frequently Asked Questions and Answers (FAQ)."

Each FAQ article is tagged with keywords related to its content. Additionally, links to related guidelines, checklist items, and supplemenmtary information are also provided.

.. toctree::
   :maxdepth: 1
   :titlesonly:
   :hidden:

   articles/index
   tags/index

{% filter make_heading(2) -%}
List of Tags
{%- endfilter %}

{% for tag in tags -%}
*  :ref:`faq-tag-{{ tag.tag }}`
{% endfor %}

{% filter make_heading(2) -%}
List of Articles
{%- endfilter %}

{% for article in articles -%}
*  :ref:`faq-{{ article.id }}` (updated on {{ article.updated_year }}-{{ article.updated_month }}-{{ article.updated_day }})
{% endfor %}

