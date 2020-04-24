def trunc_whitespace(app, doctree, docname):
    from docutils.nodes import Text, paragraph
    if not app.config.japanesesupport_trunc_whitespace:
        return
    for node in doctree.traverse(Text):
        if isinstance(node.parent, paragraph):
            newtext = node.astext()
            for c in "\n\r\t":
                newtext = newtext.replace(c, "")
            newtext = newtext.strip()
            node.parent.replace(node, Text(newtext))

def setup(app):
    app.add_config_value('japanesesupport_trunc_whitespace', True, True)
    app.connect("doctree-resolved", trunc_whitespace)
