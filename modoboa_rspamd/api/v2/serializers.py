"""Modoboa rspamd serializer for api v2."""

import os

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


def validate_file_path(value):
    if value:
        if not os.path.isabs(value):
            # We only check if it is absolute,
            # since it shouldn't be accessible to modoboa user.
            # Only to _rspamd
            raise serializers.ValidationError(
                _("Path provided is not absolute.")
                )

class RspamdSettingsSerializer(serializers.Serializer):
    """A serializer for global parameters."""

    # dkim_settings_sep
    key_map_path = serializers.CharField(default="/var/lib/dkim/keys.path.map",
                                          allow_blank=True)
    selector_map_path = serializers.CharField(default="/var/lib/dkim/selectors.path.map",
                                              allow_blank=True)

    def validate_key_map_path(self, value):
        validate_file_path(value)
        return value

    def validate_selector_map_path(self, value):
        validate_file_path(value)
        return value
