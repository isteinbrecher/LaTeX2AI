![LaTeX2AI](/doc/logo/logo_black.png?raw=true)

LaTeX2AI is a plugin for Adobe Illustrator (macOS and Windows) that enables the use of editable text labels typeset in LaTeX inside an Illustrator document.

# License & How to Cite

LaTeX2AI is under the MIT license, see [./LICENSE](LICENSE).
If you use LaTeX2AI to create figures for your work, please acknowledge it with a link to the GitHub repository.
For example:

-   Sketches in this work have been created using the Adobe Illustrator plug-in LaTeX2AI ([https://github.com/isteinbrecher/latex2ai](https://github.com/isteinbrecher/latex2ai)).

Feel free to leave a :star: on [GitHub](https://github.com/isteinbrecher/latex2ai).
You can also add your work to [Work that uses LaTeX2AI](#work-that-uses-latex2ai).

# Installation

### Requirements

The following software dependencies are required to run LaTeX2AI:

-   A LaTeX compiler such as [TeX Live](https://www.tug.org/texlive) or [MiKTeX](https://miktex.org)
-   [Ghostscript](https://www.ghostscript.com)

### Windows

1. Download LaTeX2AI from the [GitHub release page](https://github.com/isteinbrecher/latex2ai/releases).
1. Unzip the `.zip` file.
1. Copy the user interface folder `com.isteinbrecher.latex2ai`:

    - Installation for **current user**:
        - Copy `com.isteinbrecher.latex2ai` to `C:\Users\<USERNAME>\AppData\Roaming\Adobe\CEP\extensions` (you may need to create this directory).
    - Installation for **all users** (requires administrator privileges):
        - Copy `com.isteinbrecher.latex2ai` to `C:\Program Files\Common Files\Adobe\CEP\extensions\`

1. Copy the plugin:

    - Installation for **current user**:
        - Copy `WIN/LaTeX2AI.aip` to any directory. Set this as the Adobe Illustrator plugin directory via `Edit > Preferences > Plug-ins & Scratch Disks... > Additional Plug-ins Folder`.
    - Installation for **all users** (requires administrator privileges):
        - Copy `WIN/LaTeX2AI.aip` to `C:\Program Files\Adobe\Adobe Illustrator <YOUR VERSION>\Plug-ins\`

1. Restart Adobe Illustrator. Display the LaTeX2AI tools via `Window > Toolbars > Advanced`.

To uninstall LaTeX2AI, delete the files you copied.

### macOS

1. Download LaTeX2AI from the [GitHub release page](https://github.com/isteinbrecher/latex2ai/releases).
1. Unzip the file.
1. Copy the user interface folder `com.isteinbrecher.latex2ai`:

    - Installation for **current user**:
        - Copy `com.isteinbrecher.latex2ai` to `~/Library/Application Support/Adobe/CEP/extensions/`
    - Installation for **all users** (requires administrator privileges):
        - Copy `com.isteinbrecher.latex2ai` to `/Library/Application Support/Adobe/CEP/extensions/`

1. Copy the plugin:

    - Installation for **current user**:
        - Copy `macOS/LaTeX2AI.aip` to any directory. Set this as the Adobe Illustrator plugin directory via `Edit > Preferences > Plug-ins & Scratch Disks... > Additional Plug-ins Folder`.
    - Installation for **all users** (requires administrator privileges):
        - Copy `macOS/LaTeX2AI.aip` to `/Applications/Adobe Illustrator <YOUR VERSION>/Plug-ins/`

1. Restart Adobe Illustrator. Display the LaTeX2AI tools via `Window > Toolbars > Advanced`.

> Depending on your system settings, you might get the following error message when starting Illustrator:
>
> <img src="/doc/images/macos_permission_error.png?raw=true" alt="macOS permission error" height="350" title="Create / Edit">
>
> This can be resolved by explicitly allowing the gatekeeper to run LaTeX2AI ([see also this thread](https://apple.stackexchange.com/questions/58509/how-can-i-open-a-single-app-by-an-unidentified-developer-without-allowing-all)). To do so, open the terminal and type:
>
> ```bash
> xattr -d com.apple.quarantine <PATH TO LaTeX2AI.aip>
> ```
>
> If you have installed LaTeX2AI for _all_ users, you need to run this command with administrator privileges:
>
> ```bash
> sudo xattr -d com.apple.quarantine <PATH TO LaTeX2AI.aip>
> ```

To uninstall LaTeX2AI, delete the files you copied.

# How to Use LaTeX2AI

LaTeX2AI adds four buttons to the main toolbar:

-   ![Create / Edit](/doc/images/tool_create.png?raw=true "Create / Edit") **Create / Edit**: Edit an existing label by clicking on it, or create a new one by clicking somewhere in the document.
-   ![Redo items](/doc/images/tool_redo.png?raw=true "Redo labels") **Redo LaTeX2AI labels**: Recompile or reset the scale of all existing LaTeX2AI labels.
-   ![LaTeX2AI options](/doc/images/tool_options.png?raw=true "LaTeX2AI options") **LaTeX2AI options**: Open a form to set global LaTeX2AI options and edit the LaTeX header in an external application.
-   ![Save document as PDF](/doc/images/tool_save_as_pdf.png?raw=true "Save document as PDF") **Save as PDF**: Save the current `.ai` document as a `.pdf` with the same name. The LaTeX2AI labels are included.

You can also double-click on a LaTeX2AI label to enter edit mode.

## Create / Edit a LaTeX2AI Label

This form appears when creating or editing labels:

![Create / Edit](/doc/images/create_edit_ui.png?raw=true "The LaTeX2AI Create / Edit form")

### Placement

This option defines how a label behaves when its size changes.

Take for example the well-known formula `$\sum_{k=0}^{\infty}\frac{x^k}{k!}$` placed inside a rectangle:

![Placement small](/doc/images/placement_small.png?raw=true)

The green box shows the size of the label, and the dot marks the placement anchor. When the LaTeX code changes and affects the label size, this anchor point stays in the same position relative to the rectangle.

If the label is changed to `\displaystyle`:

![Placement large](/doc/images/placement_large.png?raw=true)

The size changes, but the anchor position remains fixed.

#### Baseline Placement

An additional placement option is _baseline_, which centers the label's baseline vertically. This allows for an easy alignment with other baseline LaTeX2AI labels or Illustrator text:

![Placement baseline](/doc/images/placement_baseline.png?raw=true)

## Item Scaling Behavior

By default, LaTeX2AI inserts labels with a 1:1 scale: 1pt in LaTeX equals 1pt in Illustrator.
For example, LaTeX labels with 12pt font match Illustrator text set to 12pt.

Labels can be resized like other Illustrator objects, but modifying the LaTeX code resets them to 1:1 scale.

The recommended approach is to keep items at 1:1 scale. This ensures consistent font sizes when exporting and including the artwork in LaTeX documents with `\includegraphics[scale=1]`.

Use the **Redo items** tool to reset the scale of all LaTeX2AI items.

## LaTeX Header

LaTeX2AI assumes that all Illustrator files in the same folder share the same LaTeX header: `LaTeX2AI_header.tex`.

If this file doesn't exist, it is created when needed. You can edit this file to add packages or macros.

## File Structure

LaTeX label `.pdf` files are stored in the `links` subfolder of the document directory.
LaTeX2AI automatically manages these files and deletes unused ones.

# Known Issues

## Creative Cloud Documents

LaTeX2AI does **not** currently support _Creative Cloud documents_.

# Work That Uses LaTeX2AI

An incomplete list of work that uses LaTeX2AI:

-   Toenniessen, F.: _Die Homotopie der Sphären - Eine Einführung in Spektralsequenzen, Lokalisierungen und Kohomologie-Operationen_, Springer Verlag Heidelberg, 2023.
-   Steinbrecher, I., Popp, A., Meier, C.: _Consistent coupling of positions and rotations for embedding 1D Cosserat beams into 3D solid volumes._ Comput Mech (2021), [Open Access](https://doi.org/10.1007/s00466-021-02111-4)
-   Steinbrecher, I., Mayr, M., Grill, M.J., Kremheller, J., Meier, C., Popp, A.: _A mortar-type finite element approach for embedding 1D beams into 3D solid volumes_, Comput Mech (2020), 66(6):1377-1398, [Open Access](https://doi.org/10.1007/s00466-020-01907-0)
-   Steinbrecher, I., Humer, A., Vu-Quoc, L.: _On the numerical modeling of sliding beams: A comparison of different approaches_, Journal of Sound and Vibration, 408:270-290, [Open Access](https://doi.org/10.1016/j.jsv.2017.07.010)

# Contributing

We welcome contributions to LaTeX2AI.

For general questions, feature requests, or bug reports, please open an [issue](https://github.com/isteinbrecher/latex2ai/issues).

To contribute code:

1. Fork the repository and work in a feature branch.
1. Consider opening an issue for discussion if your changes are substantial.
1. When ready, create a pull request to the `develop` branch.

Please also:

-   Compile a debug build and run framework tests in Illustrator ![Framework tests](/doc/images/tool_testing.png?raw=true "Framework tests").
-   Consider adding tests in `./src/tests`.
-   Run `./scripts/check_license.py` to ensure proper license headers.
-   Format code with `clang-format`:
    -   In Visual Studio: `Ctrl-K`, then `Ctrl-D`.
    -   On macOS:
        ```bash
        find src -iname '*.h' -o -iname '*.cpp' | xargs clang-format -i
        ```
-   Add a description of your changes to the [Changelog](doc/CHANGELOG.md).
-   Feel free to add yourself to the [./CONTRIBUTORS](CONTRIBUTORS) file.

# Build LaTeX2AI from Source

Instructions are available [here](doc/BUILD_FROM_SOURCE.md).

# Changelog

See the detailed [changelog](doc/CHANGELOG.md).
