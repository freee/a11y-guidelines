.. csv-table:: Mapping to the WCAG 2.1 Success Criteria
   :widths: auto
   :header: "Success Criterion","Level","Corresponding Guidelines"
{% for item in mapping %}
   "{{ item.sc }} `{{ item.sc_en_title }} <{{ item.sc_en_url }}>`_""{{ item.level }}","
{%- for gl in item.guidelines %}
   *  {{ gl.category }}: :ref:`{{ gl.guideline }}`
{%- endfor %}"
{%- endfor %}

