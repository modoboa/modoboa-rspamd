# -*- coding: utf-8 -*-

"""Modoboa rspamd forms."""

from django import forms
from django.utils.translation import ugettext_lazy

from modoboa.lib import form_utils
from modoboa.parameters import forms as param_forms


class ParametersForm(param_forms.AdminParametersForm):
    """Extension settings."""

    app = "modoboa_rspamd"

    dkim_settings_sep = form_utils.SeparatorField(
        label=ugettext_lazy("DKIM signing settings"))

    path_map_path = forms.CharField(
        label=ugettext_lazy("Path map path"),
        initial="",
        help_text=ugettext_lazy(
            "Absolute path of the file which contains paths to DKIM "
            "private keys."
        ),
        required=False
    )
    selector_map_path = forms.CharField(
        label=ugettext_lazy("Selector map path"),
        initial="",
        help_text=ugettext_lazy(
            "Absolute path of the file which contains names of "
            "DKIM selectors."
        ),
        required=False
    )
