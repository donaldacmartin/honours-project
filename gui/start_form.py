from npyscreen import Form, TitleText, TitleSelectOne

class StartForm(Form):
    def create(self):
        self.add(TitleText, name="Hello", value="Hello")
        self.add(TitleSelectOne, name="GraphType", values=["Map1", "Map2"], scroll_exit=true)

    def afterEditing(self):
        self.parentApp.setNextForm(None)
