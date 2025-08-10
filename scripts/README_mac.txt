LaTeX2AI - macOS Installation
==============================

This package contains the LaTeX2AI Adobe Illustrator plugin.
https://github.com/isteinbrecher/latex2ai

Requirements:
- A LaTeX distribution (TeX Live or MacTeX)
- Ghostscript

Installation (Current User):
1. Copy the folder `com.isteinbrecher.latex2ai` to:
   ~/Library/Application Support/Adobe/CEP/extensions/

2. Copy `LaTeX2AI.aip` to any directory.
   In Illustrator, enable this path via:
   Edit > Preferences > Plug-ins & Scratch Disks... > Additional Plug-ins Folder.

Installation (All Users - Administrator privileges required):
1. Copy the folder `com.isteinbrecher.latex2ai` to:
   /Library/Application Support/Adobe/CEP/extensions/

2. Copy `LaTeX2AI.aip` to:
   /Applications/Adobe Illustrator <YOUR VERSION>/Plug-ins/

Finally, restart Adobe Illustrator.
You can show the LaTeX2AI toolbar from:
   Window > Toolbars > Advanced

Note:
On macOS you may see a warning when starting Illustrator:
   "LaTeX2AI cannot be opened because it is from an unidentified developer."
To fix this, open Terminal and run:

   xattr -d com.apple.quarantine <PATH TO LaTeX2AI.aip>

If installed for all users, run with sudo:

   sudo xattr -d com.apple.quarantine <PATH TO LaTeX2AI.aip>

Uninstall:
- Delete the files/folders you copied above.

For troubleshooting or Windows instructions, see the full documentation:
https://github.com/isteinbrecher/latex2ai#installation

License:
--------
LaTeX2AI is released under the MIT License.
See the LICENSE file or the project repository for full terms.
