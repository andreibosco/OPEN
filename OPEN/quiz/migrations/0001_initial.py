# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Quiz'
        db.create_table(u'quiz_quiz', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_deleted', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['course.Course'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['course.UploadedFile'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('quiz', ['Quiz'])

        # Adding model 'Question'
        db.create_table(u'quiz_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_deleted', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('quiz', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quiz.Quiz'])),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('quiz', ['Question'])

        # Adding model 'Choice'
        db.create_table(u'quiz_choice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_deleted', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('quiz', ['Choice'])

        # Adding model 'MCQuestion'
        db.create_table(u'quiz_mcquestion', (
            (u'question_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['quiz.Question'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('quiz', ['MCQuestion'])

        # Adding M2M table for field choice on 'MCQuestion'
        m2m_table_name = db.shorten_name(u'quiz_mcquestion_choice')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mcquestion', models.ForeignKey(orm['quiz.mcquestion'], null=False)),
            ('choice', models.ForeignKey(orm['quiz.choice'], null=False))
        ))
        db.create_unique(m2m_table_name, ['mcquestion_id', 'choice_id'])

        # Adding model 'MCQAnswer'
        db.create_table(u'quiz_mcqanswer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_deleted', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quiz.MCQuestion'])),
            ('correct', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quiz.Choice'])),
        ))
        db.send_create_signal('quiz', ['MCQAnswer'])

        # Adding model 'Likert'
        db.create_table(u'quiz_likert', (
            (u'question_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['quiz.Question'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('quiz', ['Likert'])

        # Adding model 'LikertAnswer'
        db.create_table(u'quiz_likertanswer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_deleted', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quiz.Likert'])),
            ('correct', self.gf('django.db.models.fields.CharField')(default='', max_length=2, null=True, blank=True)),
        ))
        db.send_create_signal('quiz', ['LikertAnswer'])

        # Adding model 'OpenEnded'
        db.create_table(u'quiz_openended', (
            (u'question_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['quiz.Question'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('quiz', ['OpenEnded'])

        # Adding model 'MCQuestionAttempt'
        db.create_table(u'quiz_mcquestionattempt', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_deleted', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('answer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quiz.Choice'])),
            ('mcquestion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quiz.MCQuestion'])),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('correct', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('no_of_attempt', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
        ))
        db.send_create_signal('quiz', ['MCQuestionAttempt'])

        # Adding model 'LikertAttempt'
        db.create_table(u'quiz_likertattempt', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_deleted', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('likert', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quiz.Likert'])),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('correct', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('no_of_attempt', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('scale', self.gf('django.db.models.fields.CharField')(default='', max_length=2, null=True, blank=True)),
        ))
        db.send_create_signal('quiz', ['LikertAttempt'])

        # Adding model 'OpenEndedAttempt'
        db.create_table(u'quiz_openendedattempt', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_deleted', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('openended', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quiz.OpenEnded'])),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('answer', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('no_of_attempt', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
        ))
        db.send_create_signal('quiz', ['OpenEndedAttempt'])


    def backwards(self, orm):
        # Deleting model 'Quiz'
        db.delete_table(u'quiz_quiz')

        # Deleting model 'Question'
        db.delete_table(u'quiz_question')

        # Deleting model 'Choice'
        db.delete_table(u'quiz_choice')

        # Deleting model 'MCQuestion'
        db.delete_table(u'quiz_mcquestion')

        # Removing M2M table for field choice on 'MCQuestion'
        db.delete_table(db.shorten_name(u'quiz_mcquestion_choice'))

        # Deleting model 'MCQAnswer'
        db.delete_table(u'quiz_mcqanswer')

        # Deleting model 'Likert'
        db.delete_table(u'quiz_likert')

        # Deleting model 'LikertAnswer'
        db.delete_table(u'quiz_likertanswer')

        # Deleting model 'OpenEnded'
        db.delete_table(u'quiz_openended')

        # Deleting model 'MCQuestionAttempt'
        db.delete_table(u'quiz_mcquestionattempt')

        # Deleting model 'LikertAttempt'
        db.delete_table(u'quiz_likertattempt')

        # Deleting model 'OpenEndedAttempt'
        db.delete_table(u'quiz_openendedattempt')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'course.course': {
            'Meta': {'object_name': 'Course'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_deleted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institute': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['institute.Institute']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'course.uploadedfile': {
            'Meta': {'object_name': 'UploadedFile'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['course.Course']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_deleted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uploader': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'uploads': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'})
        },
        'institute.institute': {
            'Meta': {'object_name': 'Institute'},
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_deleted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'})
        },
        'quiz.choice': {
            'Meta': {'object_name': 'Choice'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_deleted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'quiz.likert': {
            'Meta': {'object_name': 'Likert', '_ormbases': ['quiz.Question']},
            u'question_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['quiz.Question']", 'unique': 'True', 'primary_key': 'True'})
        },
        'quiz.likertanswer': {
            'Meta': {'object_name': 'LikertAnswer'},
            'correct': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_deleted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quiz.Likert']"})
        },
        'quiz.likertattempt': {
            'Meta': {'object_name': 'LikertAttempt'},
            'correct': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_deleted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likert': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quiz.Likert']"}),
            'no_of_attempt': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'scale': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'quiz.mcqanswer': {
            'Meta': {'object_name': 'MCQAnswer'},
            'correct': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quiz.Choice']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_deleted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quiz.MCQuestion']"})
        },
        'quiz.mcquestion': {
            'Meta': {'object_name': 'MCQuestion', '_ormbases': ['quiz.Question']},
            'choice': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['quiz.Choice']", 'symmetrical': 'False'}),
            u'question_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['quiz.Question']", 'unique': 'True', 'primary_key': 'True'})
        },
        'quiz.mcquestionattempt': {
            'Meta': {'object_name': 'MCQuestionAttempt'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quiz.Choice']"}),
            'correct': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_deleted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mcquestion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quiz.MCQuestion']"}),
            'no_of_attempt': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'quiz.openended': {
            'Meta': {'object_name': 'OpenEnded', '_ormbases': ['quiz.Question']},
            u'question_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['quiz.Question']", 'unique': 'True', 'primary_key': 'True'})
        },
        'quiz.openendedattempt': {
            'Meta': {'object_name': 'OpenEndedAttempt'},
            'answer': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_deleted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'no_of_attempt': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'openended': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quiz.OpenEnded']"}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'quiz.question': {
            'Meta': {'object_name': 'Question'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_deleted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quiz': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quiz.Quiz']"})
        },
        'quiz.quiz': {
            'Meta': {'object_name': 'Quiz'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['course.Course']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_deleted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['course.UploadedFile']"})
        }
    }

    complete_apps = ['quiz']