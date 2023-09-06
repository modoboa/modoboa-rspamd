# -*- coding: utf-8 -*-

"""Modoboa rspamd forms."""

import collections

from django import forms
from django.utils.translation import gettext_lazy as _

from modoboa.lib import form_utils
from modoboa.parameters import forms as param_forms

RSPAMD_PARAMETERS_STRUCT = collections.OrderedDict([
    ("dkim_settings_sep", {
        "label": _("DKIM signing settings"),
        "params": collections.OrderedDict([
            ("key_map_path", {
                "label": _("Key map path"),
                "help_text": _(
                    "Absolute path of the file which contains "
                    "paths to DKIM private keys. "
                    "Must be readable by _rspamd group or user.")
            }),
            ("selector_map_path", {
                "label": _("Selector map path"),
                "help_text": _(
                    "Absolute path of the file which contains "
                    "names of DKIM selectors. "
                    "Must be readable by _rspamd group or user.")
            })
        ])
    })
])


class ParametersForm(param_forms.AdminParametersForm):
    """Extension settings."""

    app = "modoboa_rspamd"

    dkim_settings_sep = form_utils.SeparatorField(
        label=_("DKIM signing settings"))

    key_map_path = forms.CharField(
        label=_("Key map path"),
        initial="",
        help_text=_(
            "Absolute path of the file which contains paths to DKIM "
            "private keys. "
            "Must be readable by _rspamd group or user."
        ),
        required=False
    )
    selector_map_path = forms.CharField(
        label=_("Selector map path"),
        initial="",
        help_text=_(
            "Absolute path of the file which contains names of "
            "DKIM selectors. "
            "Must be readable by _rspamd group or user."
        ),
        required=False
    )
