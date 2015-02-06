from npyscreen import Form, Pager, TitleSelectOne

entry_text = ("Welcome to the University of Glasgow's Map of the Internet "
              "application for the year 2014/15. To proceed, please select "
              "of the options below.")

class StartForm(Form):
    def create(self):
        self.add(Pager, values=entry_text, max_height=4)
        self.add(TitleSelectOne,
                 name="Visualisation Type: ",
                 values=["Geographical Atlas",
                         "Internet Outage Diagram",
                         "Ring Graph",
                         "Yearly Chart"],
                 scroll_exit=True)

    def whileEditing(self):

    def afterEditing(self):
        self.parentApp.setNextForm(None)
