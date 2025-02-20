# service.py

import xbmcaddon
import xbmc

from resources.lib.maintenance import auto_maintenance_if_enabled

ADDON = xbmcaddon.Addon(id='plugin.program.nativowizard')

def run_service():
    """
    This gets called automatically by Kodi when it starts up,
    because we declared <extension point="xbmc.service" library="service.py" /> in addon.xml.
    """
    # If the user has auto-maintenance enabled, do it now
    auto_maintenance_if_enabled()

if __name__ == "__main__":
    run_service()
