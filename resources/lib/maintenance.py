# resources/lib/maintenance.py
import sys
import os
import shutil
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmc

ADDON = xbmcaddon.Addon(id='plugin.program.mywizard')

def open_maintenance_menu():
    """
    Show a submenu for maintenance actions:
      1. Enable Auto Maintenance
      2. Disable Auto Maintenance
      3. Manually Clear Cache
      4. Manually Remove Thumbnails
    """
    add_menu_item("Enable Auto Maintenance on Startup", "enable_auto")
    add_menu_item("Disable Auto Maintenance on Startup", "disable_auto")
    add_menu_item("Manually Clear Cache", "clear_cache")
    add_menu_item("Manually Remove Thumbnails", "remove_thumbs")
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def add_menu_item(label, action):
    """
    Helper that creates a clickable item in Kodi's list.
    `action` is passed as a query parameter so we know what user selected.
    """
    url = f"{sys.argv[0]}?action={action}"
    list_item = xbmcgui.ListItem(label=label)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, list_item, isFolder=False)

def handle_maintenance_action(action):
    """
    Called from default.py when the user clicks a maintenance menu item.
    """
    if action == 'enable_auto':
        ADDON.setSettingBool("auto_maintenance", True)
        xbmcgui.Dialog().ok(
            "Auto Maintenance Enabled", 
            "Kodi will clear cache and remove thumbnails on startup."
        )
    elif action == 'disable_auto':
        ADDON.setSettingBool("auto_maintenance", False)
        xbmcgui.Dialog().ok(
            "Auto Maintenance Disabled", 
            "Kodi will no longer run maintenance on startup."
        )
    elif action == 'clear_cache':
        clear_cache()
    elif action == 'remove_thumbs':
        remove_thumbs()

def auto_maintenance_if_enabled():
    """
    Called on Kodi startup (service mode).
    If auto maintenance is ON in settings, run the cleaning tasks automatically.
    """
    if ADDON.getSettingBool("auto_maintenance"):
        clear_cache()
        remove_thumbs()

def clear_cache():
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Clear Cache", "Do you want to clear temporary files now?"):
        temp_path = xbmc.translatePath("special://temp/")
        if os.path.exists(temp_path):
            try:
                for item in os.listdir(temp_path):
                    item_path = os.path.join(temp_path, item)
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    else:
                        shutil.rmtree(item_path, ignore_errors=True)
                dialog.ok("Cache Cleared", "Temporary files have been removed.")
            except Exception as e:
                dialog.ok("Error Clearing Cache", str(e))
        else:
            dialog.ok("No Cache Found", "No temp folder found. Nothing to remove.")
    else:
        dialog.notification("Cache Not Cleared", "Operation cancelled.", xbmcgui.NOTIFICATION_INFO, 3000)

def remove_thumbs():
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Remove Thumbnails", "This will remove your thumbnail cache. Continue?"):
        thumbs_path = xbmc.translatePath("special://profile/Thumbnails/")
        if os.path.exists(thumbs_path):
            try:
                shutil.rmtree(thumbs_path, ignore_errors=True)
                dialog.ok("Thumbnails Removed", "Please restart Kodi for changes to take effect.")
            except Exception as e:
                dialog.ok("Error Removing Thumbs", str(e))
        else:
            dialog.ok("No Thumbnails Folder", "No Thumbnails folder found.")
    else:
        dialog.notification("Thumbnails Not Removed", "Operation cancelled.", xbmcgui.NOTIFICATION_INFO, 3000)
