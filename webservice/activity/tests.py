# -*- coding: utf-8 -*-
from unittest.mock import Mock
from django.test import TestCase


class WarehouseDSL(object):
    pass


class ActivityDSL(object):

    def giftbag_already_exists_for(self, package, version=None,
                                   published_datetime=None,
                                   expire_datetime=None,
                                   ):
        pass

    def gitbag_already_has_many_gitcard(self, gitbag, card_code):
        pass


class GitBagTest(TestCase):

    def _test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


from should_dsl import should
from account.models import User
from activity.documents.actions.comment import *


from mongoengine import register_connection
from django.conf import settings
con_key = 'data_center'
con_opts = settings.MOGOENGINE_CONNECTS[con_key]
register_connection(alias=con_key,
                    name=con_opts.get('name'),
                    host=con_opts.get('host'),
                    port=con_opts.get('port'))

import logging
logger = logging.getLogger('console')


class TaskTestCase(TestCase):

    action_class = None

    task_class = None

    rule_class = None

    def get_rule(self):
        try:
            rule = self.rule_class.objects.get(code=self.rule_class.CODE)
        except:
            rule = self.rule_class()
            rule.save()
        return rule

    def tearDown(self):
        self.task_class.objects.delete()
        self.action_class.objects.delete()
        self.rule_class.objects.delete()


class CommentTestCase(TaskTestCase):

    action_class = CommentAction

    task_class = CommentTask

    rule_class = CommentTaskRule

    rule = None

    def get_rule(self):
        try:
            rule = CommentTaskRule.objects.get(code=CommentTaskRule.CODE)
        except:
            rule = CommentTaskRule(name='post comment', comment_count=3)
            rule.save()
        return rule

    def test_add_duplicate_action(self):
        self.rule = self.get_rule()
        self.rule.comment_count |should| equal_to(3)

        user = User.objects.get(username='killuavx')
        task = CommentTask()
        self.task = task

        same_cmt = user.comment_comments.all()[1]
        action = CommentAction(content=same_cmt)
        task.process(user=user, action=action, rule=self.rule)

        task.status |should| equal_to(CommentTask.STATUS.inprogress)
        task.actions |should| have(1).items

        action = CommentAction(content=same_cmt)
        (task.process, user, action, task.rule) |should| throw(TaskConditionDoesNotMeet)
        task.actions |should| have(1).items

    def test_finish_comment_task(self):
        self.rule = self.get_rule()
        self.rule.comment_count |should| equal_to(3)

        user = User.objects.get(username='killuavx')
        task = CommentTask()
        self.task = task
        task.make_done = Mock(return_value=None)

        cmt1 = user.comment_comments.all()[1]
        action = CommentAction(content=cmt1)
        task.process(user=user, action=action, rule=self.rule)
        task.make_done.called |should| be(False)

        task.status |should| equal_to(CommentTask.STATUS.inprogress)
        task.actions |should| have(1).items

        cmt2 = user.comment_comments.all()[2]
        action = CommentAction(content=cmt2)
        task.process(user=user, action=action, rule=self.rule)
        task.make_done.called |should| be(False)

        task.status |should| equal_to(CommentTask.STATUS.inprogress)
        task.actions |should| have(2).items

        cmt3 = user.comment_comments.all()[10]
        action = CommentAction(content=cmt3)
        task.process(user=user, action=action, rule=self.rule)
        task.make_done.called |should| be(True)

        task.status |should| equal_to(CommentTask.STATUS.done)
        task.actions |should| have(3).items

        cmt3 = user.comment_comments.all()[8]
        action = CommentAction(content=cmt3)
        (task.process, user, action, task.rule) |should| throw(TaskAlreadyDone)
        task.make_done.call_count |should| equal_to(1)

    def test_factory(self):
        self.rule = self.get_rule().comment_count |should| equal_to(3)
        user = User.objects.get(username='killuavx')
        cmt1 = user.comment_comments.all()[1]
        cmt2 = user.comment_comments.all()[2]
        cmt3 = user.comment_comments.all()[3]
        cmt4 = user.comment_comments.all()[4]
        CommentTask.make_done = Mock(return_value=None)

        action_datetime = now().astimezone()

        task1, user, action, rule = CommentTask.factory(comment=cmt1, action_datetime=action_datetime)
        task1.process(user=user, action=action, rule=rule)
        task1.make_done.called |should| be(False)
        task1.status |should| equal_to(CommentTask.STATUS.inprogress)
        task1.actions |should| have(1).items

        task2, user, action, rule = CommentTask.factory(comment=cmt2, action_datetime=action_datetime)
        task2.id |should| equal_to(task1.id)

        task2.process(user=user, action=action, rule=rule)
        task2.make_done.called |should| be(False)
        task2.status |should| equal_to(CommentTask.STATUS.inprogress)
        task2.actions |should| have(2).items

        task3, user, action, rule = CommentTask.factory(comment=cmt3, action_datetime=action_datetime)
        task3.process(user=user, action=action, rule=rule)
        task3.make_done.called |should| be(True)
        task3.status |should| equal_to(CommentTask.STATUS.done)
        task3.actions |should| have(3).items

        cmt4 = user.comment_comments.all()[4]
        task4, user, action, rule = CommentTask.factory(comment=cmt4, action_datetime=action_datetime)
        (task4.process, user, action, task4.rule) |should| throw(TaskAlreadyDone)
        task4.make_done.call_count |should| equal_to(1)


