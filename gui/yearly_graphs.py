from npyscreen import Form, TitleText

class YearlyGraphForm(Form):
    def create(self):
        self.add(TitleText, name="Start Year")
        self.add(TitleText, name="End Year")

    def afterEditing(self):
        self.parentApp.setNextForm(None)
