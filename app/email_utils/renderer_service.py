from jinja2 import Environment, FileSystemLoader, select_autoescape

from email_utils.email_templates import EmailTemplate


class RendererService:
    def __init__(self):
        self.env = Environment(
            loader=FileSystemLoader("templates"),
            autoescape=select_autoescape(["html", "xml"]),
        )

        for template in EmailTemplate:
            self.env.get_template(f"{template.value}.html")
            self.env.get_template(f"{template.value}.txt")


    def render(self, template_name: EmailTemplate, context: dict):
        template_html = self.env.get_template(f"{template_name.value["template"]}.html")
        template_txt = self.env.get_template(f"{template_name.value["template"]}.txt")

        return template_name.value["subject"], template_txt.render(**context), template_html.render(**context)
