# -*- coding: utf-8 -*-
from model_utils import FieldTracker
from django.core.exceptions import ValidationError
from django.db import models, transaction, IntegrityError
from django.db.models.query import QuerySet
from django.utils.timezone import now
from mezzanine.core.models import TimeStamped
from mezzanine.utils.models import get_user_model_name

from activity.managers import GiftBagManager, GiftCardManager
from toolkit.models import PublishDisplayable, SiteRelated
from toolkit.helpers import current_request, get_global_site


class EmptyRemainingGiftCard(Exception):
    pass


user_model_name = get_user_model_name()


class GiftBag(PublishDisplayable,
              SiteRelated,
              TimeStamped,
              models.Model):

    objects = GiftBagManager()

    title = models.CharField(max_length=500)

    for_package = models.ForeignKey('warehouse.Package',
                                    verbose_name='应用',
                                    related_name='giftbags')

    for_version = models.ForeignKey('warehouse.PackageVersion',
                                    verbose_name='应用版本',
                                    related_name='giftbags',
                                    null=True,
                                    blank=True)

    summary = models.CharField(verbose_name='礼包内容', max_length=500)

    usage_description = models.TextField(verbose_name='使用方法')

    issue_description = models.TextField(verbose_name='发号说明')

    cards_remaining_count = models.IntegerField(default=0, editable=False)

    cards_total_count = models.IntegerField(default=0, editable=False)

    publisher = models.ForeignKey(user_model_name,
                                  on_delete=models.DO_NOTHING)

    def clean(self):
        super(GiftBag, self).clean()
        if self.for_version_id is not None:
            if self.for_version.package_id != self.for_package_id:
                raise ValidationError('PackageVersion (%s) Does not belong to Package (%s)' %(self.for_version,
                                                                                              self.for_package))

    def save(self, *args, **kwargs):
        if self.publisher_id is None:
            self.publisher = current_request().user
        return super(GiftBag, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '礼包'
        verbose_name_plural = '礼包'
        index_together = (
            ('site', 'for_package',),
            ('site', 'for_package', 'for_version'),

            ('site', 'publish_date', ),
            ('site', 'for_package', 'publish_date',),
            ('site', 'for_package', 'for_version', 'publish_date', ),
        )
        ordering = ('-publish_date', )

    @transaction.commit_on_success
    def take_by(self, user, took_date=None):
        dt = now().astimezone() if took_date is None else took_date
        try:
            card = self.cards.select_for_update().remaining()[0]
        except IndexError:
            raise EmptyRemainingGiftCard
        else:
            card.owner = user
            card.took_date = dt
            card.save()
            return card

    def __str__(self):
        return self.title


class GiftCardQuerySet(QuerySet):

    def remaining(self):
        table = self.model._meta.db_table
        return self.extra(where=['%s.owner_id IS NULL' % table])


class GiftCard(SiteRelated, models.Model):

    objects = GiftCardManager.for_queryset_class(GiftCardQuerySet)()

    giftbag = models.ForeignKey(GiftBag, related_name='cards')

    code = models.CharField(max_length=50, editable=False)

    owner = models.ForeignKey(user_model_name,
                              null=True,
                              blank=True,
                              on_delete=models.DO_NOTHING)

    took_date = models.DateTimeField(null=True, blank=True)

    tracker = FieldTracker()

    class Meta:
        verbose_name = '礼品码'
        verbose_name_plural = '礼品码'
        unique_together = (
            ('site', 'giftbag', 'code'),
        )
        index_together = (
            ('site', 'giftbag', 'owner'),
            ('site', 'giftbag', 'owner', 'took_date'),
        )

    def __str__(self):
        return "%s: %s" % (self.giftbag_id, self.code)


from import_export import resources, widgets, fields as ie_fields


class CodeWidget(widgets.CharWidget):

    def clean(self, value):
        if value:
            return value.strip()
        return value


class GiftCardResource(resources.ModelResource):

    #id = ie_fields.Field(attribute='pk', widget=widgets.IntegerWidget())

    giftbag = ie_fields.Field(column_name='giftbag',
                                 attribute='giftbag_id',
                                 widget=widgets.IntegerWidget())

    code = ie_fields.Field(column_name='code',
                           attribute='code',
                           widget=CodeWidget())

    class Meta:
        model = GiftCard
        fields = ('giftbag', 'code', )
        import_id_fields = ['giftbag', 'code']

    def get_instance(self, instance_loader, row):
        giftbag_field = self.fields['giftbag']
        code_field = self.fields['code']
        model = self._meta.model
        try:
            return model.objects.get(site_id=get_global_site().pk,
                                     giftbag_id=giftbag_field.clean(row),
                                     code=code_field.clean(row))
        except model.DoesNotExist:
            return None


from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete


@receiver(pre_save, sender=GiftCard)
def giftcard_pre_save_took(sender, instance, **kwargs):
    if instance.pk and instance.tracker.has_changed('owner_id'):
        instance._owner_changed = True


@receiver(post_save, sender=GiftCard)
def giftcard_post_save_took(sender, instance, created, **kwargs):
    if getattr(instance, '_owner_changed', False):
        del instance._owner_changed
        giftbag = instance.giftbag
        giftbag.cards_remaining_count = giftbag.cards.remaining().count()
        giftbag.save()


@receiver(post_save, sender=GiftCard)
def giftcard_created(sender, instance, created, **kwargs):
    if created:
        giftbag = instance.giftbag
        giftbag.cards_remaining_count = giftbag.cards.remaining().count()
        giftbag.cards_total_count = giftbag.cards.count()
        giftbag.save()


@receiver(post_delete, sender=GiftCard)
def giftcard_delete(sender, instance, **kwargs):
    try:
        giftbag = instance.giftbag
        giftbag.cards_remaining_count = giftbag.cards.remaining().count()
        giftbag.cards_total_count = giftbag.cards.count()
        giftbag.save()
    except GiftBag.DoesNotExist:
        pass
