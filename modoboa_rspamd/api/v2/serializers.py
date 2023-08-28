
import os

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from modoboa_rspamd import handlers


def validate_file_path(value):
    if value:
        if os.path.isdir(value):
            raise serializers.ValidationError(
                _("Path provided is a directory")
                )
        condition = (os.path.exists(value) and os.access(value))\
                    or\
                    (not os.path.exists(value) and os.access(os.path.dirname(value),
                                                             os.W_OK))
        if not condition:
            raise serializers.ValidationError(
                _("File or directory is not writable")
                )


class RspamdSettingsSerializer(serializers.Serializer):
    """A serializer for global parameters."""

    # dkim_settings_sep
    key_path_map_path = serializers.CharField(default="/var/lib/dkim/keys.path.map",
                                          allow_blank=True)
    selector_map_path = serializers.CharField(default="/var/lib/dkim/selectors.path.map",
                                              allow_blank=True)

    def validate_key_path_map_path(self, value):
        validate_file_path(value)
        return value

    def validate_selector_map_path(self, value):
        validate_file_path(value)
        return value
