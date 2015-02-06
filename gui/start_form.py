from npyscreen import Form, TitleText

class StartForm(Form):
    def create(self):
        self.add(TitleText, name="Hello", value="Hello"
        self.graphType(TitleSelectOne, name="GraphType", values=["Map1", "Map2"], scroll_exit=True)

    def afterEditing(self):
        self.parentApp.setNextForm(None)
