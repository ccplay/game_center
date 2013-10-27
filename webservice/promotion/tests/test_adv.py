# -*- encoding=utf-8 -*-
from datetime import timedelta
import io
import os
from os.path import join, abspath, dirname
from django.contrib.contenttypes.models import ContentType
from django.core.files import File
from django.test import TestCase
from django.utils.timezone import now
from django.test.utils import override_settings
from should_dsl import should
from promotion.models import Advertisement, Place, Advertisement_Places
from fts.helpers import ApiDSL
import shutil

_fixture_dir = join(dirname(abspath(__file__)), 'fixtures')

class PlaceUnitTest(TestCase):

    def test_basic_create(self):
        place = Place(slug='mobile-home-top', help_text='手机端的首页顶部')
        place.save()
        except_place = Place.objects.get(pk=place.pk)
        self.assertEqual(except_place.slug, 'mobile-home-top')

class AdvUnitTest(TestCase):

    _fixture_dir = _fixture_dir
    _files_to_remove = []

    def setUp(self):
        _dir = join(self._fixture_dir, 'temp')
        os.makedirs(_dir, exist_ok=True)
        self._files_to_remove.append(_dir)
        super(AdvUnitTest, self).setUp()

    def tearDown(self):
        for f in self._files_to_remove:
            shutil.rmtree(f, ignore_errors=True)

    def create_place(self, **default):
        return Place.objects.create(**default)

    def test_basic_create_adverisement(self):
        pkg = ApiDSL.Given_i_have_published_package(self,
                                                        title='愤怒的小鸟：星球大战')
        adv = Advertisement(title='愤怒的小鸟 愤怒地登场', content=pkg)
        adv.save()
        self.assertEqual(adv.title, '愤怒的小鸟 愤怒地登场')
        self.assertEqual(adv.status, adv.STATUS.draft)
        self.assertEqual(adv.content.title, '愤怒的小鸟：星球大战')

        self.assertEqual(adv.is_published(), False)

    def test_adverisement_place_to_show(self):
        yestoday = now()-timedelta(days=1)
        pkg = ApiDSL.Given_i_have_published_package(self,
                                                    title='愤怒的小鸟：星球大战')
        adv = Advertisement.objects.create(title='愤怒的小鸟 愤怒地登场',
                            content=pkg,
                            released_datetime=yestoday,
                            status=Advertisement.STATUS.published
                            )
        p1 = self.create_place(slug='mobile-home-top')
        Advertisement_Places.objects.create(advertisement=adv, place=p1)
        p2 = self.create_place(slug='website-home-top')
        Advertisement_Places.objects.create(advertisement=adv, place=p2)
        self.assertEqual(2, adv.places.count())
        self.assertEqual(adv.is_published(), True)

    @override_settings(MEDIA_ROOT=join(_fixture_dir, 'temp'))
    def test_upload_file_to_path(self):
        pkg = ApiDSL.Given_i_have_published_package(self,
                                                    title='愤怒的小鸟：星球大战')
        cover = io.FileIO(join(self._fixture_dir, 'adv-cover.jpg'))
        adv = Advertisement(
            title='愤怒的小鸟 愤怒地登场',
            content=pkg,
            cover=File(cover),
            )
        adv.save()

        ct = ContentType.objects.get(model='package')
        adv_path_pattern = '.*/advertisement/%(date)s/%(ct)s-%(oid)d/cover.jpg' % {
            'date': now().strftime('%Y%m%d'),
            'ct': ct.model,
            'oid': pkg.pk
        }
        adv.cover.path |should| be_like(adv_path_pattern)
