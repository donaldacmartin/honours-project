from base_form import BaseForm
from npyscreen import TitleText, TitleMultiSelect

info_text = ("This option will produce a graph with years along the X-axis and "
             "your chosen value along the Y-axis. Please select one or more of "
             "the options below to continue.")

class YearlyChartForm(BaseForm):
    def create(self):
        self.add_wrapped_text(info_text)
        self.nextrely += 1
        self.add(TitleText, name="Start Year: ", value=1997)
        self.nextrely += 1
        self.add(TitleText, name="End Year: ", value=2014)
        self.nextrely += 1

        self.add(TitleMultiSelect,
                 name="Desired Charts: ",
                 values=["IPv4 Address Space Usage",
                         "Most Common Prefix Allocation",
                         "Stacked Allocation of Prefixes",
                         "Prefixes as Horizontal Lines"],
                 scroll_exit=True)

    def afterEditing(self):
        self.parentApp.setNextForm(None)
