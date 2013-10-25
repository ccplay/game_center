# -*- coding: utf-8 -*-
from behave import *
from fts.features import support
from fts.tests import helpers
from fts.tests.helpers import ApiDSL
from should_dsl import should


@then('I should see the category {is_in:inb} result tree')
def step_should_see_the_category_in_reuslt(context, is_in):
    the_category = context.world.get('the_category')
    ApiDSL.Then_i_should_see_the_category_in_category_tree(context,
                                                           the_category,
                                                           is_in)

@when('I visit the category detail page')
def step_visit_the_category_detail_page(context):
    the_category = context.world.get('the_category')
    ApiDSL.When_i_access_category_detail(context, the_category)

@given('the category "{name}" as root just created')
def step_create_category_as_root(context, name):
    category=helpers.create_category(name=name)
    context.world.update(dict(the_category=category))

@when('I visit category page')
def step_visit_category_page(context):
    ApiDSL.When_i_access_category_list(context)

@given('I hide the category')
def step_hide_category(context):
    the_category = context.world.get('the_category')
    the_category.is_hidden = True
    the_category.save()

@then('I should see the category detail I just hidden')
def step_should_see_the_hidden_category_detail(context):
    the_category = context.world.get('the_category')
    the_category.is_hidden |should| be(True)
    expect_category = context.world.get('content')
    expect_category.get('slug') |should| equal_to(the_category.slug)
