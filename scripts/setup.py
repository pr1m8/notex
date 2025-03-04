import subprocess
import platform
import shutil
import sys

REQUIRED_BINARIES = ["pdflatex", "xelatex", "lualatex", "pdfinfo", "pdftoppm"]

def check_dependencies():
    """Check if required system dependencies are installed."""
    missing = [binary for binary in REQUIRED_BINARIES if not shutil.which(binary)]
    if missing:
        print(f"⚠️  Missing system dependencies: {', '.join(missing)}")
        return False
    print("✅ All required dependencies are installed.")
    return True

def install_dependencies():
    """Attempt to install missing dependencies automatically."""
    system = platform.system().lower()

    if system == "linux":
        print("🔧 Installing dependencies for Linux...")
        try:
            subprocess.run(["sudo", "apt", "update"], check=True)  # Run `apt update` first
            subprocess.run([
                "sudo", "apt", "install", "-y",
                "texlive-latex-extra", "texlive-xetex", "texlive-luatex",
                "poppler-utils", "ghostscript"
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Installation failed: {e}")
            sys.exit(1)

    elif system == "darwin":
        print("🔧 Installing dependencies for macOS...")
        try:
            subprocess.run(["brew", "install", "mactex", "poppler", "ghostscript"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Installation failed: {e}")
            sys.exit(1)

    elif system == "windows":
        print("⚠️ Windows detected. Please install the following manually:")
        print("- MiKTeX: https://miktex.org/download")
        print("- Poppler: https://github.com/oschwartz10612/poppler-windows/releases")
        print("Make sure to add `Poppler/bin/` to your PATH.")
        sys.exit(1)
    else:
        print(f"❌ Unsupported OS: {system}. Install dependencies manually.")
        sys.exit(1)

def main():
    """Main entry point for the script."""
    print("🔍 Checking system dependencies for Notex...")
    if not check_dependencies():
        install_dependencies()
    else:
        print("🎉 Setup complete!")

if __name__ == "__main__":
    main()
