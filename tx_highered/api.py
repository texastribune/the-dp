import json

from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin

from tx_highered.models import Institution


class ApiView(View):
    def get(self, request, *args, **kwargs):
        data = self.get_content_data()
        content = json.dumps(data)
        return HttpResponse(content, content_type='application/json')


class EnrollmentApiView(SingleObjectMixin, ApiView):
    model = Institution

    def get_content_data(self):
        self.object = self.get_object()
        race_data = []
        for enrollment in self.object.enrollment.all():
            race_data.extend(enrollment.race_data())

        return race_data


class ReportView(SingleObjectMixin, ApiView):
    model = Institution
    report_name = None

    def get_content_data(self):
        self.object = self.get_object()
        return_data = []
        for obj in getattr(self.object, self.report_name).all():
            return_data.append(obj.__json__())
        return return_data


class AutocompleteApiView(ApiView):
    def get_content_data(self):
        data = []
        for i in Institution.objects.all():
            data.append({
                'uri': i.get_absolute_url(),
                'name': unicode(i),
            })

        return data


enrollment_api = EnrollmentApiView.as_view()
autocomplete_api = AutocompleteApiView.as_view()
