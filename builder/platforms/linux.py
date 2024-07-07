import os

from builder.config import get_build_args
from builder.utils import (
    Logger,
    archive_build_output,
    run_command,
    store_includes,
)


def setup_env():
    # # Update package lists
    # run_command(
    #     ["sudo", "apt-get", "update"],
    #     "Updating package lists",
    # )

    # FIXME: update to make it install the lastest release
    # Install Bazelisk
    run_command(
        [
            "sudo", "wget", 
            "https://github.com/bazelbuild/bazelisk/releases/download/v1.20.0/bazelisk-linux-amd64",
            "-O", "/usr/local/bin/bazelisk"
        ],
        "Downloading Bazelisk"
    )
    # run_command(
    #     ["sudo", "chmod", "+x", "/usr/local/bin/bazelisk"],
    #     "Making Bazelisk executable"
    # )
    run_command(
        ["bazelisk", "version"],
        "Testing Bazelisk installation"
    )

    # Install LLVM
    run_command(
        ["wget", "https://apt.llvm.org/llvm.sh", "-O", "/tmp/llvm.sh"],
        "Downloading LLVM installation script"
    )
    run_command(
        ["sudo", "chmod", "+x", "/tmp/llvm.sh"],
        "Making LLVM installation script executable"
    )
    run_command(
        ["sudo", "bash", "/tmp/llvm.sh"],
        "Running LLVM installation script"
    )
    # run_command(
    #     ["which", "clang"],
    #     "Check clang version"
    # )
    # run_command(
    #     ["clang", "--version"],
    #     "Check clang version"
    # )

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
        [os.path.join(os.getcwd(), "depot_tools", "gclient")],
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
    
    # Install Skia extra dependencies
    run_command(
        [os.path.join(os.getcwd(), "skia", "tools", "install_dependencies.sh")],
        "Install Skia Extra Dependencies",
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


def build(custom_build_args=None, archive_output=False):
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

    build_args = custom_build_args or get_build_args("linux-x64")
    run_command(
        [
            os.path.join(os.getcwd(), "skia", "bin", "gn"),
            "gen",
            "out/linux-x64",
            f"--args={build_args}",
        ],
        "Generating Build Files",
        cwd=skia_path,
    )

    run_command(
        [os.path.join(os.getcwd(), "depot_tools", "ninja"), "-C", "out/linux-x64"],
        "Building Skia for linux-x64",
        cwd=skia_path,
    )

    if archive_output:
        archive_build_output(os.path.join(skia_path, "out", "linux-x64"))
