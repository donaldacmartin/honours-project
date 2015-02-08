from npyscreen import NPSAppManaged
from start_form import StartForm
from yearly_chart_form import YearlyChartForm

class Application(NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", StartForm, name="Map of the Internet (2014/15)")
        self.addForm("YearlyChart", YearlyChartForm, name="Create a Yearly Chart")
