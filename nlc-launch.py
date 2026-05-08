import argparse
import os
import sys

def create_desktop_file(command, chroot_name, app_name, icon_path):
    chroot_path = f"/nsm/chroots/{chroot_name}"
    
    if not os.path.isdir(chroot_path):
        print(f"Error: Chroot '{chroot_name}' not found at /nsm/chroots/")
        sys.exit(1)

    desktop_content = f"""[Desktop Entry]
Name={app_name}
Exec=pkexec nlc -e -n="{chroot_name}" -exec="{command}"
Icon={icon_path}
Type=Application
Terminal=false
Categories=Utility;
"""
    
    filename = f"{app_name.lower().replace(' ', '-')}.desktop"
    filepath = os.path.expanduser(f"~/.local/share/applications/{filename}")

    try:
        with open(filepath, "w") as f:
            f.write(desktop_content)
        
        os.chmod(filepath, 0o755)
        
        print(f"Success: Launcher created at {filepath}")
        print("This application will run as ROOT via pkexec.")
        print(f"Running '{command}' as root can have CATASTROPHIC effects")
        print(f"inside the chroot '{chroot_name}' if the app is malicious.")
        
    except Exception as e:
        print(f"Failed to create file: {e}")

def main():
    parser = argparse.ArgumentParser(prog="nlc-launch")
    parser.add_argument("--export", required=True, help="Command to execute")
    parser.add_argument("-c", "--chroot", required=True, help="Name of the chroot")
    parser.add_argument("-n", "--name", required=True, help="Name of the application")
    parser.add_argument("-i", "--icon", required=True, help="Icon name or path")

    args = parser.parse_args()

    create_desktop_file(args.export, args.chroot, args.name, args.icon)

if __name__ == "__main__":
    main()
