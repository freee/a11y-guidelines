ALL_INC_FILES = {{ info_to_gl_target }} {{ info_to_faq_target }} {{ guideline_category_target }} {{ check_example_target }} {{ wcag_mapping_target }} {{ priority_diff_target }} {{ all_checks_target }}  {{ miscdefs_target }}

%.yaml: ;
%.json: ;

{{ wcag_mapping_target }} {{ priority_diff_target }}: {{ gl_yaml }} {{ wcag_sc }}
	@$(YAML2RST) $@

{{ all_checks_target }}: {{ gl_yaml }} {{ check_yaml }} {{ faq_yaml }}
	@$(YAML2RST) {{ all_checks_target }}

{{ miscdefs_target }}: {{ info_src }}
	@$(YAML2RST) {{ miscdefs_target }}

{{ faq_index_target }}: {{ faq_yaml }}
	@$(YAML2RST) $@

{% for item in depends %}
{{ item.target }}: {{ item.depends }}
	@$(YAML2RST) {{ item.target }}
{% endfor %}
