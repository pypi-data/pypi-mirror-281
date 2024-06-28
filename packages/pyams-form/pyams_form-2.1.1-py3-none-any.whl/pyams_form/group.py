#
# Copyright (c) 2015-2020 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_form.group module

This module handles groups of widgets within forms.
"""

from zope.interface import Interface, implementer

from pyams_form.events import FormUpdatedEvent
from pyams_form.form import BaseForm, get_form_weight
from pyams_form.interfaces.form import IFormContent, IGroup, IGroupForm, IGroupManager
from pyams_form.interfaces.widget import IWidgets
from pyams_layer.interfaces import IFormLayer
from pyams_utils.adapter import adapter_config

__docformat__ = 'restructuredtext'


@implementer(IGroupManager)
class GroupManager:  # pylint: disable=no-member
    """Base groups manager mixin class"""

    groups = ()

    def get_groups(self):
        """Internal groups iterator getter"""
        registry = self.request.registry
        yield from sorted((adapter for name, adapter in
                           registry.getAdapters((self.context, self.request, self), IGroup)),
                          key=get_form_weight)

    def update(self):
        """See interfaces.IForm"""
        self.update_widgets()
        groups = []
        # static groups list
        for group_class in self.groups:
            # only instantiate the group_class if it hasn't already
            # been instantiated
            if IGroup.providedBy(group_class):
                group = group_class
            else:
                group = group_class(self.context, self.request, self)
            groups.append(group)
        # groups can also be added dynamically using adapters
        for group in self.get_groups():
            groups.append(group)
        # update all groups
        [group.update() for group in groups]  # pylint: disable=expression-not-assigned
        self.groups = tuple(groups)
        [subform.update() for subform in self.subforms]  # pylint: disable=expression-not-assigned
        [tabform.update() for tabform in self.tabforms]  # pylint: disable=expression-not-assigned
        self.request.registry.notify(FormUpdatedEvent(self))

    def extract_data(self, set_errors=True, notify=True):
        """See interfaces.IForm"""
        data, errors = super().extract_data(set_errors=set_errors, notify=notify)
        for group in self.groups:
            group_data, group_errors = group.extract_data(set_errors=set_errors, notify=notify)
            data.update(group_data)
            if group_errors:
                if errors:
                    errors += group_errors
                else:
                    errors = group_errors
        return data, errors


@implementer(IGroup)
class Group(GroupManager, BaseForm):
    """Group of field widgets within form"""

    def __init__(self, context, request, parent_form):  # pylint: disable=super-init-not-called
        self.context = context
        self.request = request
        self.parent_form = self.__parent__ = parent_form

    def update_widgets(self, prefix=None, use_form_mode=True):
        """See interfaces.IForm"""
        registry = self.request.registry
        self.widgets = registry.getMultiAdapter((self, self.request, self.get_content()),
                                                IWidgets)
        self.widgets.mode = self.mode
        if use_form_mode:
            for attr_name in ('ignore_request', 'ignore_context', 'ignore_readonly'):
                value = getattr(self.parent_form.widgets, attr_name)
                setattr(self.widgets, attr_name, value)
        if prefix is not None:
            self.widgets.prefix = prefix
        self.widgets.update()


@adapter_config(required=(Interface, IFormLayer, IGroup),
                provides=IFormContent)
def get_group_content(context, request, group):  # pylint: disable=unused-argument
    """Group content getter"""
    return group.parent_form.get_content()


@implementer(IGroupForm)
class GroupForm(GroupManager):
    """A mix-in class for add and edit forms to support groups."""

    def update(self):
        """See interfaces.IForm"""
        GroupManager.update(self)
        self.update_actions()  # pylint: disable=no-member
        self.actions.execute()  # pylint: disable=no-member
