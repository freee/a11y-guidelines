import unicodedata
from jinja2 import Environment, FileSystemLoader

class TemplateManager:
    def __init__(self, template_dir):
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.env.filters['make_heading'] = self.make_heading
        self.template = None

    def load(self, filename):
        self.template = self.env.get_template(filename)
        return self

    def write_rst(self, data, output_path):
        rendered_content = self.template.render(data)
        with open(output_path, mode='w', encoding='utf-8', newline='\n') as file:
            file.write(rendered_content)

    @staticmethod
    def make_heading(title, level, class_name=""):

        def _is_multibyte(c):
            return unicodedata.east_asian_width(c) in ['F', 'W', 'A']

        def _width(c):
            return 2 if _is_multibyte(c) else 1

        def width(s):
            return sum(_width(c) for c in s)

        # Modify heading_styles accordingly
        heading_styles = [('#', True), ('*', True), ('=', False), ('-', False), ('^', False), ('"', False)]

        if not 1 <= level <= len(heading_styles):
            raise ValueError(f'Invalid level: {level}. Must be between 1 and {len(heading_styles)}')

        char, overline = heading_styles[level - 1]
        line = char * width(title)

        heading_lines = []

        if class_name:
            heading_lines.append(f'.. rst-class:: {class_name}\n')

        if overline:
            heading_lines.append(line)

        heading_lines.append(title)
        heading_lines.append(line)

        return '\n'.join(heading_lines)
