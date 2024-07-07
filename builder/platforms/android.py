import os

from builder.config import get_build_args
from builder.utils import (
    Logger,
    archive_build_output,
    run_command,
    store_includes,
)


def setup_env():
    # Verify Chocolatey Installation
    run_command(
        ["choco", "--version"],
        "Verifying Chocolatey Installation",
    )

    # Install Bazelisk, Ninja, and LLVM
    # tools_to_install = ["bazelisk", "ninja", "llvm"]
    tools_to_install = ["bazelisk", "llvm"]
    for tool in tools_to_install:
        run_command(
            ["choco", "install", tool, "-y"],
            f"Installing {tool}",
        )

    # Clone depot_tools
    run_command(
        [
            "git",
            "clone",
            "https://chromium.googlesource.com/chromium/tools/depot_tools.git",
        ],
        "Cloning depot_tools",
    )

    # Verify Depot Tools Installation
    run_command(
        [os.path.join(os.getcwd(), "depot_tools", "gclient.bat")],
        "Verifying Depot Tools Installation",
    )

    # Clone Skia Repository and Fetch Dependencies
    run_command(
        ["git", "clone", "https://skia.googlesource.com/skia.git"],
        "Cloning Skia Repository",
    )

    skia_path = os.path.join(os.getcwd(), "skia")

    # Fetch and checkout to the specific branch (Chrome/m131)
    run_command(
        ["git", "fetch", "-v"],
        "Fetching Skia Repository",
        cwd=skia_path,
    )
    run_command(
        ["git", "checkout", "origin/chrome/m131"],
        "Checking out Chrome/m131 branch",
        cwd=skia_path,
    )

    # Sync Skia dependencies using git-sync-deps script
    run_command(
        ["python3", "tools/git-sync-deps"],
        "Syncing Skia Dependencies",
        cwd=skia_path,
    )

    # Fetch Ninja binary for Skia
    run_command(
        ["python3", "bin/fetch-ninja"],
        "Fetching Ninja for Skia",
        cwd=skia_path,
    )






    # Download Android NDK
    run_command(
        ["curl", "-o", "android-ndk-r27-windows.zip", "https://dl.google.com/android/repository/android-ndk-r27-windows.zip"],
        "Downloading Android NDK"
    )
    # Unzip Android NDK
    run_command(
        ["powershell", "-Command", "Expand-Archive -Path 'android-ndk-r27-windows.zip' -DestinationPath 'C:/Program Files/NDK'"],
        "Extracting Android NDK"
    )
    # run_command(
    #     ["del", "android-ndk-r27-windows.zip"],
    #     "Cleaning up the downloaded zip file"
    # )






def build(target_cpu=None, custom_build_args=None, archive_output=False):
    Logger.info(
        f"Building with {'custom' if custom_build_args else 'default'} "
        "arguments."
    )
    Logger.info(
        "Archiving build output."
        if archive_output
        else "Build output will not be archived."
    )

    skia_path = os.path.join(os.getcwd(), "skia")

    if archive_output:
        store_includes(skia_path)

    build_target = f"android-{target_cpu or 'arm'}"
    print(">>>>>", build_target)

    build_args = custom_build_args or get_build_args(build_target)
    run_command(
        [
            "skia/bin/gn.exe",
            "gen",
            f"out/{build_target}",
            f"--args={build_args}",
        ],
        "Generating Build Files",
        cwd=skia_path,
    )

    run_command(
        [
            os.path.join(os.getcwd(), "depot_tools", "ninja.bat"),
            "-C",
            f"out/{build_target}",
        ],
        f"Building Skia for {build_target}",
        cwd=skia_path,
    )

    if archive_output:
        archive_build_output(
            os.path.join(skia_path, "out", f"{build_target}")
        )
