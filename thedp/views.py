from django.views.generic.detail import DetailView

from armstrong.core.arm_layout.utils import get_layout_template_name


class RenderModelDetailView(DetailView):
    """ shortcut to rendering an object using render_model """
    layout = None

    def get_template_names(self):
        return get_layout_template_name(self.object, self.layout)