from activity.documents.actions.signin import *


class SigninTestCase(TaskTestCase):

    action_class = SigninAction

    task_class = SigninTask

    rule_class = SigninTaskRule

    rule = None

    def test_signin_task(self):
        user = User.objects.get(username='killuavx')
        task = SigninTask()
        self.task = task
        self.rule = self.get_rule()

        action = SigninAction(user=user)
        task.make_done = Mock(return_value=None)
        task.process(user=user, action=action, rule=self.rule)
        task.make_done.called |should| be(True)

        task.status |should| equal_to(SigninTaskRule.STATUS.done)
        task.actions |should| have(1).items

        action = SigninAction(user=user)
        (task.process, user, action, task.rule) |should| throw(TaskAlreadyDone)
        task.make_done.call_count |should| equal_to(1)

    def test_factory(self):
        user = User.objects.get(username='killuavx')
        task, user, action, rule = SigninTask.factory(user=user,
                                                      ip_address='127.0.0.1')
        task.make_done = Mock(return_value=None)
        task.process(user=user, action=action, rule=rule)
        task.make_done.called |should| be(True)

        action.ip_address |should| equal_to('127.0.0.1')
        task.ip_address |should| equal_to('127.0.0.1')

        task.status |should| equal_to(SigninTaskRule.STATUS.done)
        task.actions |should| have(1).items

        sec_task, user, sec_action, rule = SigninTask.factory(user=user,
                                                              ip_address='127.0.0.2')

        sec_task.id |should| equal_to(task.id)
        sec_action.ip_address |should| equal_to('127.0.0.2')

        (task.process, user, action, task.rule) |should| throw(TaskAlreadyDone)
        task.make_done.call_count |should| equal_to(1)
        sec_task.ip_address |should| equal_to('127.0.0.1')


from activity.documents.actions.share import *
from warehouse.models import PackageVersion


class ShareTestCase(TaskTestCase):

    task_class = ShareTask

    action_class = ShareAction

    rule_class = ShareTaskRule

    @classmethod
    def setUpClass(cls):
        cls.task_class.make_done = Mock(return_value=None)

    def get_rule(self):
        try:
            rule = self.rule_class.objects.get(code=self.rule_class.CODE)
        except:
            rule = self.rule_class(share_count=3)
            rule.save()
        return rule

    def test_factory(self):
        self.rule = self.get_rule()
        self.rule.share_count |should| equal_to(3)
        user = User.objects.get(username='killuavx')
        ip_address = '127.0.0.1'
        queryset = PackageVersion.objects.published()

        version1 = queryset[0]
        task1, user, action, rule = ShareTask.factory(user=user,
                                                      version=version1,
                                                      ip_address=ip_address)
        task1.process(user=user, action=action, rule=rule)
        task1.make_done.called |should| be(False)
        task1.actions |should| have(1).items
        task1.status |should| equal_to(ShareTaskRule.STATUS.inprogress)

        version2 = queryset[1]
        task2, user, action, rule = ShareTask.factory(user=user,
                                                      version=version2,
                                                      ip_address=ip_address)

        task2.id |should| equal_to(task1.id)

        task2.process(user=user, action=action, rule=rule)
        task2.make_done.called |should| be(False)
        task2.actions |should| have(2).items
        task2.status |should| equal_to(ShareTaskRule.STATUS.inprogress)

        version3 = queryset[2]
        task3, user, action, rule = ShareTask.factory(user=user,
                                                      version=version3,
                                                      ip_address=ip_address)
        task3.process(user=user, action=action, rule=rule)
        task3.make_done.called |should| be(True)
        task3.actions |should| have(3).items
        task3.status |should| equal_to(ShareTaskRule.STATUS.done)


        version4 = queryset[3]
        task4, user, action, rule = ShareTask.factory(user=user,
                                                      version=version4,
                                                      ip_address=ip_address)
        (task4.process, user, action, rule) |should| throw(TaskAlreadyDone)
        task4.actions |should| have(3).items


    def test_factory_duplicate(self):
        self.rule = self.get_rule()
        self.rule.share_count |should| equal_to(3)
        user = User.objects.get(username='killuavx')
        ip_address = '127.0.0.1'
        queryset = PackageVersion.objects.published()

        same_version = version = queryset[0]
        task1, user, action, rule = ShareTask.factory(user=user,
                                                      version=version,
                                                      ip_address=ip_address)
        task1.process(user=user, action=action, rule=rule)
        task1.make_done.called |should| be(False)
        task1.actions |should| have(1).items
        task1.status |should| equal_to(ShareTaskRule.STATUS.inprogress)

        task2, user, action, rule = ShareTask.factory(user=user,
                                                      version=same_version,
                                                      ip_address=ip_address)

        task2.id |should| equal_to(task1.id)

        (task2.process, user, action, rule) |should| throw(TaskConditionDoesNotMeet)
        task2.actions |should| have(1).items
