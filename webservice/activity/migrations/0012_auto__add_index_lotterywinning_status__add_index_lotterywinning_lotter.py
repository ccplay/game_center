# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'LotteryWinning', fields ['status']
        db.create_index('activity_lotterywinning', ['status'])

        # Adding index on 'LotteryWinning', fields ['lottery', 'status']
        db.create_index('activity_lotterywinning', ['lottery_id', 'status'])

        # Adding index on 'LotteryPrize', fields ['status']
        db.create_index('activity_lotteryprize', ['status'])

        # Adding index on 'Lottery', fields ['status']
        db.create_index('activity_lottery', ['status'])


    def backwards(self, orm):
        # Removing index on 'Lottery', fields ['status']
        db.delete_index('activity_lottery', ['status'])

        # Removing index on 'LotteryPrize', fields ['status']
        db.delete_index('activity_lotteryprize', ['status'])

        # Removing index on 'LotteryWinning', fields ['lottery', 'status']
        db.delete_index('activity_lotterywinning', ['lottery_id', 'status'])

        # Removing index on 'LotteryWinning', fields ['status']
        db.delete_index('activity_lotterywinning', ['status'])


    models = {
        'account.user': {
            'Meta': {'db_table': "'auth_user'", 'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True', 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'activity.activity': {
            'Meta': {'index_together': "(('site', 'status'), ('site', 'status', 'publish_date', 'expiry_date'))", 'unique_together': "(('site', 'slug'),)", 'object_name': 'Activity'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '500'}),
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'default': "''", 'max_length': '500'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'to': "orm['generic.AssignedKeyword']", 'object_id_field': "'object_pk'"}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '500'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'null': 'True', 'max_length': '200'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '2000'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['account.User']", 'related_name': "'activitys'"}),
            'workspace': ('mezzanine.core.fields.FileField', [], {'blank': 'True', 'default': "''", 'max_length': '500'})
        },
        'activity.bulletin': {
            'Meta': {'index_together': "(('site', 'status'), ('site', 'status', 'publish_date', 'expiry_date'))", 'ordering': "('-publish_date',)", 'object_name': 'Bulletin'},
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'null': 'True', 'max_length': '200'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['account.User']", 'related_name': "'bulletins'"})
        },
        'activity.giftbag': {
            'Meta': {'index_together': "(('site', 'for_package'), ('site', 'for_package', 'for_version'), ('site', 'publish_date'), ('site', 'for_package', 'publish_date'), ('site', 'for_package', 'for_version', 'publish_date'), ('site', 'status', 'publish_date'), ('site', 'status', 'for_package', 'publish_date'), ('site', 'status', 'for_package', 'for_version', 'publish_date'))", 'ordering': "('-publish_date',)", 'object_name': 'GiftBag'},
            'cards_remaining_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cards_total_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'for_package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warehouse.Package']", 'related_name': "'giftbags'"}),
            'for_version': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warehouse.PackageVersion']", 'blank': 'True', 'null': 'True', 'related_name': "'giftbags'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'issue_description': ('django.db.models.fields.TextField', [], {}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['account.User']", 'on_delete': 'models.DO_NOTHING'}),
            'short_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'null': 'True', 'max_length': '200'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'usage_description': ('django.db.models.fields.TextField', [], {})
        },
        'activity.giftcard': {
            'Meta': {'index_together': "(('site', 'giftbag', 'owner'), ('site', 'giftbag', 'owner', 'took_date'), ('site', 'owner'))", 'unique_together': "(('site', 'giftbag', 'code'),)", 'object_name': 'GiftCard'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'giftbag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['activity.GiftBag']", 'related_name': "'cards'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['account.User']", 'on_delete': 'models.DO_NOTHING', 'null': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'took_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'})
        },
        'activity.lottery': {
            'Meta': {'index_together': "(('status',), ('status', 'publish_date'), ('status', 'publish_date', 'expiry_date'))", 'object_name': 'Lottery'},
            'cost_coin': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'null': 'True', 'max_length': '200'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'takepartin_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'takepartin_times': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        'activity.lotteryprize': {
            'Meta': {'index_together': "(('lottery', 'status'), ('lottery', 'group', 'level'))", 'unique_together': "(('lottery', 'group', 'level'),)", 'object_name': 'LotteryPrize'},
            'award_coin': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'group': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {}),
            'lottery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['activity.Lottery']", 'related_name': "'prizes'"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'total_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'win_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'win_prompt': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'activity.lotterywinning': {
            'Meta': {'index_together': "(('lottery', 'status'), ('lottery', 'prize'), ('prize', 'status'), ('prize', 'status', 'win_date'))", 'object_name': 'LotteryWinning'},
            'accept_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lottery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['activity.Lottery']", 'related_name': "'winnings'"}),
            'prize': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['activity.LotteryPrize']", 'related_name': "'winnings'"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1', 'db_index': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['account.User']", 'related_name': "'lotterywinnings'"}),
            'win_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        'activity.note': {
            'Meta': {'unique_together': "(('site', 'slug'),)", 'object_name': 'Note'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'comments.comment': {
            'Meta': {'db_table': "'django_comments'", 'ordering': "('submit_date',)", 'object_name': 'Comment'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '3000'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'related_name': "'content_type_set_for_comment'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'blank': 'True', 'null': 'True', 'max_length': '15'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_pk': ('django.db.models.fields.TextField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'submit_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['account.User']", 'blank': 'True', 'null': 'True', 'related_name': "'comment_comments'"}),
            'user_email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'user_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50'}),
            'user_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'generic.assignedkeyword': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'AssignedKeyword'},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['generic.Keyword']", 'related_name': "'assignments'"}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {})
        },
        'generic.keyword': {
            'Meta': {'object_name': 'Keyword'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '2000'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'generic.rating': {
            'Meta': {'object_name': 'Rating'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {}),
            'rating_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['account.User']", 'null': 'True', 'related_name': "'ratings'"}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'generic.threadedcomment': {
            'Meta': {'_ormbases': ['comments.Comment'], 'ordering': "('submit_date',)", 'object_name': 'ThreadedComment'},
            'by_author': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'comment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['comments.Comment']", 'primary_key': 'True', 'unique': 'True'}),
            'rating': ('mezzanine.generic.fields.RatingField', [], {'to': "orm['generic.Rating']", 'object_id_field': "'object_pk'"}),
            'rating_average': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'rating_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rating_sum': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'replied_to': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['generic.ThreadedComment']", 'null': 'True', 'related_name': "'comments'"})
        },
        'sites.site': {
            'Meta': {'db_table': "'django_site'", 'ordering': "('domain',)", 'object_name': 'Site'},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'taxonomy.category': {
            'Meta': {'ordering': "('ordering',)", 'unique_together': "(('site', 'slug'), ('site', 'name'))", 'object_name': 'Category'},
            'icon': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'default': "''", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mptt_level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_rgt': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '32'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'default': '0', 'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'to': "orm['taxonomy.Category']", 'blank': 'True', 'null': 'True', 'related_name': "'children'"}),
            'resources': ('toolkit.fields.MultiResourceField', [], {'to': "orm['toolkit.Resource']", 'object_id_field': "'object_pk'"}),
            'resources_count': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': '0'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'default': "''", 'max_length': '200'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'taxonomy.topic': {
            'Meta': {'ordering': "('ordering',)", 'unique_together': "(('site', 'slug'), ('site', 'name'))", 'object_name': 'Topic'},
            'cover': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'default': "''", 'max_length': '100'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'default': "''", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mptt_level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_rgt': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '32'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'default': '0', 'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'to': "orm['taxonomy.Topic']", 'blank': 'True', 'null': 'True', 'related_name': "'children'"}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True', 'db_index': 'True'}),
            'resources': ('toolkit.fields.MultiResourceField', [], {'to': "orm['toolkit.Resource']", 'object_id_field': "'object_pk'"}),
            'resources_count': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': '0'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32'}),
            'status': ('model_utils.fields.StatusField', [], {'blank': 'True', 'default': "'draft'", 'no_check_for_status': 'True', 'max_length': '100'}),
            'summary': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "''", 'max_length': '255'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        'taxonomy.topicalitem': {
            'Meta': {'index_together': "(('site', 'topic'), ('site', 'topic', 'content_type'), ('site', 'topic', 'content_type', 'object_id'), ('site', 'topic', 'content_type', 'object_id', 'ordering'), ('topic', 'content_type'))", 'ordering': "('ordering',)", 'unique_together': "(('topic', 'content_type', 'object_id'),)", 'object_name': 'TopicalItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'related_name': "'topic_content_type'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'default': '0', 'db_index': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['taxonomy.Topic']", 'related_name': "'items'"}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True', 'auto_now': 'True'})
        },
        'toolkit.resource': {
            'Meta': {'object_name': 'Resource', 'index_together': "(('site', 'content_type'), ('site', 'content_type', 'object_pk'), ('site', 'content_type', 'object_pk', 'kind'))", 'ordering': "('site', 'content_type', 'object_pk', 'kind')", 'unique_together': "(('site', 'content_type', 'object_pk', 'kind', 'alias'),)", 'db_table': "'common_resource'"},
            'alias': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "'default'", 'max_length': '50'}),
            'alt': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "''", 'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'related_name': "'+'"}),
            'file': ('mezzanine.core.fields.FileField', [], {'max_length': '500'}),
            'file_md5': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'default': 'None', 'max_length': '40'}),
            'file_size': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': '0'}),
            'height': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': '0', 'max_length': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'default': 'None', 'max_length': '100'}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'width': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': '0', 'max_length': '6'})
        },
        'toolkit.star': {
            'Meta': {'db_table': "'common_star'", 'object_name': 'Star'},
            'by_comment': ('django.db.models.fields.related.ForeignKey', [], {'on_delete': 'models.DO_NOTHING', 'null': 'True', 'to': "orm['generic.ThreadedComment']", 'blank': 'True', 'default': 'None', 'related_name': "'content_star'"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'related_name': "'+'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'blank': 'True', 'null': 'True', 'max_length': '15'}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {}),
            'rating_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'on_delete': 'models.DO_NOTHING', 'null': 'True', 'to': "orm['account.User']", 'blank': 'True', 'default': 'True', 'related_name': "'stars'"}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'warehouse.author': {
            'Meta': {'unique_together': "(('site', 'name'),)", 'object_name': 'Author'},
            'cover': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'default': "''", 'max_length': '100'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'unique': 'True'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'default': "''", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '16'}),
            'resources': ('toolkit.fields.MultiResourceField', [], {'to': "orm['toolkit.Resource']", 'object_id_field': "'object_pk'"}),
            'resources_count': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': '0'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'draft'", 'no_check_for_status': 'True', 'max_length': '100'}),
            'workspace': ('mezzanine.core.fields.FileField', [], {'blank': 'True', 'default': "''", 'max_length': '500'})
        },
        'warehouse.package': {
            'Meta': {'index_together': "(('site', 'id'), ('site', 'status'), ('site', 'status', 'released_datetime'))", 'unique_together': "(('site', 'package_name'),)", 'object_name': 'Package'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warehouse.Author']", 'related_name': "'packages'"}),
            'award_coin': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['taxonomy.Category']", 'blank': 'True', 'related_name': "'packages'", 'symmetrical': 'False'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'default': '0', 'db_index': 'True', 'max_length': '9'}),
            'has_award': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_version': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warehouse.PackageVersion']", 'null': 'True', 'default': 'None', 'related_name': "'+'"}),
            'main_category_names': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'}),
            'package_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255'}),
            'primary_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['taxonomy.Category']", 'blank': 'True', 'null': 'True', 'related_name': "'primary_packages'"}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True', 'db_index': 'True'}),
            'root_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['taxonomy.Category']", 'blank': 'True', 'null': 'True', 'related_name': "'root_packages'"}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'draft'", 'no_check_for_status': 'True', 'max_length': '100'}),
            'summary': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "''", 'max_length': '255'}),
            'tags_text': ('toolkit.fields.TagField', [], {'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True', 'db_index': 'True'}),
            'workspace': ('mezzanine.core.fields.FileField', [], {'blank': 'True', 'default': "''", 'max_length': '500'})
        },
        'warehouse.packageversion': {
            'Meta': {'index_together': "(('site', 'package'), ('site', 'id'), ('site', 'status'), ('site', 'status', 'released_datetime'), ('has_award',), ('site', 'has_award'), ('site', 'award_coin'), ('site', 'reported'), ('site', 'reported', 'status'))", 'unique_together': "(('site', 'package', 'version_code'),)", 'object_name': 'PackageVersion'},
            'award_coin': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'comments': ('comment.fields.CommentsField', [], {'to': "orm['generic.ThreadedComment']", 'object_id_field': "'object_pk'"}),
            'comments_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'default': "''", 'max_length': '500'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"}),
            'di_download': ('toolkit.fields.PkgFileField', [], {'blank': 'True', 'default': "''", 'max_length': '500'}),
            'di_download_md5': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'default': 'None', 'max_length': '40'}),
            'di_download_size': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': '0'}),
            'download': ('toolkit.fields.PkgFileField', [], {'blank': 'True', 'default': "''", 'max_length': '500'}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'default': '0', 'max_length': '9'}),
            'download_md5': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'default': 'None', 'max_length': '40'}),
            'download_size': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': '0'}),
            'has_award': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'default': "''", 'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warehouse.Package']", 'related_name': "'versions'"}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True', 'db_index': 'True'}),
            'reported': ('warehouse.models.PkgReportField', [], {'default': 'False'}),
            'reported_adv': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reported_gplay': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reported_network': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reported_root': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'resources': ('toolkit.fields.MultiResourceField', [], {'to': "orm['toolkit.Resource']", 'object_id_field': "'object_pk'"}),
            'resources_count': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': '0'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'stars': ('toolkit.fields.StarsField', [], {'to': "orm['toolkit.Star']", 'object_id_field': "'object_pk'"}),
            'stars_average': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'stars_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'stars_good_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'stars_good_rate': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'stars_low_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'stars_low_rate': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'stars_medium_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'stars_medium_rate': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'stars_sum': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'status': ('model_utils.fields.StatusField', [], {'blank': 'True', 'default': "'draft'", 'no_check_for_status': 'True', 'max_length': '100'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "''", 'max_length': '255'}),
            'summary': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "''", 'max_length': '255'}),
            'supported_devices': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['warehouse.SupportedDevice']", 'blank': 'True', 'symmetrical': 'False'}),
            'supported_features': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['warehouse.SupportedFeature']", 'blank': 'True', 'symmetrical': 'False'}),
            'supported_languages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['warehouse.SupportedLanguage']", 'blank': 'True', 'symmetrical': 'False'}),
            'tags_text': ('toolkit.fields.TagField', [], {'default': "''"}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'version_code': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '8'}),
            'version_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'whatsnew': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"}),
            'workspace': ('mezzanine.core.fields.FileField', [], {'blank': 'True', 'default': "''", 'max_length': '500'})
        },
        'warehouse.supporteddevice': {
            'Meta': {'unique_together': "(('site', 'code'),)", 'object_name': 'SupportedDevice'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '150', 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "''", 'max_length': '50'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"})
        },
        'warehouse.supportedfeature': {
            'Meta': {'unique_together': "(('site', 'code'),)", 'object_name': 'SupportedFeature'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "''", 'max_length': '30'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"})
        },
        'warehouse.supportedlanguage': {
            'Meta': {'object_name': 'SupportedLanguage'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True'})
        }
    }

    complete_apps = ['activity']