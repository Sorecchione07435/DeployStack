# DeployStack

DeployStack is a command-line utility for deploying OpenStack on Debian.  
The instructions below describe a **temporary installation** method for development or testing, until an official `.deb` package is released.

---

## 1. System Preparation

Ensure you have the necessary tools for Python 3:

```bash
sudo apt update -y
sudo apt install python3-pip python3-venv git -y
```

* `python3-pip` allows you to use `pip` to install Python packages.
* `python3-venv` allows you to create isolated virtual environments with `python3 -m venv`.
* `git` is needed to clone the repository.

---

## 2. Clone the repository

Clone DeployStack into a directory of your choice (e.g., in your home folder):

```bash
git clone https://github.com/Sorecchione07435/DeployStack.git ~/DeployStack
cd ~/DeployStack
```

---

## 3. Create a Python virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

> Using a virtual environment avoids conflicts with system packages.

---

## 4. Install DeployStack

```bash
pip install --upgrade pip
pip install .
```

* This installs DeployStack and its Python dependencies inside the virtual environment.

---

## 5. Install additional dependencies (optional)

Most Python dependencies are installed automatically by pip.
If you prefer, you can also install system packages:

```bash
sudo apt install python3-dotenv python3-psutil python3-yaml -y
```

> Recommended: using pip inside the virtual environment is safer for development.

---

## 6. Run DeployStack

With the virtual environment active:

```bash
deploystack --help
```

* This displays available commands and CLI usage.
* No need to manually move files to `/usr/bin/`.

---

✅ DeployStack is now ready for development and testing.

> ⚠️ **Note:** For production, an official `.deb` package will be provided, which installs the CLI properly in the system PATH and manages dependencies automatically.

---

## 7. Update DeployStack during development

If you want to pull the latest changes from the repository:

```bash
cd ~/DeployStack
git pull
```

* The installed package will reflect updates after reinstalling with `pip install .`.



For usage instructions and additional documentation, see the Wiki at [DeployStack Wiki](https://github.com/Sorecchione07435/DeployStack/wiki).
