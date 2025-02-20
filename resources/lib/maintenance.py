# maintenance.py
import xbmcgui
import xbmcaddon
import xbmc
import os
import shutil

ADDON = xbmcaddon.Addon(id='plugin.program.nativowizard')

def clear_cache():
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Clear Cache", "Remove temporary files?"):
        temp_path = xbmc.translatePath("special://temp/")
        if os.path.exists(temp_path):
            for item in os.listdir(temp_path):
                item_path = os.path.join(temp_path, item)
                try:
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    else:
                        shutil.rmtree(item_path, ignore_errors=True)
                except:
                    pass
            dialog.ok("Cache Cleared", "Temporary files removed.")
        else:
            dialog.ok("Cache Not Found", "No temp folder.")

def remove_thumbs():
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Remove Thumbnails", "This will remove all thumbnails. Continue?"):
        thumbs_path = xbmc.translatePath("special://profile/Thumbnails/")
        if os.path.exists(thumbs_path):
            shutil.rmtree(thumbs_path, ignore_errors=True)
            dialog.ok("Thumbnails Removed", "Restart Kodi to regenerate thumbs.")
        else:
            dialog.ok("No Thumbnails Folder", "Nothing to remove.")

def enable_auto_maintenance():
    ADDON.setSettingBool("auto_maintenance", True)
    xbmcgui.Dialog().ok("Auto Maintenance Enabled", "Maintenance will run at Kodi startup.")

def disable_auto_maintenance():
    ADDON.setSettingBool("auto_maintenance", False)
    xbmcgui.Dialog().ok("Auto Maintenance Disabled", "No automatic cleanup on startup.")
