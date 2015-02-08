from base_form import BaseForm
from npyscreen import TitleDateCombo, TitleMultiSelect

class YearlyChartForm(BaseForm):
    def create(self):
        self.add(TitleDateCombo, name="Start Year: ")
        self.add(TitleDateCombo, name="End Year: ")

        self.add(TitleMultiSelect, name="", values=["IPv4 Address Space Usage",
                                                    "Most Common Prefix Allocation",
                                                    "Stacked Allocation of Prefixes",
                                                    "Prefixes as Horizontal Lines"])
