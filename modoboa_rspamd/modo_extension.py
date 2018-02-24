# -*- coding: utf-8 -*-

"""Rspamd plugin for Modoboa."""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy

from modoboa.core.extensions import ModoExtension, exts_pool
from modoboa.parameters import tools as param_tools

from . import __version__, forms


class Rspamd(ModoExtension):
    """Rspamd extension class."""

    name = "modoboa_rspamd"
    label = ugettext_lazy("Rspamd frontend")
    description = ugettext_lazy("Rspamd management frontend")
    version = __version__

    def load(self):
        param_tools.registry.add("global", forms.ParametersForm, "Rspamd")


exts_pool.register_extension(Rspamd)
