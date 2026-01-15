# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# MIT License
#
# Copyright (c) 2020-2026 Ivo Steinbrecher
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
    get_git_tag_or_hash,
    get_repository_dir,
    is_github_runner,
    is_windows,
)


def build_solution_windows(repo_dir, build_type):
    """Build the solution.

    Returns:
        Path to the created executable.
    """

    script_dir = os.path.join(repo_dir, "scripts")
    os.chdir(script_dir)
    return_value = subprocess.call(["compile_solution.bat"])  # nosec B603 B607
    if return_value == 0:
        executable_dir = os.path.realpath(
            os.path.join(repo_dir, "..\\output", "win", "x64", build_type)
        )
        executable = os.path.join(executable_dir, "LaTeX2AI.aip")
        return Path(executable)
    else:
        raise ValueError("Could not build solution")


def build_solution_mac(repo_dir, build_type):
    """Build the solution.

    Returns:
        Path to the created executable.
    """
    return_value = subprocess.call(os.path.join(repo_dir, "scripts/compile_mac.sh"))  # nosec B603
    if return_value == 0:
        mac_release_dir = (
            Path(repo_dir) / ".." / "output" / "mac" / build_type / "LaTeX2AI.aip"
        )
        if not mac_release_dir.exists():
            raise ValueError("Executable not found")
        return mac_release_dir
    else:
        raise ValueError("Could not build solution")


if __name__ == "__main__":
    # Execution part of script

    # Set default environment variables
    default_env_values = [
        (
            "PYTHON_EXE",
            "python",
        ),
        (
            "L2A_BUILD_TYPE",
            "release",
        ),
        (
            "VS_ACTIVATION_SCRIPT",
            "C:\\Program Files\\Microsoft Visual Studio\\2022\\Community\\Common7\\Tools\\VsDevCmd.bat",
        ),
        (
            "AI_SDK_VERSION",
            "",
        ),
        ("RELEASE_PATH_RELATIVE_TO_REPO", "."),
    ]
    for key, default_value in default_env_values:
        if key not in os.environ:
            os.environ[key] = default_value

    # Get some basic repo/git information
    repo_dir = get_repository_dir()
    git_sha, git_identifier = get_git_tag_or_hash(repo_dir)
    os.environ["L2A_GIT_IDENTIFIER"] = git_identifier

    # Check if this is a clean repository
    check_clean_repo(repo_dir)

    # Build LaTeX2AI release
    build_type = os.environ["L2A_BUILD_TYPE"]
    if is_windows():
        executable = build_solution_windows(repo_dir, build_type)
    else:
        executable = build_solution_mac(repo_dir, build_type)

    # If this is run on GitHub, move the executable to the executable folder.
    if is_github_runner:
        final_name_parts = ["LaTeX2AI", git_identifier]
        if not os.environ.get("AI_SDK_VERSION") == "":
            final_name_parts.append(os.environ.get("AI_SDK_VERSION"))
        final_name_parts.append("win" if is_windows() else "mac")
        final_name_parts.append(build_type)
        final_name = f"{'.'.join(final_name_parts)}.aip"
        final_path = (
            Path(repo_dir) / os.environ["RELEASE_PATH_RELATIVE_TO_REPO"] / final_name
        )
        final_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(executable), str(final_path))
