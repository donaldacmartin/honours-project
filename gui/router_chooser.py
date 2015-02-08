from base_form import BaseForm
from npyscreen import TitleMultiSelect

info_text = ("Here, it is possible to choose to parse data dumped from one or "
             "more specific routers. Please pick at least one of the following "
             "options to continue.")

class RouterChooserForm(BaseForm):
    def create(self):
        self.add_wrapped_text(info_text)
        self.nextrely += 1

        self.add(TitleMultiSelect,
                 name="Routers to Parse: ",
                 values=["OIX  - Oregon Internet Exchange",
                         "EQIX - Unknown",
                         "ISC  - Unknown",
                         "RV1  - Routeviews Router 1 (Uni of Oregon)",
                         "RV3  - Routeviews Router 3 (Uni of Oregon)",
                         "RV4  - Routeviews Router 4 (Uni of Oregon)"],
                 scroll_exit=True)
