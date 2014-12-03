import json

from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin

from tx_highered.models import Institution


class JSON(int):
    """
    Wraps encoded JSON and ensures it passes through the default encoder
    without being encoded again.

    Relies on an implementation detail of the built-in json module. int
    values are encoded by calling `__str__` on them, so if that changes,
    this code will break.
    """
    def __new__(cls, content):
        o = super(JSON, cls).__new__(cls)
        o.content = str(content)
        return o

    def __str__(self):
        return self.content


class ApiView(View):
    def get(self, request, *args, **kwargs):
        data = self.get_content_data()
        content = json.dumps(data)
        return HttpResponse(content, content_type='application/json')


class EnrollmentApiView(SingleObjectMixin, ApiView):
    model = Institution

    def get_content_data(self):
        self.object = self.get_object()

        # Use IPEDS enrollment data if this is a private university;
        # otherwise use THECB data.
        if self.object.is_private:
            qs = self.object.enrollment.all()
        else:
            qs = self.object.publicenrollment.all()

        race_data = []
        for enrollment in qs:
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


class InstitutionApiView(ApiView):
    available_fields = ['is_private', 'enrollment_fte', 'city', 'geojson']
    queryset = Institution.objects.published()

    def get_content_data(self):
        data = []
        for i in self.queryset:
            object_data = {'uri': i.get_absolute_url(), 'name': i.name}
            for field in self.request.GET.get('fields', '').split(','):
                if field in self.available_fields:
                    object_data[field] = getattr(i, field)
            data.append(object_data)

        return data


enrollment_api = EnrollmentApiView.as_view()
institution_api = InstitutionApiView.as_view()
