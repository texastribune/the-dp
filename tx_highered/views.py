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
        num_pricetrends=Count('pricetrends', distinct=True),
        num_sattestscores=Count('testscores', distinct=True),
        num_admissions=Count('admissions', distinct=True)).order_by('name')


class InstitutionDetailView(DetailView):
    model = Institution


class SATListView(ListView):
    queryset = Institution.objects.filter(ipeds_id__isnull=False).\
               exclude(testscores__isnull=True).order_by('name')
    template_name_suffix = "_sats"

    def get_queryset(self):
        qs = self.queryset
        for x in qs:
            x.scores = x.testscores_set.latest('year')
        return qs
