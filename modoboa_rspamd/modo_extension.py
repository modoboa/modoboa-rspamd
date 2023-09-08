# -*- coding: utf-8 -*-

"""Rspamd plugin for Modoboa."""

from __future__ import unicode_literals

from django.utils.translation import gettext_lazy

from modoboa.core.extensions import ModoExtension, exts_pool
from modoboa.parameters import tools as param_tools

from . import __version__


class Rspamd(ModoExtension):
    """Rspamd extension class."""

    name = "modoboa_rspamd"
    label = gettext_lazy("Rspamd frontend")
    description = gettext_lazy("Rspamd management frontend")
    version = __version__


exts_pool.register_extension(Rspamd)
