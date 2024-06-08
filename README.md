# Git Credential Manager 👨‍💻

![Git Credential Manager](https://img.shields.io/badge/Git%20Credential%20Manager-v2.0-red)

![Git Credential Manager](https://github.com/tilltmk/git-user-manager/blob/main/screenshots/screenshot-v2.png)

## 📜 Description

The **Git Credential Manager** is a Python-based graphical user interface (GUI) application that leverages `customtkinter` to help users manage Git credentials and repositories with ease. With features to add, edit, delete credentials, and configure repositories, it simplifies the process of juggling multiple Git accounts.

## 📝 Features

- **Add Credentials**: Easily add new Git credentials.
- **Edit Credentials**: Modify existing Git credentials.
- **Delete Credentials**: Remove Git credentials you no longer need.
- **Manage Repositories**: Configure repositories with selected credentials.
- **Dark Mode UI**: A sleek dark mode for better visual comfort.

## 📂 File Structure

```
git-user-manager/
│
├── git_user_manager.py   # Main application file
├── credentials.json      # JSON file to store credentials (auto-generated)
├── GitUserManager.desktop   # Desktop entry file
├── icon.png              # Application icon
├── install.sh            # Installation script
└── README.md             # This readme file
```

## 🚀 Getting Started

### Prerequisites

Ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

### Installation

1. **Clone the Repository**:
    ```shell
    git clone https://github.com/tilltmk/git-user-manager.git
    cd git-user-manager
    ```

2. **Install Required Packages**:
    ```shell
    pip install customtkinter
    ```

3. **Package the Application**:
    ```shell
    pyinstaller --onefile --name GitUserManager --icon=icon.png git_user_manager.py
    ```

4. **Run the Installation Script**:
    ```shell
    chmod +x install.sh
    ./install.sh
    ```

### Linux Installation

#### Debian/Ubuntu

```shell
sudo apt update
sudo apt install python3 python3-pip
pip3 install customtkinter
```

#### Arch Linux

```shell
sudo pacman -Syu
sudo pacman -S python python-pip
pip install customtkinter
```

#### Fedora

```shell
sudo dnf update
sudo dnf install python3 python3-pip
pip3 install customtkinter
```

#### OpenSUSE

```shell
sudo zypper refresh
sudo zypper install python3 python3-pip
pip3 install customtkinter
```

You can start the application by running:
```shell
python git_user_manager.py
```

## 🖥️ Usage

1. **Add New Credential**:
    - Click the `Add` button.
    - Fill in the username, password, and remote URL.
    - Click `Submit`.

2. **Edit Credential**:
    - Select a credential by clicking the checkbox next to it.
    - Click the `Edit` button.
    - Modify the fields as needed.
    - Click `Submit`.

3. **Delete Credential**:
    - Select the credential(s) you wish to delete.
    - Click the `Delete` button.

4. **Manage Repositories**:
    - Select the credential(s) you wish to use.
    - Click the `Manage Repos` button.
    - Enter the repository path and submit.

    The repository will be configured with the selected credentials, including username, email, and remote URL.

## 🛠️ Methods Overview

### `AddCredentialDialog`
- A dialog window for adding a new Git credential.

### `RepoPathDialog`
- A dialog window for entering the repository path.

### `GitCredentialManager`
- The main application window for managing credentials and repositories.

## 🧑‍💻 Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## 📜 License

This project is licensed under the GNU GPL v3 License.

## Special Thanks

Special Thanks to Wil Nichols via Iconspedia:
https://www.iconspedia.com/icon/user-black-folder-icon-36035.html

---

Happy managing your Git credentials! ✨
