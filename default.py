import sys
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmc

from resources.lib.backup_restore import backup, restore
from resources.lib.maintenance import clear_cache, remove_thumbs

ADDON = xbmcaddon.Addon(id='plugin.program.mywizard')

def main_menu():
    add_menu_item('Install Build', action='install_build')
    add_menu_item('Backup Kodi', action='backup')
    add_menu_item('Restore Kodi', action='restore')
    add_menu_item('Maintenance', action='maintenance')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def add_menu_item(label, action=''):
    url = f"{sys.argv[0]}?action={action}"
    item = xbmcgui.ListItem(label=label)
    xbmcplugin.addDirectoryItem(
        handle=int(sys.argv[1]),
        url=url,
        listitem=item,
        isFolder=False
    )

def install_build():
    xbmcgui.Dialog().ok("Install Build", "Install build placeholder")

def run_action(params):
    action = params.get('action', '')
    if action == 'install_build':
        install_build()
    elif action == 'backup':
        backup()
    elif action == 'restore':
        restore()
    elif action == 'maintenance':
        clear_cache()
        remove_thumbs()
    else:
        main_menu()

def parse_parameters():
    import urllib.parse
    if len(sys.argv) > 2:
        param_string = sys.argv[2]
        if param_string.startswith('?'):
            param_string = param_string[1:]
        return dict(urllib.parse.parse_qsl(param_string))
    return {}

if __name__ == '__main__':
    params = parse_parameters()
    run_action(params)
