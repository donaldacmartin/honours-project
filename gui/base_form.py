from npyscreen import Form, MultiLineEdit
from textwrap import wrap

class BaseForm(Form):
    def add_wrapped_text(self, text):
        lines = wrap(text, self.columns)
        text  = "\n".join(wrapped_lines)
        self.add(MultiLineEdit, value=text, max_height=len(lines), editable=False)
