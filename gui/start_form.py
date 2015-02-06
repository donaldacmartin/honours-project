from npyscreen import Form, TitleText

class StartForm(Form):
    def create(self):
        self.add(TitleText, name="Hello", value="Hello")

    def afterEditing(self):
        self.parentApp.setNextForm(none)
