from npyscreen import Form, Pager, TitleSelectOne

entry_text = ("Welcome to the University of Glasgow's Map of the Internet "
              "application for the year 2014/15. To proceed, please select "
              "of the options below.")

class StartForm(Form):
    def create(self):
        self.intro_text = self.add(Pager, values=entry_text, max_height=4, editable=False)
        self.add(TitleSelectOne,
                 name="Visualisation Type: ",
                 values=["Geographical Atlas",
                         "Internet Outage Diagram",
                         "Ring Graph",
                         "Yearly Chart"],
                 scroll_exit=True)

        self.intro_text.display()

    def whileEditing(self):
        self.intro_text.display()

    def afterEditing(self):
        self.parentApp.setNextForm(None)
