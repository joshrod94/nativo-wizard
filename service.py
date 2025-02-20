# service.py

import xbmcaddon
import xbmc
from resources.lib.maintenance import auto_maintenance_if_enabled

ADDON = xbmcaddon.Addon(id='plugin.program.nativowizard')

def run_service():
    """
    This is called at Kodi startup (service mode).
    If auto-maintenance is enabled, it clears cache and thumbnails.
    """
    auto_maintenance_if_enabled()

if __name__ == "__main__":
    run_service()
