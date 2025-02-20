# default.py
import xbmcaddon
import xbmcgui
import sys

# If you have backup/restore and maintenance modules, import them:
# (Adjust import paths if needed.)
from resources.lib.backup_restore import backup, restore
from resources.lib.maintenance import clear_cache, remove_thumbs, enable_auto_maintenance, disable_auto_maintenance

# Reference to your add-on, matching the 'id' in addon.xml
ADDON = xbmcaddon.Addon(id='plugin.program.nativowizard')

def show_main_menu():
    """
    Displays a simple "main menu" using dialog options.
    Script add-ons do not have plugin handles, so we rely on dialogs or WindowXML.
    """
    options = [
        "Install Build",
        "Backup Kodi",
        "Restore Kodi",
        "Maintenance",
        "Exit"
    ]
    dialog = xbmcgui.Dialog()
    choice = dialog.select("Nativo Wizard - Main Menu", options)
    
    if choice == 0:
        install_build()
    elif choice == 1:
        backup()
    elif choice == 2:
        restore()
    elif choice == 3:
        show_maintenance_menu()
    elif choice == 4 or choice == -1:  # -1 if user presses ESC/back
        # Exit the script
        return

def install_build():
    """
    Placeholder for your build-installation logic.
    Could involve downloading a ZIP, extracting, and restarting Kodi.
    """
    xbmcgui.Dialog().ok("Install Build", "Implement your download & extract logic here.")
    # Example: If user must restart Kodi after install, you might prompt:
    # if xbmcgui.Dialog().yesno("Restart Now?", "Do you want to quit Kodi to finalize changes?"):
    #     xbmc.executebuiltin("Quit")

def show_maintenance_menu():
    """
    Displays maintenance options (auto-maintenance, clearing cache, removing thumbnails, etc.).
    """
    options = [
        "Clear Cache",
        "Remove Thumbnails",
        "Enable Auto Maintenance",
        "Disable Auto Maintenance",
        "Back"
    ]
    dialog = xbmcgui.Dialog()
    choice = dialog.select("Maintenance Options", options)
    
    if choice == 0:
        clear_cache()
    elif choice == 1:
        remove_thumbs()
    elif choice == 2:
        enable_auto_maintenance()
    elif choice == 3:
        disable_auto_maintenance()
    elif choice == 4 or choice == -1:
        return
    
    # After performing an action, show the menu again so the user can do more tasks
    show_maintenance_menu()

if __name__ == "__main__":
    # Show the main wizard menu as soon as the script runs
    show_main_menu()
