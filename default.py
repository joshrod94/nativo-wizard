# default.py

import sys
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmc

# Import your modules (adjust paths as necessary):
from resources.lib.backup_restore import backup, restore
from resources.lib.maintenance import (
    open_maintenance_menu,
    handle_maintenance_action,
    auto_maintenance_if_enabled
)

ADDON = xbmcaddon.Addon(id='plugin.program.nativowizard')

def run_service_mode():
    """
    Called on Kodi startup (service mode).
    No plugin handle here, so we can't display menus.
    Only run auto-maintenance or background tasks.
    """
    auto_maintenance_if_enabled()

def plugin_main():
    """
    Called when the user opens this add-on via the Kodi UI ("Programs" section).
    In plugin mode, sys.argv has at least 2 elements (the script URL and the handle).
    We can parse parameters, then decide which menu or action to show.
    """
    params = parse_parameters()
    run_action(params)

def main_menu():
    """
    Show the main wizard menu items in plugin mode only.
    If there's no valid plugin handle, we skip adding menu items 
    to avoid the 'list index out of range' error.
    """
    if len(sys.argv) < 2:
        # Not in plugin mode or no handle available
        xbmc.log("main_menu called without a valid plugin handle. Skipping menu generation.", level=xbmc.LOGWARNING)
        return

    add_menu_item("Install Build", "install_build")
    add_menu_item("Backup Kodi", "backup")
    add_menu_item("Restore Kodi", "restore")
    add_menu_item("Maintenance", "maintenance")

    # Let Kodi know we're done adding items
    handle = int(sys.argv[1])
    xbmcplugin.endOfDirectory(handle)

def add_menu_item(label, action):
    """
    Helper to create a clickable item in the Kodi interface (plugin mode).
    """
    # sys.argv[0] is the base plugin URL. sys.argv[1] is the handle.
    url = f"{sys.argv[0]}?action={action}"
    list_item = xbmcgui.ListItem(label=label)

    # Only do this if we actually have a handle
    if len(sys.argv) > 1:
        handle = int(sys.argv[1])
        xbmcplugin.addDirectoryItem(handle, url, list_item, isFolder=False)
    else:
        xbmc.log("add_menu_item called without a valid handle.", level=xbmc.LOGWARNING)

def install_build():
    """
    Placeholder for your build-installation logic.
    """
    xbmcgui.Dialog().ok(
        "Install Build",
        "Build installation placeholder.\nImplement your download + extract logic here."
    )

def run_action(params):
    """
    Determine which action to perform based on query parameters.
    If there's no recognized action, display the main menu.
    """
    action = params.get('action', '')
    if action == 'install_build':
        install_build()
    elif action == 'backup':
        backup()
    elif action == 'restore':
        restore()
    elif action == 'maintenance':
        open_maintenance_menu()  # Displays the sub-menu for enabling/disabling auto, clearing cache, etc.
    elif action in ['enable_auto', 'disable_auto', 'clear_cache', 'remove_thumbs']:
        handle_maintenance_action(action)
    else:
        # No specific action => show the main wizard menu
        main_menu()

def parse_parameters():
    """
    Parse the plugin query string, e.g. plugin://.../?action=foo
    Returns a dict like {'action': 'foo'}.
    """
    import urllib.parse
    if len(sys.argv) > 2 and sys.argv[2].startswith('?'):
        param_string = sys.argv[2][1:]  # remove '?'
        return dict(urllib.parse.parse_qsl(param_string))
    return {}

if __name__ == '__main__':
    # 1. Always run service mode tasks first (e.g., auto-maintenance).
    run_service_mode()

    # 2. Check if we are in plugin mode (i.e., sys.argv has a handle).
    #    Typically, sys.argv[1] is the handle if the user actually clicked the add-on.
    if len(sys.argv) > 1:
        # We have a plugin handle, so proceed to the plugin main logic.
        plugin_main()
    else:
        # Kodi started us as a service, no handle. 
        # We do nothing else here to avoid "list index out of range."
        pass
