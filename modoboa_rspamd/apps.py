# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class ModoboaRspamdConfig(AppConfig):
    name = 'modoboa_rspamd'

    def ready(self):
        from . import handlers  # NOQA:F401
