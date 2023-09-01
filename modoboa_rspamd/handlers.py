# -*- coding: utf-8 -*-

"""Modoboa rspamd handlers."""

from django.core.management import call_command
from django.dispatch import receiver
from django.db.models.signals import post_save

import django_rq

from modoboa.admin import models as admin_models

@receiver(post_save, sender=admin_models.Domain)
def update_rspamd_dkim_maps(sender, instance, created, **kwargs):
    """Update config maps."""
    # Modify or create
    condition = (instance._loaded_values["dkim_private_key_path"] != instance.dkim_private_key_path or
         instance._loaded_values["dkim_key_selector"] != instance.dkim_key_selector
         )
    if condition:
        queue = django_rq.get_queue('dkim')
        queue.enqueue(call_command,
                      "manage_rspamd_maps",
                      f"--domain={instance.name}")

