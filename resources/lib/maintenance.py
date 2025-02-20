# resources/lib/maintenance.py

import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs # For Kodi 19+ compatibility
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
    Called at Kodi startup (via service.py).
    If auto_maintenance is True, we show a progress bar and clear cache + remove thumbnails.
    """
    if ADDON.getSettingBool("auto_maintenance"):
        run_maintenance_with_progress()

def run_maintenance_with_progress():
    """
    Clears cache and removes thumbnails while showing a background progress bar.
    Once done, displays a 'Maintenance Completed' message.
    """
    dialog = xbmcgui.DialogProgressBG()
    dialog.create("Auto Maintenance", "Starting maintenance...")

    # We'll do two major steps: Clear Cache, Remove Thumbs(disabled for now).
    # Let's keep track of total steps to show approximate progress.
    total_steps = 1 # We're only clearing cache, so total steps is 1. Update to 2 when implementing thumbs.
    current_step = 0

    # 1) Clear cache
    dialog.update(int((current_step / total_steps) * 100), "Clearing Cache...")
    clear_cache(ask_confirmation=False)
    current_step += 1

    '''# 2) Remove thumbnails
    dialog.update(int((current_step / total_steps) * 100), "Removing Thumbnails...")
    remove_thumbs(ask_confirmation=False) # Commented out because we're not implementing remove_thumbs
    current_step += 1'''

    # Final update to 100%
    dialog.update(100, "Maintenance Completed")
    # Keep the dialog visible for ~4 seconds
    time.sleep(4)
    dialog.close()

    # Optionally show a final dialog box
    xbmcgui.Dialog().notification("Maintenance Completed", "Cache has been cleared.", xbmcgui.NOTIFICATION_INFO, 6000) # change text when implementing remove_thumbs

def clear_cache(ask_confirmation=True):
    dialog = xbmcgui.Dialog()
    if ask_confirmation:
        confirm = dialog.yesno("Clear Cache", "Remove temporary files now?")
        if not confirm:
            dialog.notification("Cache Not Cleared", "Operation cancelled.", xbmcgui.NOTIFICATION_INFO, 3000)
            return

    # Use xbmcvfs.translatePath for Kodi 19+
    temp_path = xbmcvfs.translatePath("special://temp/")
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

'''def remove_thumbs(ask_confirmation=True):
    dialog = xbmcgui.Dialog()
    if ask_confirmation:
        confirm = dialog.yesno("Remove Thumbnails", "This will remove all thumbnails. Continue?")
        if not confirm:
            dialog.notification("Thumbnails Not Removed", "Operation cancelled.", xbmcgui.NOTIFICATION_INFO, 3000)
            return

    thumbs_path = xbmcvfs.translatePath("special://profile/Thumbnails/")
    if os.path.exists(thumbs_path):
        try:
            shutil.rmtree(thumbs_path, ignore_errors=True)
            if ask_confirmation:
                dialog.ok("Thumbnails Removed", "Restart Kodi to regenerate thumbs.")
        except Exception as e:
            dialog.ok("Error Removing Thumbnails", str(e))
    else:
        if ask_confirmation:
            dialog.ok("No Thumbnails Folder", "Nothing to remove.")'''
