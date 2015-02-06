from npyscreen import Form, FixedText, TitleSelectOne

entry_text = """Welcome to the University of Glasgow's Map of the Internet
                application for the year 2014/15."""

class StartForm(Form):
    def create(self):
        self.add(FixedText, value="Hello")
        self.add(TitleSelectOne, name="GraphType", values=["Map1", "Map2"], scroll_exit=True)

    def afterEditing(self):
        self.parentApp.setNextForm(None)
