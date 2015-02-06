from npyscreen import Form, FixedText, TitleSelectOne

class StartForm(Form):
    def create(self):
        self.add(FixedText, "Hello")
        self.add(TitleSelectOne, name="GraphType", values=["Map1", "Map2"], scroll_exit=True)

    def afterEditing(self):
        self.parentApp.setNextForm(None)
