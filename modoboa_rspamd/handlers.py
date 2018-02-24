# -*- coding: utf-8 -*-

"""Modoboa rspamd handlers."""

from __future__ import unicode_literals

from django.dispatch import receiver

from modoboa.admin import models as admin_models
from modoboa.admin import signals as admin_signals
from modoboa.parameters import tools as param_tools


@receiver(admin_signals.new_dkim_keys)
def update_rspamd_dkim_maps(sender, domains, **kwargs):
    """Update config maps."""
    qset = admin_models.Domain.objects.filter(enable_dkim=True)
    config = dict(param_tools.get_global_parameters())
    if not config["path_map_path"] or not config["selector_map_path"]:
        return
    dkim_path_map = open(config["path_map_path"], "w")
    dkim_selector_map = open(config["selector_map_path"], "w")
    for domain in qset:
        dkim_path_map.write(
            "{} {}\n".format(domain.name, domain.dkim_private_key_path))
        dkim_selector_map.write(
            "{} {}\n".format(domain.name, domain.dkim_key_selector))
    dkim_path_map.close()
    dkim_selector_map.close()
