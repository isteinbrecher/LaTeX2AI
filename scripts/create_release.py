# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# MIT License
#
# Copyright (c) 2020-2025 Ivo Steinbrecher
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -----------------------------------------------------------------------------
"""Compile and create a release for LaTeX2AI."""

import os
import shutil
import subprocess  # nosec B404
from pathlib import Path

from utils import (
    check_clean_repo,
    create_zip,
    get_git_tag_or_hash,
    get_repository_dir,
    remove_path,
)

OS_TYPE_FULL = {"mac": "macOS", "win": "Windows"}

if __name__ == "__main__":
    # Execution part of script

    repo_dir = get_repository_dir()

    # Check if this is a clean repository
    check_clean_repo(repo_dir)

    # Sign the UI folder
    subprocess.call(  # nosec B603
        [os.path.join(repo_dir, "scripts/ui_signing/sign_ui_folder.sh")],
        # stdout=open(os.devnull, "wb"),
    )
    ui_release_dir = repo_dir / "scripts" / "ui_signing" / "com.isteinbrecher.latex2ai"
    if not os.path.isdir(ui_release_dir):
        raise ValueError("Could find the signed UI folder")

    # Get the current git identifier
    _, short_sha = get_git_tag_or_hash(repo_dir)

    # Get the previously build executables
    directory = repo_dir / "gathered_artifacts"
    for file_path in directory.iterdir():
        name_split = file_path.name.split(".")
        if not name_split[1] == short_sha:
            raise ValueError(
                f"The git sha for {file_path.name} does not match the one from the repo {short_sha}"
            )
        illustrator_version = name_split[2].split("_")[2]
        os_type = name_split[3]
        build_type = name_split[4]

        # Prepare the executable
        new_file_path = file_path.parent / "LaTeX2AI.aip"
        file_path.rename(new_file_path)

        # Prepare the readme file
        readme_file = repo_dir / "scripts" / f"README_{os_type}.txt"
        readme_file_new = repo_dir / "scripts" / "README.txt"
        shutil.copy2(readme_file, readme_file_new)

        create_zip(
            Path("final_release_files")
            / f"LaTeX2AI_{short_sha}_{OS_TYPE_FULL[os_type]}_Illustrator{illustrator_version}_{build_type}.zip",
            [
                new_file_path,
                ui_release_dir,
                readme_file_new,
            ],
        )

        # Remove the executable, since we don'd need it anymore
        remove_path(new_file_path)
