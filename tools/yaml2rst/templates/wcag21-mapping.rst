.. csv-table:: WCAG 2.1の達成基準との対応一覧
   :widths: auto
   :header: "達成基準","原文","日本語訳","レベル","対応するガイドライン"
{% for item in mapping %}
   "{{ item.sc }}","`{{ item.sc_en_title }} <{{ item.sc_en_url }}>`_","`{{ item.sc_ja_title }} <{{ item.sc_ja_url }}>`_","{{ item.level }}","
{%- for gl in item.guidelines %}
   *  {{ gl.category }}： :ref:`{{ gl.guideline }}`
{%- endfor %}"
{%- endfor %}

