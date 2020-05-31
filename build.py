import PyInstaller.__main__ as pi
import os

app_name = "wml-tool"
cwd_path = os.path.dirname(os.getcwd())
output_path = os.path.join(cwd_path, "wml-build")
script_file = os.path.join(os.path.dirname(__file__), "cli.py")

__build_arguments = [
    f"--name={app_name}",
    f"--onefile",
    f"--specpath={output_path}",
    f"--distpath={os.path.join(output_path, 'dist')}",
    f"--workpath={os.path.join(output_path, 'build')}",
    f"--noconfirm",
    "--clean",
    "--log-level=WARN",
    f"{script_file}"
]

def build_linux():
    pi.run(__build_arguments)
    pass

def build_window():
    pass

if __name__ == "__main__":
    build_linux()