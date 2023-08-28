"""Management command to create DKIM keys."""

import os

from django.core.management.base import BaseCommand, CommandError

from modoboa.parameters import tools as param_tools

from .... import models


class ManageRSPAMDMap(BaseCommand):
    """Command class."""

    def load_files(self):
        config = dict(param_tools.get_global_parameters("modoboa_rspamd"))
        if not config["key_path_map_path"] or not config["selector_map_path"]:
            raise CommandError("path map path and/or selector map path "
                "not set in modoboa rspamd settings.")

        self.dkim_path_map = {}
        try:
            with open(config["key_path_map_path"], "r") as f:
                for line in f:
                    domain_name, path = line.split()
                    dkim_path_map[domain_name] = path.replace("\n","")
        except FileNotFoundError:
            pass
        self.selector_map = {}
        try:
            with open(config["selector_map_path"], "r") as f:
                for line in f:
                    domain_name, selector = line.split()
                    selector_map[domain_name] = path.replace("\n","")
        except FileNotFoundError:
            pass

    def manage_domain(self, domain_instance):
        domain_name = domain_instance.name
        selector_entry = self.selector_map.get(domain_name, None)
        dkim_path_entry = self.dkim_path_map.get(domain_name, None)
        if not domain_instance.enable_dkim:
            if selector_entry is not None:
                self.selector_map.pop(domain_name)
            if dkim_path_entry is not None:
                self.dkim_path_map.pop(domain_name)
            return

        # modify selector map
        condition = (selector_entry is None or
                     selector_entry=!domain_instance.dkim_key_selector)
        if condition:
            self.selector_map[domain_name] = domain_instance.dkim_key_selector
            self.modified_selector_file = True

        # modify dkim path map
        condition = (dkim_path_entry is None or
                     dkim_path_entry=!domain_instance.dkim_private_key_path)
        if condition:
            self.dkim_path_map[domain_name] = domain_instance.dkim_private_key_path
            self.modified_key_path_file = True


    def add_arguments(self, parser):
        """Add arguments to command."""
        parser.add_argument(
            "--domain", type=str, dest="domain", default="",
            help="Domain target for keys generation."
        )

    def handle(self, *args, **options):
        """Entry point."""
        self.modified_selector_file = False
        self.modified_key_path_file = False
        self.load_files()

        if options["domain"] != "":
            domain = models.Domain.objects.filter(name=options["domain"])
            if domain.exists():
                self.manage_domain(domain[0])
        else:
            qset = models.Domain.objects.all()
            for domain in qset:
                self.manage_domain(domain)
        config = dict(param_tools.get_global_parameters("modoboa_rspamd"))

        if self.modified_selector_file:
            with open(config["selector_map_path"], "w") as f:
                for domain_name, selector in self.selector_map.values():
                    f.write(f"{domain_name} {selector}")
        if self.modified_key_path_file:
            with open(config["key_path_map_path"], "w") as f:
                for domain_name, key_path in self.dkim_path_map.values():
                    f.write(f"{domain_name} {key_path}")