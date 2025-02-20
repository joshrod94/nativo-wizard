# default.py
import sys
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmc

# Import your custom modules (adjust paths as needed):
from resources.lib.backup_restore import backup, restore
from resources.lib.maintenance import (
    open_maintenance_menu,
    handle_maintenance_action
)

# Reference to the current add-on
ADDON = xbmcaddon.Addon(id='plugin.program.nativowizard')

def main_menu():
    """
    Creates the top-level wizard menu:
      - Install Build
      - Backup Kodi
      - Restore Kodi
      - Maintenance
    We only build this menu if there's a valid plugin handle in sys.argv[1].
    """
    if len(sys.argv) < 2:
        xbmc.log("No plugin handle found, skipping menu generation.", level=xbmc.LOGWARNING)
        return

    add_menu_item("Install Build", "install_build")
    add_menu_item("Backup Kodi", "backup")
    add_menu_item("Restore Kodi", "restore")
    add_menu_item("Maintenance", "maintenance")

    # Signal to Kodi that we're done adding menu items
    handle = int(sys.argv[1])
    xbmcplugin.endOfDirectory(handle)

def add_menu_item(label, action):
    """
    Helper function to add a clickable item in Kodi's UI (in plugin mode).
    Each menu item includes a query parameter, e.g. ?action=install_build
    """
    if len(sys.argv) > 1:
        base_url = sys.argv[0]
        handle = int(sys.argv[1])
        url = f"{base_url}?action={action}"
        list_item = xbmcgui.ListItem(label=label)
        xbmcplugin.addDirectoryItem(handle, url, list_item, isFolder=False)
    else:
        xbmc.log("Cannot add menu item; no valid handle in sys.argv[1].", level=xbmc.LOGWARNING)

def install_build():
    """
    Placeholder for your build installation logic.
    You could download a ZIP and extract it to Kodi's profile folders.
    """
    xbmcgui.Dialog().ok(
        "Install Build",
        "This is a placeholder for build install logic.\nImplement your download + extract steps here."
    )

def parse_parameters():
    """
    Extracts plugin parameters from sys.argv[2], e.g. plugin://.../?action=xyz.
    Returns a dictionary like {'action': 'xyz'}.
    """
    import urllib.parse
    if len(sys.argv) > 2 and sys.argv[2].startswith('?'):
        query_str = sys.argv[2][1:]  # Remove the '?' prefix
        return dict(urllib.parse.parse_qsl(query_str))
    return {}

def run_action(params):
    """
    Looks at the 'action' query parameter and calls the appropriate function.
    If there's no recognized action, it shows the main menu.
    """
    action = params.get('action', '')
    if action == 'install_build':
        install_build()
    elif action == 'backup':
        backup()
    elif action == 'restore':
        restore()
    elif action == 'maintenance':
        open_maintenance_menu()
    elif action in ['enable_auto', 'disable_auto', 'clear_cache', 'remove_thumbs']:
        # Those sub-actions are handled in maintenance.py
        handle_maintenance_action(action)
    else:
        # No or unknown action => show the wizard's main menu
        main_menu()

if __name__ == "__main__":
    # Parse any plugin parameters (e.g. ?action=...)
    params = parse_parameters()
    # Perform the requested action or show the main menu
    run_action(params)
