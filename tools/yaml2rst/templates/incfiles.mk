guidelines_rst = {{ guidelines_rst }}

incfiles: $(guidelines_rst)

%.yaml: ;

{{ wcag_mapping_target }}: {{ gl_yaml }} {{ wcag_sc }}
	@$(YAML2RST) {{ wcag_mapping_target }}

{{ priority_diff_target }}: {{ gl_yaml }} {{ wcag_sc }}
	@$(YAML2RST) {{ priority_diff_target }}

{{ all_checks_target }}: {{ all_yaml }}
	@$(YAML2RST) {{ all_checks_target }}

{{ miscdefs_target }}: {{ info_src }}
	@$(YAML2RST) {{ miscdefs_target }}

{% for item in gl_deps %}
{{ item.dep }}
	@$(YAML2RST) {{ item.target }}
{% endfor %}
