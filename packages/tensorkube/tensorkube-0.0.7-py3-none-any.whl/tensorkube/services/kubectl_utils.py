import platform
import subprocess


def check_and_install_kubectl():
    """Check if kubectl is installed and install it if it's not."""
    try:
        subprocess.run(["kubectl", "version", "--client"], check=True)
        print("kubectl is already installed.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("kubectl is not installed. Proceeding with installation.")
        if platform.system() == "Darwin":
            try:
                subprocess.run(["brew", "install", "kubectl"], check=True)
            except subprocess.CalledProcessError as e:
                print("Unable to install kubectl using Homebrew. Please install kubectl manually.")
                raise e
        elif platform.system() == "Linux":
            try:
                with open('/etc/os-release') as f:
                    os_info = f.read().lower()
                    if 'debian' in os_info or 'ubuntu' in os_info:
                        # Check if Snap is installed
                        snap_installed = subprocess.run(["which", "snap"], check=False).returncode == 0

                        if not snap_installed:
                            # Install Snap
                            subprocess.run(["sudo", "apt-get", "update"], check=True)
                            subprocess.run(["sudo", "apt-get", "install", "-y", "snapd"], check=True)

                        # Install kubectl using Snap
                        subprocess.run(["sudo", "snap", "install", "kubectl", "--classic"], check=True)
                    else:
                        print("Unsupported Linux distribution. Please install kubectl manually.")
                        raise Exception('Unsupported Linux distribution.')
            except subprocess.CalledProcessError as e:
                print("Unable to install kubectl. Please install kubectl manually.")
                raise e
        else:
            print("Unsupported operating system. Please install kubectl manually.")
            raise Exception('Unsupported operating system.')

        # Verify kubectl installation
        try:
            subprocess.run(["kubectl", "version", "--client"], check=True)
            print("kubectl installed successfully.")
        except subprocess.CalledProcessError as e:
            print("kubectl installation failed. Please install kubectl manually.")
            raise e


def check_and_install_helm():
    """Check if helm is installed and install it if it's not."""
    try:
        subprocess.run(["helm", "version"], check=True)
        print("Helm is already installed.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Helm is not installed. Proceeding with installation.")
        if platform.system() == "Darwin":
            try:
                subprocess.run(["brew", "install", "helm"], check=True)
            except subprocess.CalledProcessError as e:
                print("Unable to install helm using Homebrew. Please install helm manually.")
                raise e
        elif platform.system() == "Linux":
            try:
                # Check if Snap is installed
                snap_installed = subprocess.run(["which", "snap"], check=False).returncode == 0

                if not snap_installed:
                    # Install Snap
                    distro = platform.linux_distribution()[0].lower()
                    if 'ubuntu' in distro or 'debian' in distro:
                        subprocess.run(["sudo", "apt-get", "update"], check=True)
                        subprocess.run(["sudo", "apt-get", "install", "-y", "snapd"], check=True)
                    elif 'centos' in distro or 'redhat' in distro:
                        subprocess.run(["sudo", "yum", "update"], check=True)
                        subprocess.run(["sudo", "yum", "install", "-y", "epel-release"], check=True)
                        subprocess.run(["sudo", "yum", "install", "-y", "snapd"], check=True)
                        subprocess.run(["sudo", "systemctl", "enable", "--now", "snapd.socket"], check=True)
                        subprocess.run(["sudo", "ln", "-s", "/var/lib/snapd/snap", "/snap"], check=True)
                    else:
                        print("Unsupported Linux distribution. Please install helm manually.")
                        raise Exception('Unsupported Linux distribution.')

                # Install helm using Snap
                subprocess.run(["sudo", "snap", "install", "helm", "--classic"], check=True)
                print("Helm installed successfully using Snap.")
            except subprocess.CalledProcessError as e:
                print("Unable to install helm using Snap. Please install helm manually.")
                raise e
        else:
            print("Unsupported operating system. Please install helm manually.")
            raise Exception('Unsupported operating system.')

        # Verify helm installation
        try:
            subprocess.run(["helm", "version"], check=True)
            print("Helm installed successfully.")
        except subprocess.CalledProcessError as e:
            print("Helm installation failed. Please install helm manually.")
            raise e
