# -*- coding: utf-8 -*-

"""Modoboa rspamd forms."""

import collections

from django import forms
from django.utils.translation import ugettext_lazy as _

from modoboa.lib import form_utils
from modoboa.parameters import forms as param_forms

RSPAMD_PARAMETERS_STRUCT = collections.OrderedDict([
    ("dkim_settings_sep", {
        "label": _("DKIM signing settings"),
        "params": collections.OrderedDict([
            ("path_map_path", {
                "label": _("Path map path"),
                "help_text": _(
                    "Absolute path of the file which contains "
                    "paths to DKIM private keys.")
            }),
            ("selector_map_path", {
                "label": _("Selector map path"),
                "help_text": _(
                    "Absolute path of the file which contains "
                    "names of DKIM selectors.")
            })
        ])
    })
])


class ParametersForm(param_forms.AdminParametersForm):
    """Extension settings."""

    app = "modoboa_rspamd"

    dkim_settings_sep = form_utils.SeparatorField(
        label=_("DKIM signing settings"))

    path_map_path = forms.CharField(
        label=_("Path map path"),
        initial="",
        help_text=_(
            "Absolute path of the file which contains paths to DKIM "
            "private keys."
        ),
        required=False
    )
    selector_map_path = forms.CharField(
        label=_("Selector map path"),
        initial="",
        help_text=_(
            "Absolute path of the file which contains names of "
            "DKIM selectors."
        ),
        required=False
    )
