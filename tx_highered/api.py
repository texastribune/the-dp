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


enrollment_api = EnrollmentApiView.as_view()
