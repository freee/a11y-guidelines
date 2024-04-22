{% if lang == 'ja' -%}
.. csv-table:: WCAG 2.1の達成基準との対応一覧
   :widths: auto
   :header: "達成基準","原文","日本語訳","レベル","対応するガイドライン"
{% for item in mapping %}
   "{{ item.sc }}","`{{ item.sc_en_title }} <{{ item.sc_en_url }}>`__","`{{ item.sc_ja_title }} <{{ item.sc_ja_url }}>`__","{{ item.level }}","
{%- if item.guidelines|length == 0 -%}該当無し{%- else -%}
{%- for gl in item.guidelines %}
   *  {{ gl.category }}： :ref:`{{ gl.guideline }}`
{%- endfor %}{%- endif -%}"
{%- endfor %}
{%- elif lang == 'en' -%}
.. csv-table:: Mapping to the WCAG 2.1 Success Criteria
   :widths: auto
   :header: "Success Criterion","Level","Corresponding Guidelines"
{% for item in mapping %}
   "{{ item.sc }} `{{ item.sc_en_title }} <{{ item.sc_en_url }}>`__","{{ item.level }}","
{%- if item.guidelines|length == 0 -%}N/A{%- else -%}
{%- for gl in item.guidelines %}
   *  {{ gl.category }}: :ref:`{{ gl.guideline }}`
{%- endfor %}{%- endif -%}"
{%- endfor %}
{%- endif %}
{% if lang == 'ja' %}
.. translated:: true
{% endif %}



