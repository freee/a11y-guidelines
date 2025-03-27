{% if lang == 'ja' -%}
.. csv-table:: レベルを見直した達成基準一覧
   :widths: auto
   :header: "達成基準","原文","日本語訳","見直し前","見直し後"
{% for item in diffs %}
   "{{ item.sc }}","`{{ item.sc_en_title }} <{{ item.sc_en_url }}>`__","`{{ item.sc_ja_title }} <{{ item.sc_ja_url }}>`__","{{ item.level }}","{{ item.LocalLevel }}"
{%- endfor %}
{%- elif lang == 'en' -%}
.. csv-table:: List of Success Criteria with Revised Levels
   :widths: auto
   :header: "Success Criterion","Original Level","Revised Level"
{% for item in diffs %}
   "{{ item.sc }} `{{ item.sc_en_title }} <{{ item.sc_en_url }}>`__","{{ item.level }}","{{ item.LocalLevel }}"
{%- endfor %}
{%- endif %}
{%if lang == 'ja' %}
.. translated:: true
{% endif %}

