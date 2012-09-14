# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PublicGraduationRates'
        db.create_table('tx_highered_publicgraduationrates', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')(default=1970)),
            ('year_type', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('institution', self.gf('django.db.models.fields.related.ForeignKey')(related_name='publicgraduationrates', to=orm['tx_highered.Institution'])),
            ('associate_3yr', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2)),
            ('associate_4yr', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2)),
            ('associate_6yr', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2)),
            ('bachelor_3yr', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2)),
            ('bachelor_4yr', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2)),
            ('bachelor_5yr', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2)),
            ('bachelor_6yr', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2)),
        ))
        db.send_create_signal('tx_highered', ['PublicGraduationRates'])

        # Adding unique constraint on 'PublicGraduationRates', fields ['year', 'institution']
        db.create_unique('tx_highered_publicgraduationrates', ['year', 'institution_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'PublicGraduationRates', fields ['year', 'institution']
        db.delete_unique('tx_highered_publicgraduationrates', ['year', 'institution_id'])

        # Deleting model 'PublicGraduationRates'
        db.delete_table('tx_highered_publicgraduationrates')


    models = {
        'tx_highered.admissions': {
            'Meta': {'ordering': "['year']", 'unique_together': "(('year', 'institution'),)", 'object_name': 'Admissions'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'admissions'", 'to': "orm['tx_highered.Institution']"}),
            'number_admitted': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'number_admitted_who_enrolled': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'number_of_applicants': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'percent_of_admitted_who_enrolled': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '1', 'blank': 'True'}),
            'percent_of_applicants_admitted': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '1', 'blank': 'True'}),
            'percent_top10rule': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '1'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '1970'}),
            'year_type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'})
        },
        'tx_highered.enrollment': {
            'Meta': {'ordering': "['year']", 'unique_together': "(('year', 'institution'),)", 'object_name': 'Enrollment'},
            'fulltime': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'fulltime_equivalent': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'enrollment'", 'to': "orm['tx_highered.Institution']"}),
            'parttime': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'total': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'total_percent_asian': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'total_percent_black': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'total_percent_hispanic': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'total_percent_native': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'total_percent_unknown': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'total_percent_white': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '1970'}),
            'year_type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'})
        },
        'tx_highered.graduationrates': {
            'Meta': {'ordering': "['year']", 'unique_together': "(('year', 'institution'),)", 'object_name': 'GraduationRates'},
            'bachelor_4yr': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'bachelor_5yr': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'bachelor_6yr': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'graduationrates'", 'to': "orm['tx_highered.Institution']"}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '1970'}),
            'year_type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'})
        },
        'tx_highered.institution': {
            'Meta': {'object_name': 'Institution'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fice_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution_type': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'ipeds_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'ope_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '60', 'db_index': 'True'}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tx_highered.System']", 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'wikipedia_abstract': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'wikipedia_logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'wikipedia_scraped': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'wikipedia_seal': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'wikipedia_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        'tx_highered.pricetrends': {
            'Meta': {'ordering': "['year']", 'unique_together': "(('year', 'institution'),)", 'object_name': 'PriceTrends'},
            'books_and_supplies': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pricetrends'", 'to': "orm['tx_highered.Institution']"}),
            'room_and_board_off_campus': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'room_and_board_off_campus_w_family': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'room_and_board_on_campus': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'tuition_fees_in_state': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'tuition_fees_outof_state': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '1970'}),
            'year_type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'})
        },
        'tx_highered.publicenrollment': {
            'Meta': {'ordering': "['year']", 'unique_together': "(('year', 'institution'),)", 'object_name': 'PublicEnrollment'},
            'african_american_count': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'african_american_percent': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'asian_count': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'asian_percent': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'hispanic_count': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'hispanic_percent': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'publicenrollment'", 'to': "orm['tx_highered.Institution']"}),
            'international_count': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'international_percent': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'multiracial_count': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'multiracial_percent': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'native_american_count': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'native_american_percent': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'pacific_islander_count': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'pacific_islander_percent': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'total': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'unknown_count': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'unknown_percent': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'white_count': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'white_percent': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '1970'}),
            'year_type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'})
        },
        'tx_highered.publicgraduationrates': {
            'Meta': {'ordering': "['year']", 'unique_together': "(('year', 'institution'),)", 'object_name': 'PublicGraduationRates'},
            'associate_3yr': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2'}),
            'associate_4yr': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2'}),
            'associate_6yr': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2'}),
            'bachelor_3yr': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2'}),
            'bachelor_4yr': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2'}),
            'bachelor_5yr': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2'}),
            'bachelor_6yr': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'publicgraduationrates'", 'to': "orm['tx_highered.Institution']"}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '1970'}),
            'year_type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'})
        },
        'tx_highered.system': {
            'Meta': {'object_name': 'System'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '60', 'db_index': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        'tx_highered.testscores': {
            'Meta': {'ordering': "['year']", 'unique_together': "(('year', 'institution'),)", 'object_name': 'TestScores'},
            'act_composite_25th_percentile': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'act_composite_75th_percentile': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'act_english_25th_percentile': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'act_english_75th_percentile': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'act_math_25th_percentile': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'act_math_75th_percentile': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'act_submitted_number': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'act_submitted_percent': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'act_writing_25th_percentile': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'act_writing_75th_percentile': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'testscores'", 'to': "orm['tx_highered.Institution']"}),
            'sat_math_25th_percentile': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'sat_math_75th_percentile': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'sat_submitted_number': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'sat_submitted_percent': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'sat_verbal_25th_percentile': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'sat_verbal_75th_percentile': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'sat_writing_25th_percentile': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'sat_writing_75th_percentile': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '1970'}),
            'year_type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'})
        }
    }

    complete_apps = ['tx_highered']
