.. csv-table:: WCAG 2.1の達成基準との対応一覧
   :widths: auto
   :header: "達成基準","原文","日本語訳","適合レベル","対応するガイドライン"
{% for item in mapping %}
   "{{ item.sc }}","{{ item.sc_en }}","{{ item.sc_ja }}","{{ item.level }}","{{ item.gls }}"
{%- endfor %}
