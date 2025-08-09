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
"""Python utility functions."""

# Import python modules.
import os
import platform
import shutil
import subprocess  # nosec B404
import sys
import zipfile
from pathlib import Path


def get_repository_dir():
    """Get the root directory of this repository."""

    script_path = os.path.realpath(__file__)
    root_dir = Path(os.path.dirname(os.path.dirname(script_path)))
    return root_dir


def check_clean_repo(repo_dir):
    """Check if this is a clean repository."""
    is_clean_repo = clean_repository(repo_dir)
    if not is_clean_repo:
        if input("Repository is not clean. Do You Want To Continue? ").lower() != "y":
            sys.exit(1)


def get_git_sha(repo=None):
    """Return the git sha of the repository."""

    # Get the git sha of the repository.
    process = subprocess.Popen(  # nosec B603 B607
        ["git", "rev-parse", "HEAD"], stdout=subprocess.PIPE, cwd=repo
    )
    out, _err = process.communicate()
    return out.decode("UTF-8").strip()


def get_git_tag_or_hash(repo=None):
    """Return the commit, if the commit has a tag, return the tag."""

    if is_github_runner():
        # If this is executed by a GitHub runner, we get the sha from the following
        # environment variable.
        git_sha = os.environ["GITHUB_SHA"]
        return git_sha, git_sha[:7]

    # Get current sha.
    git_sha = get_git_sha(repo)

    # Get all tags and their sha.
    process = subprocess.Popen(  # nosec B603 B607
        ["git", "show-ref", "--tags"], stdout=subprocess.PIPE, cwd=repo
    )
    out, _err = process.communicate()
    tags = out.decode("UTF-8").strip().split("\n")
    tags = [line.split(" ") for line in tags]
    for sha, tag in tags:
        if sha == git_sha:
            # This commit has a tag, return the tag.
            return git_sha, tag.split("/")[-1]
    return git_sha, git_sha[:7]


def clean_repository(repository_dir):
    """Check if the repository is clean."""

    # Check if the repository is clean.
    os.chdir(repository_dir)
    out = subprocess.check_output(  # nosec B603 B607
        ["git", "status", "--untracked-files=no", "--porcelain"]
    )
    if out == b"":
        return True
    else:
        return False


def is_github_runner():
    """Check if this script is executed by a github runner."""
    return "GITHUB_SHA" in os.environ.keys()


def is_windows():
    """Check if this script is executed on Windows."""
    return platform.system() == "Windows"


def create_zip(output_zip: str, items: list[Path]):
    """Create a zip file containing the given files and folders."""
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for item in items:
            item = Path(item)
            if item.is_file():
                # Add single file
                zf.write(item, arcname=item.name)
            elif item.is_dir():
                # Walk folder and add files relative to the folder
                for root, _, files in os.walk(item):
                    for file in files:
                        filepath = Path(root) / file
                        arcname = filepath.relative_to(item.parent)
                        zf.write(filepath, arcname=arcname)


def remove_path(p: Path):
    """Remove a file or directory."""
    if p.is_file() or p.is_symlink():
        p.unlink()
    elif p.is_dir():
        shutil.rmtree(p)
