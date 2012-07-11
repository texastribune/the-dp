from django.db.models import Count
from django.views.generic import DetailView, ListView

from armstrong.core.arm_layout.utils import get_layout_template_name

from .models import Institution


class RenderModelDetailView(DetailView):
    """ shortcut to rendering an object using render_model """
    layout = None

    def get_template_names(self):
        return get_layout_template_name(self.object, self.layout)


class InstitutionListView(ListView):
    queryset = Institution.objects.filter(ipeds_id__isnull=False).annotate(
        num_pricetrends=Count('pricetrend', distinct=True),
        num_sattestscores=Count('testscores', distinct=True),
        num_admissions=Count('admissions', distinct=True)).order_by('name')


class SATListView(ListView):
    queryset = Institution.objects.filter(ipeds_id__isnull=False).\
               exclude(testscores__isnull=True).order_by('name')
    template_name_suffix = "_sats"

    def get_queryset(self):
        qs = self.queryset
        MIN = 300
        ACTMIN = 10
        multiplier = (800 - MIN) / (36 - ACTMIN)
        for x in qs:
            x.scores = x.testscores_set.latest('year')
            if x.scores.sat_verbal_25th_percentile:
                x.bar_v = dict(left=x.scores.sat_verbal_25th_percentile - MIN,
                          width=x.scores.sat_verbal_75th_percentile - x.scores.sat_verbal_25th_percentile)
            if x.scores.sat_math_25th_percentile:
                x.bar_m = dict(left=x.scores.sat_math_25th_percentile - MIN,
                          width=x.scores.sat_math_75th_percentile - x.scores.sat_math_25th_percentile)
            if x.scores.act_composite_25th_percentile:
                x.bar_a = dict(left=multiplier * (x.scores.act_composite_25th_percentile - ACTMIN),
                          width=multiplier * (x.scores.act_composite_75th_percentile - x.scores.act_composite_25th_percentile))
        return qs


class DegreesListView(ListView):
    queryset = Institution.objects.filter(ipeds_id__isnull=False).exclude(degreescertificates__isnull=True).order_by('name')

    def get_queryset(self):
        qs = self.queryset
        for x in qs:
            data = x.degreescertificates_set.filter(gender='Total', raceethnicity='Total').latest('year')
            x.num_pricetrends = data.year
            x.num_sattestscores = data.value
        return qs
