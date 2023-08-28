# -*- coding: utf-8 -*-

"""Modoboa rspamd handlers."""

from __future__ import unicode_literals

from django.dispatch import receiver
from django.db.models.signals import post_save

from modoboa.admin import models as admin_models
from modoboa.admin import signals as admin_signals
from modoboa.parameters import tools as param_tools


@receiver(signals.post_save, sender=admin_models.Domain)
def update_rspamd_dkim_maps(sender, instance, created, **kwargs):
    """Update config maps."""
    # Modify or create
    condition = instance.enable_dkim and \
        (created or
         instance._loaded_values["dkim_private_key_path"] != instance.dkim_private_key_path or
         instance._loaded_values["dkim_key_selector"] != instance.dkim_key_selector
         )
    if condition:
        queue = django_rq.get_queue('rspamd')
        queue.enqueue(call_command,
                      "manage_rspamd_maps",
                      f"--domain={instance.name}")

