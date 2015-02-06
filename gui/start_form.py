from npyscreen import Form, TextBox, TitleSelectOne

class StartForm(Form):
    def create(self):
        self.add(TextBox, display_value="Hello")
        self.add(TitleSelectOne, name="GraphType", values=["Map1", "Map2"], scroll_exit=True)

    def afterEditing(self):
        self.parentApp.setNextForm(None)
