from django.db.models import Max
from django.core.cache import cache
from django.views.generic import DetailView, ListView, TemplateView

from armstrong.core.arm_layout.utils import get_layout_template_name

from .models import Institution, Enrollment, PublicEnrollment


class RenderModelDetailView(DetailView):
    """ shortcut to rendering an object using render_model """
    layout = None

    def get_template_names(self):
        return get_layout_template_name(self.object, self.layout)


class FunnelMixin(object):
    """ Adds `funnels` property to an `Institution` for the Funnel viz """
    def annotate_funnels(self, inst):
        enterdata = inst.admissions.all()

        # please excuse the horribleness of this
        funnels = []
        for year in enterdata:
            try:
                funnel = {'year': year.year}
                funnel[0] = 100
                funnel[1] = float(year.percent_of_applicants_admitted)
                funnel[2] = funnel[1] * float(year.percent_of_admitted_who_enrolled) / 100
                funnels.append(funnel)
            except TypeError:
                continue
        inst.funnels = funnels


class HomeView(TemplateView):
    template_name = "tx_highered/home.html"

    def get_short_list(self):
        """ list of high enrollment schools to make getting to UT one click """
        ipeds_queryset = (Enrollment.institution_values
                    .by_year(2010, enrollment_total='total')
                    .order_by('-enrollment_total')
                    .exclude(fice_id=None, ipeds_id=None))[:15]
        thecb_queryset = (PublicEnrollment.institution_values
                          .by_year(2010, enrollment_total='total')
                          .order_by('-enrollment_total')
                          .exclude(fice_id=None, ipeds_id=None))[:15]

        # Join the data with THECB taking priority
        joined_enrollment = {}
        for o in ipeds_queryset:
            joined_enrollment[o.id] = o
        for o in thecb_queryset:
            joined_enrollment[o.id] = o

        # Take the top schools by joined enrollment
        short_list = sorted(joined_enrollment.values(), reverse=True,
                            key=lambda o: o.enrollment_total)[:15]

        return short_list

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context['short_list'] = self.get_short_list()
        return context


class InstitutionListView(ListView):
    queryset = Institution.objects.filter(ipeds_id__isnull=False).\
        order_by('name')


class InstitutionDetailView(DetailView, FunnelMixin):
    model = Institution

    def get_context_data(self, *args, **kwargs):
        context = super(InstitutionDetailView, self).get_context_data(*args, **kwargs)
        context['prompt_for_chrome_frame'] = True
        # self.annotate_funnels(self.object)
        return context


######################### REPORTS ##########################
class TestScoresReport(InstitutionListView):
    template_name = "tx_highered/reports/testscores.html"

    def get_queryset(self):
        qs = super(TestScoresReport, self).get_queryset()
        qs = qs.exclude(testscores__isnull=True).order_by('name')
        for x in qs:
            x.scores = x.testscores.latest('year')
        return qs


class FunnelReport(InstitutionListView, FunnelMixin):
    template_name = "tx_highered/reports/funnel.html"

    def get_context_data(self, *args, **kwargs):
        # TODO this shouldn't be get_context_data
        context = super(FunnelReport, self).get_context_data(*args, **kwargs)
        for obj in self.object_list:
            self.annotate_funnels(obj)
        return context


class Top10RuleReport(InstitutionListView, FunnelMixin):
    template_name = "tx_highered/reports/top10.html"
    year_range = range(2000, 2012)

    def build_table(self, obj):
        raw_data = obj.admissions.filter(percent_top10rule__isnull=False).\
            values('year', 'percent_top10rule')
        data = dict([(x['year'], x['percent_top10rule']) for x in raw_data])
        return data

    def get_queryset(self):
        qs = super(Top10RuleReport, self).get_queryset()
        qs = qs.filter(institution_type='uni', is_private=False)
        # TODO prefetch admissions
        for x in qs:
            x.data = self.build_table(x)
        return qs

    def get_context_data(self, **kwargs):
        context = super(Top10RuleReport, self).get_context_data(**kwargs)
        context['year_range'] = self.year_range
        return context
