.. _faq-index:

{% filter make_heading(1) -%}
よくある質問と回答（FAQ）
{%- endfilter %}

.. toctree::
   :maxdepth: 1
   :titlesonly:

{% for f in files %}
   articles/{{ f }}
{%- endfor %}

.. toctree::
   :hidden:
   :glob:

   tags/*

