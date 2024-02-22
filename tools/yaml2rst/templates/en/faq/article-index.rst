.. _faq-article-index:

{% filter make_heading(1) -%}
FAQ Articles
{%- endfilter %}

This is a list of all the FAQ articles in the system.

.. toctree::
   :maxdepth: 1
   :titlesonly:
{% for article in articles %}
   {{ article.id }}
{%- endfor %}

