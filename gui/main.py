from npyscreen import NPSAppManaged
from start_form import StartForm

class Application(NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", StartForm, name="Map of the Internet (2014/15)")
