# DeployStack

DeployStack is a command-line utility for deploying OpenStack on your system.  

The instructions below describe a **temporary installation** method, intended for development or testing, until an official `.deb` package is released.

---

## Temporary Installation (Development Version)

1. **Clone the repository** into your Python 3 `dist-packages` folder:

```bash
sudo git clone https://github.com/Sorecchione07435/DeployStack.git /usr/lib/python3/dist-packages/deploystack
```

> If `git` is not installed, install it first:

```bash
sudo apt install git -y
```

2. **Move the `deploystack` executable** to `/usr/bin/` so it can be run directly from the shell:

```bash
sudo mv /usr/lib/python3/dist-packages/deploystack/deploystack /usr/bin/deploystack
```

3. Grant permissions to make it executable with:

```bash
sudo chmod +x /usr/bin/deploystack
```

> ⚠️ This allows you to run `deploystack` directly, without the need for `python3 -m`.

3. **Install essential Python dependencies**:

```bash
sudo apt install python3-dotenv python3-psutil -y
```

---

✅ DeployStack is now ready to use on your system.

> ⚠️ **Note:** These steps are temporary for development/testing purposes.
> An official `.deb` package will be provided in a future release for easier installation and updates.

For usage instructions and additional documentation, see the Wiki at [DeployStack Wiki](https://github.com/Sorecchione07435/DeployStack/wiki).