from base_form import BaseForm
from npyscreen import TitleDateCombo, TitleMultiSelect

class YearlyChartForm(BaseForm):
    def create(self):
        self.add(TitleText, name="Start Year: ")
        self.nextrely += 1
        self.add(TitleText, name="End Year: ")
        self.nextrely += 1

        self.add(TitleMultiSelect, name="Charts", values=["IPv4 Address Space Usage",
                                                    "Most Common Prefix Allocation",
                                                    "Stacked Allocation of Prefixes",
                                                    "Prefixes as Horizontal Lines"])

    def afterEditing(self):
        self.parentApp.setNextForm(None)
