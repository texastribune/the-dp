Instacharts
===========
Instacharts are a way of quickly creating consistent tables from tabular
data stored in models. It is modeled on Django admin's changelist.

HowTo (basic example)
---------------------

In your settings.py:
Add instacharts to your INSTALLED_APPS

In your template, load the template tag and call it with a queryset like:

    {% load instachart %}
    <html><head><title>Price Trends</title><body>
    <h1>Price Trends</h1>
    {% instachart object_list %}
    </body></html>

You don't need to add anything to your models or views.

HowTo (advanced example)
------------------------

Import the instachart mixin in your models.py.
Mix it into your model definition, add the chart_series attribute as a list of what attributes to grab.

    from django.db import models
    from instachart.models import SimpleChart


    class PriceTrends(YearBasedInstitutionStatModel, SimpleChart):
        year = models.IntegerField(default=1970, verbose_name=u'Year')
        tuition_fees_in_state = models.IntegerField(null=True,
            verbose_name=u"In-State Tuition & Fees")
        tuition_fees_outof_state = models.IntegerField(null=True,
            verbose_name=u"Out-Of-State Tuition & Fees")
        books_and_supplies = models.IntegerField(null=True,
            verbose_name=u"Books & Supplies")

        @property
        def out_of_state_premium(self):
            return (self.tuition_Fees_outof_state / self.tuition_fees_in_state - 1) * 100

        def books_ratio(self):
            return self.books_and_supplies / self.tuition_fees_in_state
        books_ratio.verbose_name = u"Ratio of Book expenses vs Tuition and Fees (In-State)"

        chart_series = ('year',
                        'tuition_fees_outof_state',
                        'tuition_fees_in_state',
                        'out_of_state_premium',
                        'books_and_supplies',
                        'books_ratio')

And then the table generated would only use those fields. If you want to control
how the data is displayed, make it a list of tuples like:

        chart_series = (('year',),
                        ('tuition_fees_in_state', "$%d"),
                        ('tuition_fees_outof_state', "$%d"),
                        ('out_of_state_premium', "%d%%"),
                        ('books_and_supplies', "$%d"))

If you need custom html attributes in the header cells or body cells, you can add those like this:

        chart_head_attrs = (('tuition_fees_in_state', ('data-tablebars=1', 'class="span2"')),
                            ('tuition_fees_outof_state', ('data-tablebars=1', 'class="span2"')),
                            ('books_and_supplies', 'data-tablebars=1'))

        chart_body_attrs = (('tuition_fees_in_state', ('data-value="%d"',)),
                            ('tuition_fees_outof_state', ('data-value="%d"',)),
                            ('books_and_supplies', ('data-value="%d"',)))

If you only have on attribute, we are lazy friendly; you don't have to put it in a list.

Writing Custom Charts
---------------------
1. Add a new chart like `{% instachart object.pricetrends_set.all "pretty" %}`
2. Create the template, these context variables will be available to you: `object_list` and `chart_header`
3. If you load the instachart tags, you get formatting filters that can apply the head and body attrs to make cells.


TODO:
this code is now spaghetti code
