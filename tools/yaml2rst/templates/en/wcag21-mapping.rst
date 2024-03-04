.. csv-table:: Mapping to the WCAG 2.1 Success Criteria
   :widths: auto
   :header: "Success Criterion","Level","Corresponding Guidelines"
{% for item in mapping %}
   "{{ item.sc }} `{{ item.sc_en_title }} <{{ item.sc_en_url }}>`_","{{ item.level }}","
{%- if item.guidelines|length == 0 -%}N/A{%- else -%}
{%- for gl in item.guidelines %}
   *  {{ gl.category }}: :ref:`{{ gl.guideline }}`
{%- endfor %}{%- endif -%}"
{%- endfor %}

