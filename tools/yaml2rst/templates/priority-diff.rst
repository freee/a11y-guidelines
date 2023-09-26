.. csv-table:: レベルを見直した達成基準一覧
   :widths: auto
   :header: "達成基準","原文","日本語訳","見直し前","見直し後"
{% for item in diffs %}
   "{{ item.sc }}","{{ item.sc_en }}","{{ item.sc_ja }}","{{ item.level }}","{{ item.LocalLevel }}"
{%- endfor %}

