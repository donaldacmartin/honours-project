from npyscreen import NPSAppManaged
from start_form import StartForm
from yearly_chart_form import YearlyChartForm

title = "Map of the Internet (2014/15)"

class Application(NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", StartForm, name=title)
        self.addForm("YearlyChart", YearlyChartForm, name="Create a Yearly Chart | " + title)
