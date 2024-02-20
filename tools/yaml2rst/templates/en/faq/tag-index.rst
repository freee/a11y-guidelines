.. _faq-tag-index:

{% filter make_heading(1) -%}
List of FAQ Rags
{%- endfilter %}

Here is a list of tags associated with the Frequently Asked Questions and Answers (FAQ).
Clicking on a tag will display a list of FAQ articles that have been tagged with it.

.. toctree::
   :maxdepth: 1
   :titlesonly:
{% for tag in tags %}
   {{ tag.tag }}
{%- endfor %}

