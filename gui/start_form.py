from npyscreen import Form, MultiLineEdit, TitleSelectOne

entry_text = ("Welcome to the University of Glasgow's Map of the Internet "
              "application\nfor the year 2014/15. To proceed, please select "
              "of the options below.")

class StartForm(Form):
    def create(self):
        self.add(MultiLineEdit, value=entry_text, max_height=2, editable=False, wrap=True)
        self.add(TitleSelectOne,
                 name="Visualisation Type: ",
                 values=["Geographical Atlas",
                         "Internet Outage Diagram",
                         "Ring Graph",
                         "Yearly Chart"],
                 scroll_exit=True)

        self.DISPLAY()

    def afterEditing(self):
        self.parentApp.setNextForm(None)
