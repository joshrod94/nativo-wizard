# resources/lib/maintenance.py

import xbmc
import xbmcaddon
import xbmcgui
import os
import shutil

# Match your add-on ID in addon.xml
ADDON = xbmcaddon.Addon(id='plugin.program.nativowizard')

def enable_auto_maintenance():
    """
    Turn on auto-maintenance by setting the 'auto_maintenance' bool setting to True.
    """
    ADDON.setSettingBool("auto_maintenance", True)
    xbmcgui.Dialog().ok(
        "Auto Maintenance Enabled",
        "Kodi will run maintenance tasks on startup."
    )

def disable_auto_maintenance():
    """
    Turn off auto-maintenance by setting the 'auto_maintenance' bool setting to False.
    """
    ADDON.setSettingBool("auto_maintenance", False)
    xbmcgui.Dialog().ok(
        "Auto Maintenance Disabled",
        "Kodi will not run maintenance tasks on startup."
    )

def auto_maintenance_if_enabled():
    """
    Check if the user enabled auto_maintenance.
    If True, automatically clear cache and remove thumbnails on Kodi startup.
    """
    if ADDON.getSettingBool("auto_maintenance"):
        clear_cache(ask_confirmation=False)  # skip confirmation if auto-run
        remove_thumbs(ask_confirmation=False)  # skip confirmation if auto-run

def clear_cache(ask_confirmation=True):
    """
    Manually clear Kodi's cache folder at special://temp/.
    If ask_confirmation=False, it does so without prompting the user.
    """
    dialog = xbmcgui.Dialog()
    if ask_confirmation:
        confirm = dialog.yesno("Clear Cache", "Remove temporary files now?")
        if not confirm:
            dialog.notification("Cache Not Cleared", "Operation cancelled.", xbmcgui.NOTIFICATION_INFO, 3000)
            return

    temp_path = xbmc.translatePath("special://temp/")
    if os.path.exists(temp_path):
        try:
            for item in os.listdir(temp_path):
                item_path = os.path.join(temp_path, item)
                if os.path.isfile(item_path):
                    os.remove(item_path)
                else:
                    shutil.rmtree(item_path, ignore_errors=True)
            if ask_confirmation:
                dialog.ok("Cache Cleared", "Temporary files removed.")
        except Exception as e:
            dialog.ok("Error Clearing Cache", str(e))
    else:
        if ask_confirmation:
            dialog.ok("Cache Not Found", "No temp folder present.")

def remove_thumbs(ask_confirmation=True):
    """
    Manually remove the Thumbnails folder at special://profile/Thumbnails/.
    If ask_confirmation=False, it does so without prompting the user.
    """
    dialog = xbmcgui.Dialog()
    if ask_confirmation:
        confirm = dialog.yesno("Remove Thumbnails", "This will remove all thumbnails. Continue?")
        if not confirm:
            dialog.notification("Thumbnails Not Removed", "Operation cancelled.", xbmcgui.NOTIFICATION_INFO, 3000)
            return

    thumbs_path = xbmc.translatePath("special://profile/Thumbnails/")
    if os.path.exists(thumbs_path):
        try:
            shutil.rmtree(thumbs_path, ignore_errors=True)
            if ask_confirmation:
                dialog.ok("Thumbnails Removed", "Restart Kodi to regenerate thumbs.")
        except Exception as e:
            dialog.ok("Error Removing Thumbnails", str(e))
    else:
        if ask_confirmation:
            dialog.ok("No Thumbnails Folder", "Nothing to remove.")
