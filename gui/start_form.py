from textwrap import wrap
from npyscreen import Form, MultiLineEdit, TitleSelectOne

entry_text = ("Welcome to the University of Glasgow's Map of the Internet "
              "application for the year 2014/15. To proceed, please select "
              "of the options below.")

class StartForm(Form):
    def create(self):
        self.add(MultiLineEdit, value=self.wrap_text(entry_text), editable=False)
        self.add(TitleSelectOne,
                 name="Visualisation Type: ",
                 values=["Geographical Atlas",
                         "Internet Outage Diagram",
                         "Ring Graph",
                         "Yearly Chart"],
                 scroll_exit=True)

        self.DISPLAY()

    def wrap_text(self, text):
        wrapped_text = wrap(text, self.width)
        return "\n".join(wrapped_text)

    def afterEditing(self):
        self.parentApp.setNextForm(None)
