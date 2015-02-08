from base_form import BaseForm
from npyscreen import TitleSelectOne

entry_text = ("Welcome to the University of Glasgow's Map of the Internet "
              "application for the year 2014/15. To proceed, please select "
              "of the options below.")

class StartForm(BaseForm):
    def create(self):
        self.add_wrapped_text(entry_text)
        self.add(TitleSelectOne,
                 name="Visualisation Type: ",
                 values=["Geographical Atlas",
                         "Internet Outage Diagram",
                         "Ring Graph",
                         "Yearly Chart"],
                 scroll_exit=True)

    def afterEditing(self):
        self.parentApp.setNextForm(None)
