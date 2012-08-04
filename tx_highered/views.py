from django.db.models import Count, ObjectDoesNotExist
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

    def get_context_data(self, *args, **kwargs):
        context = super(InstitutionDetailView, self).get_context_data(*args, **kwargs)
        inst = self.object
        enterdata = inst.admissions_set.all()
        exitdata = inst.graduationrates_set.all()

        # please excuse the horribleness of this
        funnels = []
        for year in enterdata:
            funnel = {'year': year.year}
            funnel[0] = 100
            funnel[1] = float(year.percent_of_applicants_admitted)
            funnel[2] = funnel[1] * float(year.percent_of_admitted_who_enrolled) / 100
            try:
                year = exitdata.get(year=year.year)
            except ObjectDoesNotExist:
                continue
            funnel[3] = year.bachelor_4yr
            funnel[4] = year.bachelor_5yr
            funnel[5] = year.bachelor_6yr
            funnels.append(funnel)
        context['funnels'] = funnels
        return context


class SATListView(ListView):
    queryset = Institution.objects.filter(ipeds_id__isnull=False).\
               exclude(testscores__isnull=True).order_by('name')
    template_name_suffix = "_sats"

    def get_queryset(self):
        qs = self.queryset
        for x in qs:
            x.scores = x.testscores_set.latest('year')
        return qs


class FunnelListView(InstitutionListView):
    template_name = "tx_highered/reports/funnel.html"

    def annotate_funnels(self, inst):
        enterdata = inst.admissions_set.all()
        exitdata = inst.graduationrates_set.all()

        # please excuse the horribleness of this
        funnels = []
        for year in enterdata:
            funnel = {'year': year.year}
            funnel[0] = 100
            funnel[1] = float(year.percent_of_applicants_admitted)
            funnel[2] = funnel[1] * float(year.percent_of_admitted_who_enrolled) / 100
            try:
                year = exitdata.get(year=year.year)
            except ObjectDoesNotExist:
                continue
            funnel[3] = year.bachelor_4yr
            funnel[4] = year.bachelor_5yr
            funnel[5] = year.bachelor_6yr
            funnels.append(funnel)
        inst.funnels = funnels

    def get_context_data(self, *args, **kwargs):
        # TODO this shouldn't be get_context_data
        context = super(FunnelListView, self).get_context_data(*args, **kwargs)
        for obj in self.object_list:
            self.annotate_funnels(obj)
        return context
