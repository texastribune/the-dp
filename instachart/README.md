Instacharts
===========

HowTo (basic example)
---------------------

In your settings.py:
Add instacharts to your INSTALLED_APPS

In your template, load the template tags:
`{% load instachart %}`


And in your template, you can make a table with a queryset with:

    <h3>Price Trends</h3>
    {% simple_chart object.pricetrends_set.all %}

HowTo (advanced example)
------------------------

Import the mixin in your models.py:
`from instachart.models import SimpleChart`


And mix it into your model, add the chart_series attribute as a tuple of
(field name, string formatting, tuple of custom header attributes):

    class PriceTrends(YearBasedInstitutionStatModel, SimpleChart):
        tuition_fees_in_state = models.IntegerField(null=True,
            verbose_name=u"In-State Tuition & Fees")
        tuition_fees_outof_state = models.IntegerField(null=True,
            verbose_name=u"Out-Of-State Tuition & Fees")
        books_and_supplies = models.IntegerField(null=True,
            verbose_name=u"Books & Supplies")

        chart_series = (('year', "%d"),
                        ('tuition_fees_in_state', "$%d", ('data-tablebars=1',)),
                        ('tuition_fees_outof_state', "$%d", ('data-tablebars=1',)),
                        ('books_and_supplies', "$%d", ('data-tablebars=1',)))

Writing Custom Charts
---------------------
1. Add a new chart like {% simple_chart object.pricetrends_set.all "pretty" %}
2. Create the template, these context variables will be available to you: object_list and chart_header


TODO:
this code is now spaghetti code
