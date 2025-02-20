# default.py
import sys
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmc

# Import your custom modules:
from resources.lib.backup_restore import backup, restore
from resources.lib.maintenance import (
    open_maintenance_menu,
    handle_maintenance_action,
    auto_maintenance_if_enabled
)

ADDON = xbmcaddon.Addon(id='plugin.program.nativowizard')

def run_service_mode():
    """
    This will be called immediately when Kodi starts the add-on as a background "service."
    If the user has enabled auto-maintenance, it will automatically clear cache and remove thumbnails.
    """
    auto_maintenance_if_enabled()

def main_menu():
    """
    This displays the main wizard menu items if the user manually opens the add-on.
    Modify as needed to add more items (e.g., for your build install, advanced features, etc.).
    """
    add_menu_item("Install Build", "install_build")
    add_menu_item("Backup Kodi", "backup")
    add_menu_item("Restore Kodi", "restore")
    add_menu_item("Maintenance", "maintenance")
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def add_menu_item(label, action):
    """
    Helper function to create a clickable menu item in Kodi's interface.
    Each item includes a query parameter (?action=XYZ) so we know what the user clicked.
    """
    url = f"{sys.argv[0]}?action={action}"
    list_item = xbmcgui.ListItem(label=label)
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=list_item, isFolder=False)

def install_build():
    """
    Placeholder for your build installation logic.
    In a real wizard, you'd download and extract a ZIP to the Kodi profile folders.
    """
    xbmcgui.Dialog().ok("Install Build", "Build installation placeholder.\nImplement your download + extract logic here.")

def run_action(params):
    """
    Decides what to do based on the 'action' parameter from the plugin URL.
    If there's no action, show the main menu.
    """
    action = params.get('action', '')
    if action == 'install_build':
        install_build()
    elif action == 'backup':
        backup()
    elif action == 'restore':
        restore()
    elif action == 'maintenance':
        # Show the maintenance submenu with four choices:
        # 1) Enable Auto Maintenance
        # 2) Disable Auto Maintenance
        # 3) Manually Clear Cache
        # 4) Manually Remove Thumbnails
        open_maintenance_menu()
    elif action in ['enable_auto', 'disable_auto', 'clear_cache', 'remove_thumbs']:
        # These are handled by the maintenance module
        handle_maintenance_action(action)
    else:
        # If no action, show the main wizard menu
        main_menu()

def parse_parameters():
    """
    Extract query parameters from the plugin call, e.g. ?action=backup
    This function turns that into a Python dictionary: {'action': 'backup'}.
    """
    import urllib.parse
    if len(sys.argv) > 2:
        params_str = sys.argv[2]
        if params_str.startswith('?'):
            params_str = params_str[1:]
        return dict(urllib.parse.parse_qsl(params_str))
    return {}

if __name__ == '__main__':
    # 1. Run the service mode logic (auto-maintenance if enabled).
    run_service_mode()

    # 2. Check if the user actually opened the add-on via the GUI (plugin mode).
    #    If they did, sys.argv might have action parameters to parse.
    params = parse_parameters()
    run_action(params)
