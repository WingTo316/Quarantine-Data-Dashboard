from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView


class Dashboard(TemplateView):
    template_name = "dashboard3.html"
    from dashboard.quarantine_datareader import Reader

    def get_context_data(self, **kwargs):

        connected, has_data, date = self.Reader.getDataAvailability()

        clsoe_contact = self.Reader.getCloseContact()
        non_close_contact = self.Reader.getNonCloseContact()

        context = {
            "connected": connected,
            "has_data": has_data,

            "data": {
                "date": str(date),
                "units_in_use" : self.Reader.getUnitInUse(),
                "units_available": self.Reader.getUnitAvailable(),
                "persons_quarantined": clsoe_contact + non_close_contact,
                "non_close_contacts": non_close_contact,
                "count_consistent": self.Reader.checkConsistency()
            },
            "centres" : self.Reader.getTop3Available()
        }
        return context