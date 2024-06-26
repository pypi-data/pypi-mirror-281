from importlib import metadata

from nautobot.apps import NautobotAppConfig

__version__ = metadata.version(__name__)


class NautobotUuidLookupConfig(NautobotAppConfig):
    """Plugin configuration for the nautobot_uuid_lookup plugin."""

    name = "nautobot_uuid_lookup"
    verbose_name = "Nautobot UUID Lookup"
    base_url = "uuid"
    min_version = "1.5.2"
    max_version = "2.9999"
    description = (
        "Adds a generic URL that redirects all UUIDs to their appropriate object page"
    )
    author = "Gesellschaft für wissenschaftliche Datenverarbeitung mbH Göttingen"
    author_email = "netzadmin@gwdg.de"
    version = __version__


config = NautobotUuidLookupConfig
