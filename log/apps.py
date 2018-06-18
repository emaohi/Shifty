from __future__ import unicode_literals

import logging
from django.apps import AppConfig
from health_check.plugins import plugin_dir

from log.backends import GmailCheckBackend

logger = logging.getLogger(__name__)


class LogConfig(AppConfig):
    name = 'log'

    def ready(self):
        from .backends import CeleryHealthCheckBackend, ProfanityCheckBackend, GoogleApiCheckBackend,\
            LogoFinderCheckBackend
        plugin_dir.register(CeleryHealthCheckBackend)
        plugin_dir.register(ProfanityCheckBackend)
        plugin_dir.register(GoogleApiCheckBackend)
        plugin_dir.register(LogoFinderCheckBackend),
        plugin_dir.register(GmailCheckBackend),
