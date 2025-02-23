# Nativo Wizard

A custom Kodi wizard for auto maintenance and build management. This wizard allows you to enable or disable automatic cache clearing at Kodi startup, and to manually clear the cache at any time. It also provides an “Install Build” option—although currently, **no build ZIP is linked**, so the install feature is not functional yet.

## Features

1. **Auto Maintenance**  
   - When enabled (via “Enable Auto Maintenance”), the wizard will automatically clear Kodi’s cache at startup.
   - A progress notification will appear briefly, indicating the task is running.

2. **Manual Cache Clearing**  
   - You can choose “Clear Cache” from the Maintenance menu to remove temporary files any time you like.

3. **Build Installation (Not Yet Linked)**  
   - The wizard includes a menu option to “Install Build,” but as of now, **no build ZIP** is referenced.  
   - Once a build ZIP is added and hosted, the wizard can download and extract the build into Kodi’s folders, prompting a restart.

4. **Thumbnail Removal (Disabled)**  
   - The code for removing thumbnails has been temporarily disabled for further testing. It will be restored in a future update once stable.

## Installation

1. **Download or Clone this Repository**  
   - Copy the folder **`plugin.program.nativowizard`** (containing `addon.xml`, `default.py`, `service.py`, and `resources/`) into your Kodi `addons` directory.

2. **Restart Kodi**  
   - Kodi will load the wizard automatically as a service on startup.

3. **Access the Wizard**  
   - Go to **Add-ons** > **Program Add-ons** > **Nativo Wizard**.  
   - Select it to open the wizard’s main menu.

## Usage

- **Enable/Disable Auto Maintenance**  
  - In the Maintenance menu, you can toggle “Enable Auto Maintenance on Startup” or “Disable Auto Maintenance on Startup.”  
  - When enabled, the wizard clears the cache automatically each time Kodi starts.

- **Manually Clear Cache**  
  - In the Maintenance menu, choose “Manually Clear Cache.”  
  - The wizard removes temporary files in `special://temp/`.

- **Install Build**  
  - Presently **not functional** (no linked build).  
  - After the build ZIP link is added, you can click “Install Build” to download and install a preconfigured Kodi build, overwriting your current setup.

## Roadmap

- **Add Build ZIP Link**  
  - Update the wizard to reference a valid build ZIP URL so the “Install Build” feature works.

- **Re-enable Thumbnail Removal**  
  - Implement and re-test the thumbnail removal functionality once we confirm stable behavior.

- **Enhanced Options**  
  - Possibly add custom backup/restore routines, automatic updates, or additional housekeeping tasks.

## Disclaimer

Use this wizard at your own risk. Clearing cache or installing builds can overwrite user settings and data. Always back up your existing Kodi configuration if you have important customizations.

---

**Author**: Josh Rodriguez  
**Add-on ID**: `plugin.program.nativowizard`
