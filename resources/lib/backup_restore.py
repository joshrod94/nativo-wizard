# resources/lib/backup_restore.py
import xbmcgui
import xbmc
import shutil
import os
import time

def backup():
    dialog = xbmcgui.Dialog()
    backup_location = dialog.browse(3, "Choose Backup Folder", "files")
    if backup_location:
        userdata = xbmc.translatePath("special://profile/")
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_folder = os.path.join(backup_location, f"KodiBackup_{timestamp}")

        try:
            shutil.copytree(userdata, backup_folder)
            dialog.ok("Backup Complete", f"Backed up to {backup_folder}")
        except Exception as e:
            dialog.ok("Backup Error", str(e))

def restore():
    dialog = xbmcgui.Dialog()
    restore_location = dialog.browse(3, "Select Backup Folder", "files")
    if restore_location:
        userdata = xbmc.translatePath("special://profile/")
        confirm = dialog.yesno(
            "Confirm Restore",
            "This will overwrite your current Kodi userdata. Continue?"
        )
        if confirm:
            try:
                # Remove existing userdata
                shutil.rmtree(userdata, ignore_errors=True)
                # Copy the backup to userdata
                shutil.copytree(restore_location, userdata)
                
                # Inform the user restore is complete
                dialog.ok(
                    "Restore Completed",
                    "Your Kodi userdata has been restored successfully!"
                )
                
                # Prompt to restart
                restart_now = dialog.yesno(
                    "Restart Required",
                    "Kodi must be restarted to see changes.\nWould you like to restart now?",
                    yeslabel="Restart Now",
                    nolabel="Later"
                )
                if restart_now:
                    # Common approach: instruct Kodi to quit so user can relaunch.
                    xbmc.executebuiltin("Quit")
                    # Alternatively, some Kodi versions/platforms support:
                    # xbmc.executebuiltin("RestartApp")
                    
            except Exception as e:
                dialog.ok("Restore Error", str(e))
