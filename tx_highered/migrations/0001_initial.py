# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'System'
        db.create_table('tx_highered_system', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=60, db_index=True)),
        ))
        db.send_create_signal('tx_highered', ['System'])

        # Adding model 'Institution'
        db.create_table('tx_highered_institution', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('wikipedia_title', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('wikipedia_abstract', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('wikipedia_seal', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('wikipedia_logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('wikipedia_scraped', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=60, db_index=True)),
            ('is_private', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('institution_type', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('system', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tx_highered.System'], null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('ipeds_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('fice_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('ope_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('tx_highered', ['Institution'])

        # Adding model 'PriceTrends'
        db.create_table('tx_highered_pricetrends', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')(default=1970)),
            ('year_type', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('institution', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pricetrends', to=orm['tx_highered.Institution'])),
            ('tuition_fees_in_state', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('tuition_fees_outof_state', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('books_and_supplies', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('room_and_board_on_campus', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('room_and_board_off_campus', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('room_and_board_off_campus_w_family', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('tx_highered', ['PriceTrends'])

        # Adding unique constraint on 'PriceTrends', fields ['year', 'institution']
        db.create_unique('tx_highered_pricetrends', ['year', 'institution_id'])

        # Adding model 'TestScores'
        db.create_table('tx_highered_testscores', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')(default=1970)),
            ('year_type', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('institution', self.gf('django.db.models.fields.related.ForeignKey')(related_name='testscores', to=orm['tx_highered.Institution'])),
            ('sat_verbal_25th_percentile', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('sat_verbal_75th_percentile', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('sat_math_25th_percentile', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('sat_math_75th_percentile', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('sat_writing_25th_percentile', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('sat_writing_75th_percentile', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('sat_submitted_number', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('sat_submitted_percent', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('act_composite_25th_percentile', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('act_composite_75th_percentile', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('act_english_25th_percentile', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('act_english_75th_percentile', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('act_math_25th_percentile', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('act_math_75th_percentile', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('act_writing_25th_percentile', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('act_writing_75th_percentile', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('act_submitted_number', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('act_submitted_percent', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('tx_highered', ['TestScores'])

        # Adding unique constraint on 'TestScores', fields ['year', 'institution']
        db.create_unique('tx_highered_testscores', ['year', 'institution_id'])

        # Adding model 'Admissions'
        db.create_table('tx_highered_admissions', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')(default=1970)),
            ('year_type', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('institution', self.gf('django.db.models.fields.related.ForeignKey')(related_name='admissions', to=orm['tx_highered.Institution'])),
            ('number_of_applicants', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('number_admitted', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('number_admitted_who_enrolled', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('percent_of_applicants_admitted', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=1, blank=True)),
            ('percent_of_admitted_who_enrolled', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=1, blank=True)),
            ('percent_top10rule', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=1)),
        ))
        db.send_create_signal('tx_highered', ['Admissions'])

        # Adding unique constraint on 'Admissions', fields ['year', 'institution']
        db.create_unique('tx_highered_admissions', ['year', 'institution_id'])

        # Adding model 'Enrollment'
        db.create_table('tx_highered_enrollment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')(default=1970)),
            ('year_type', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('institution', self.gf('django.db.models.fields.related.ForeignKey')(related_name='enrollment', to=orm['tx_highered.Institution'])),
            ('total', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('fulltime_equivalent', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('fulltime', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('parttime', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('total_percent_white', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('total_percent_black', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('total_percent_hispanic', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('total_percent_native', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('total_percent_asian', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('total_percent_unknown', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('tx_highered', ['Enrollment'])

        # Adding unique constraint on 'Enrollment', fields ['year', 'institution']
        db.create_unique('tx_highered_enrollment', ['year', 'institution_id'])

        # Adding model 'GraduationRates'
        db.create_table('tx_highered_graduationrates', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')(default=1970)),
            ('year_type', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('institution', self.gf('django.db.models.fields.related.ForeignKey')(related_name='graduationrates', to=orm['tx_highered.Institution'])),
            ('bachelor_4yr', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('bachelor_5yr', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('bachelor_6yr', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('tx_highered', ['GraduationRates'])

        # Adding unique constraint on 'GraduationRates', fields ['year', 'institution']
        db.create_unique('tx_highered_graduationrates', ['year', 'institution_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'GraduationRates', fields ['year', 'institution']
        db.delete_unique('tx_highered_graduationrates', ['year', 'institution_id'])

        # Removing unique constraint on 'Enrollment', fields ['year', 'institution']
        db.delete_unique('tx_highered_enrollment', ['year', 'institution_id'])

        # Removing unique constraint on 'Admissions', fields ['year', 'institution']
        db.delete_unique('tx_highered_admissions', ['year', 'institution_id'])

        # Removing unique constraint on 'TestScores', fields ['year', 'institution']
        db.delete_unique('tx_highered_testscores', ['year', 'institution_id'])

        # Removing unique constraint on 'PriceTrends', fields ['year', 'institution']
        db.delete_unique('tx_highered_pricetrends', ['year', 'institution_id'])

        # Deleting model 'System'
        db.delete_table('tx_highered_system')

        # Deleting model 'Institution'
        db.delete_table('tx_highered_institution')

        # Deleting model 'PriceTrends'
        db.delete_table('tx_highered_pricetrends')

        # Deleting model 'TestScores'
        db.delete_table('tx_highered_testscores')

        # Deleting model 'Admissions'
        db.delete_table('tx_highered_admissions')

        # Deleting model 'Enrollment'
        db.delete_table('tx_highered_enrollment')

        # Deleting model 'GraduationRates'
        db.delete_table('tx_highered_graduationrates')


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
        'tx_highered.system': {
            'Meta': {'object_name': 'System'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
