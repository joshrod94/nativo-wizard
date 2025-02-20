# default.py
import sys
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmc

# If you have backup/restore and maintenance modules, import them here:
from resources.lib.backup_restore import backup, restore
from resources.lib.maintenance import (
    open_maintenance_menu,
    handle_maintenance_action
)

# Reference to your add-on's ID (must match the <addon id="..."> in addon.xml)
ADDON = xbmcaddon.Addon(id='plugin.program.nativowizard')

def parse_parameters():
    """
    Extracts query parameters from sys.argv[2], e.g. plugin://.../?action=backup
    Returns a dict: {'action': 'backup'} 
    or an empty dict if no parameters are provided.
    """
    import urllib.parse
    if len(sys.argv) > 2 and sys.argv[2].startswith('?'):
        query_str = sys.argv[2][1:]  # Remove the '?' at the start
        return dict(urllib.parse.parse_qsl(query_str))
    return {}

def main_menu():
    """
    Builds the main wizard menu. 
    If Kodi called us in plugin mode, sys.argv[1] is the 'handle' needed for addDirectoryItem().
    """
    if len(sys.argv) < 2:
        # No handle => not in plugin mode (or there's an error).
        xbmc.log("No plugin handle found, cannot build menu.", level=xbmc.LOGWARNING)
        return

    # Add items to the Kodi directory
    add_menu_item("Install Build", "install_build")
    add_menu_item("Backup Kodi", "backup")
    add_menu_item("Restore Kodi", "restore")
    add_menu_item("Maintenance", "maintenance")

    # Tell Kodi we're done adding items to this directory
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def add_menu_item(label, action):
    """
    Helper to add a clickable item to Kodi's UI, each linking to ?action=<whatever>.
    """
    if len(sys.argv) > 1:
        handle = int(sys.argv[1])
        base_url = sys.argv[0]
        url = f"{base_url}?action={action}"
        list_item = xbmcgui.ListItem(label=label)
        xbmcplugin.addDirectoryItem(handle, url, list_item, isFolder=False)
    else:
        xbmc.log("Cannot add menu item; no valid plugin handle in sys.argv[1].", level=xbmc.LOGWARNING)

def install_build():
    """
    Placeholder for your build-installation logic:
      - Download a ZIP from your server
      - Extract it to Kodi's userdata/addons folders
      - Prompt user to restart Kodi
    """
    xbmcgui.Dialog().ok("Install Build", "Placeholder: implement download & extraction logic here.")

def run_action(params):
    """
    Looks at the 'action' param. If it matches known actions, calls the relevant function.
    If no action, shows the main menu.
    """
    action = params.get('action', '')
    if action == 'install_build':
        install_build()
    elif action == 'backup':
        backup()  # Calls the backup function from backup_restore.py
    elif action == 'restore':
        restore() # Calls the restore function from backup_restore.py
    elif action == 'maintenance':
        open_maintenance_menu()  # A function in maintenance.py
    elif action in ['enable_auto','disable_auto','clear_cache','remove_thumbs']:
        # Sub-actions inside your maintenance module
        handle_maintenance_action(action)
    else:
        # No recognized action => show the main wizard menu
        main_menu()

if __name__ == "__main__":
    # 1. Parse query params, e.g., ?action=backup => {'action': 'backup'}
    params = parse_parameters()

    # 2. Run the appropriate function or show the main menu if no action is specified
    run_action(params)
