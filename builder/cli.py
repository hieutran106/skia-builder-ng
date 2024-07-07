import platform
import argparse
import sys

from builder.config import parse_custom_build_args
from builder.platforms import (
    android,
    # ios,
    linux,
    # darwin,
    windows,
)


def setup_env(platform, sub_env=None):
    platform_actions = {
        "Android": android.setup_env,
        # "iOS": ios.setup_env,
        "Linux": linux.setup_env,
        # "Darwin": darwin.setup_env,
        "Windows": windows.setup_env,
    }
    
    # Use sub_env if provided, otherwise default to the detected platform
    target_platform = sub_env if sub_env else platform
    
    action = platform_actions.get(target_platform)
    if action:
        action()
    else:
        print(f"Unknown platform: {target_platform}")
        sys.exit(1)


def build(platform, custom_build_args, archive_build_output, sub_env=None):
    platform_actions = {
        "Android": android.build,
        # "iOS": ios.build,
        "Linux": linux.build,
        # "Darwin": darwin.build,
        "Windows": windows.build,
    }
    
    # Use sub_env if provided, otherwise default to the detected platform
    target_platform = sub_env if sub_env else platform
    
    action = platform_actions.get(target_platform)
    if action:
        action(custom_build_args, archive_build_output)
    else:
        print(f"Unknown platform: {target_platform}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Skia Builder Script")
    parser.add_argument(
        "command",
        type=str,
        help="Command to execute, e.g., setup-env, build",
    )
    parser.add_argument(
        "--sub-env",
        type=str,
        help="Optional sub-environment to configure, e.g., Android, iOS",
    )
    parser.add_argument(
        "--custom-build-args",
        type=str,
        help="Custom arguments for the build configuration",
    )
    parser.add_argument(
        "--archive",
        action="store_true",
        help="Archive the build output after compilation",
    )

    args = parser.parse_args()
    custom_build_args = (
        parse_custom_build_args(args.custom_build_args)
        if args.custom_build_args
        else {}
    )

    current_platform = platform.system()

    if args.command == "setup-env":
        setup_env(current_platform, args.sub_env)
    elif args.command == "build":
        build(current_platform, custom_build_args, args.archive, args.sub_env)
    else:
        print(f"Unknown command: {args.command}")
        sys.exit(1)


if __name__ == "__main__":
    main()





# skia-builder setup-env
# skia-builder setup-env --sub-env=Android
# skia-builder build --sub-env=Android
# skia-builder build --custom-build-args="cc=clang cxx=clang++ skia_compile_modules=true ..."
# skia-builder build --archive --custom-build-args="cc=clang cxx=clang++ skia_compile_modules=true ..."