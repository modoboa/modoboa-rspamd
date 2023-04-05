# -*- coding: utf-8 -*-

"""Modoboa rspamd handlers."""

from __future__ import unicode_literals

from django.dispatch import receiver

from modoboa.admin import models as admin_models
from modoboa.admin import signals as admin_signals
from modoboa.parameters import tools as param_tools


@receiver(admin_signals.extra_dkim_management)
def update_rspamd_dkim_maps(sender, **kwargs):
    """Update config maps."""
    config = dict(param_tools.get_global_parameters("modoboa_rspamd"))
    if not config["path_map_path"] or not config["selector_map_path"]:
        return
    qset = admin_models.Domain.objects.filter(enable_dkim=True)

    dkim_path_map = {}
    try:
        with open(config["path_map_path"], "r") as f:
            for line in f:
                domain_name, path = line.split()
                dkim_path_map[domain_name] = path.replace("\n","")
    except FileNotFoundError:
        pass
    selector_map = {}
    try:
        with open(config["selector_map_path"], "r") as f:
            for line in f:
                domain_name, selector = line.split()
                selector_map[domain_name] = path.replace("\n","")
    except FileNotFoundError:
        pass

    db_dkim_path_map = {}
    db_selector_map = {}
    for domain in qset:
        db_dkim_path_map[domain.name] = domain.dkim_private_key_path
        db_selector_map[domain.name] = domain.dkim_key_selector

    if db_dkim_path_map != dkim_path_map:
        with open(config["path_map_path"], "w") as f:
            for domain_name, path in db_dkim_path_map.items():
                f.write("{} {}\n".format(domain_name, path))
    if db_selector_map != selector_map:
        with open(config["selector_map_path"],"w") as f:
            for domain_name, selector in db_selector_map.items():
                f.write("{} {}\n".format(domain_name, selector))
