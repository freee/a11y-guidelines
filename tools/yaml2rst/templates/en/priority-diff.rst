.. csv-table:: List of Success Criteria with Revised Levels
   :widths: auto
   :header: "Success Criterion","Original Level","Revised Level"
{% for item in diffs %}
   "{{ item.sc }} `{{ item.sc_en_title }} <{{ item.sc_en_url }}>`_","{{ item.level }}","{{ item.LocalLevel }}"
{%- endfor %}

