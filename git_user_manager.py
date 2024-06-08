import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import os
import subprocess
import keyring
from keyrings.alt.file import PlaintextKeyring
import sys
import threading

SSH_ENABLED = False

# Set the keyring to PlaintextKeyring
keyring.set_keyring(PlaintextKeyring())

class GitManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.title("Git Manager")
        self.geometry("800x600")

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.label = ctk.CTkLabel(self.main_frame, text="Git Manager", font=("Arial", 24))
        self.label.pack(pady=20)

        # Menu Section
        self.menu_frame = ctk.CTkFrame(self.main_frame)
        self.menu_frame.pack(fill="x", pady=10)

        self.add_repo_button = ctk.CTkButton(self.menu_frame, text="Add Repository", command=self.open_add_repo_window)
        self.add_repo_button.pack(side="left", padx=2)

        self.settings_button = ctk.CTkButton(self.menu_frame, text="Settings", command=self.open_settings_window)
        self.settings_button.pack(side="left", padx=2)
        
        self.init_button = ctk.CTkButton(self.menu_frame, text="Initialize", command=self.git_init_and_pull)
        self.init_button.pack(side="left", padx=2)

        self.sync_button = ctk.CTkButton(self.menu_frame, text="Sync", command=self.git_sync)
        self.sync_button.pack(side="left", padx=2)

        self.delete_button = ctk.CTkButton(self.menu_frame, text="Delete Selected", command=self.delete_selected_repos)
        self.delete_button.pack(side="left", padx=2)

        # Repository List Section
        self.listbox_frame = ctk.CTkFrame(self.main_frame)
        self.listbox_frame.pack(fill="both", expand=True)

        self.repo_listbox = tk.Listbox(self.listbox_frame, selectmode=tk.SINGLE, font=("Arial", 12), bg="#2b2b2b", fg="white", selectbackground="#4a4a4a", selectforeground="white")
        self.repo_listbox.pack(side="left", fill="both", expand=True)

        self.scrollbar = ctk.CTkScrollbar(self.listbox_frame, orientation="vertical", command=self.repo_listbox.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.repo_listbox.configure(yscrollcommand=self.scrollbar.set)

        # Terminal Section
        self.terminal_frame = ctk.CTkFrame(self.main_frame)
        self.terminal_frame.pack(fill="both", expand=True)

        self.terminal_label = ctk.CTkLabel(self.terminal_frame, text="Terminal Output", font=("Arial", 12))
        self.terminal_label.pack(pady=5)

        self.terminal_output = ctk.CTkTextbox(self.terminal_frame, font=("Courier", 12))
        self.terminal_output.configure(fg_color="#1e1e1e", text_color="white")
        self.terminal_output.pack(fill="both", expand=True)

        self.conflict_resolution_var = tk.IntVar(value=1)
        self.conflict_resolution_checkbox = ctk.CTkCheckBox(self.main_frame, text="Auto-resolve conflicts by keeping newer and larger files", variable=self.conflict_resolution_var)
        self.conflict_resolution_checkbox.pack(pady=5)

        self.load_repos()
        self.load_settings()

    def open_add_repo_window(self):
        add_repo_window = ctk.CTkToplevel(self)
        add_repo_window.title("Add Repository")
        add_repo_window.geometry("400x600")

        dir_label = ctk.CTkLabel(add_repo_window, text="Local Directory")
        dir_label.pack(pady=5)

        dir_entry = ctk.CTkEntry(add_repo_window)
        dir_entry.pack(pady=5)

        repo_label = ctk.CTkLabel(add_repo_window, text="Remote Repository URL")
        repo_label.pack(pady=5)

        repo_entry = ctk.CTkEntry(add_repo_window)
        repo_entry.pack(pady=5)

        branch_label = ctk.CTkLabel(add_repo_window, text="Branch")
        branch_label.pack(pady=5)

        branch_entry = ctk.CTkEntry(add_repo_window)
        branch_entry.pack(pady=5)
        branch_entry.insert(0, "main")  # Default branch

        user_label = ctk.CTkLabel(add_repo_window, text="Username")
        user_label.pack(pady=5)

        user_entry = ctk.CTkEntry(add_repo_window)
        user_entry.pack(pady=5)

        email_label = ctk.CTkLabel(add_repo_window, text="Email")
        email_label.pack(pady=5)

        email_entry = ctk.CTkEntry(add_repo_window)
        email_entry.pack(pady=5)

        pass_label = ctk.CTkLabel(add_repo_window, text="Password")
        pass_label.pack(pady=5)

        pass_entry = ctk.CTkEntry(add_repo_window, show="*")
        pass_entry.pack(pady=5)

        add_button = ctk.CTkButton(add_repo_window, text="Add", command=lambda: self.add_repo(dir_entry.get(), repo_entry.get(), branch_entry.get(), user_entry.get(), email_entry.get(), pass_entry.get(), add_repo_window))
        add_button.pack(pady=10)

    def add_repo(self, local_dir, remote_url, branch, username, email, password, window):
        if local_dir and remote_url and branch and username and email and password:
            keyring.set_password(remote_url, username, password)

            # Initialize the local repository if it does not exist
            if not os.path.exists(os.path.join(local_dir, '.git')):
                init_command = ["git", "init"]
                subprocess.run(init_command, cwd=local_dir)
            
            # Set user information
            self.set_git_user_info(local_dir, username, email)
            
            # Configure the repository with the access credentials
            self.configure_git_credentials(local_dir, remote_url, username, password)
            
            # Check if the remote repository already exists
            remote_check_command = ["git", "remote", "get-url", "origin"]
            result = subprocess.run(remote_check_command, cwd=local_dir, capture_output=True, text=True)
            
            if result.returncode == 0:
                # If the remote already exists, update the URL
                remote_command = ["git", "remote", "set-url", "origin", remote_url]
            else:
                # If the remote does not exist, add the remote repository URL
                remote_command = ["git", "remote", "add", "origin", remote_url]
            
            result = subprocess.run(remote_command, cwd=local_dir, capture_output=True, text=True)
            if result.returncode != 0:
                messagebox.showerror("Error", f"Failed to add or update remote URL:\n{result.stderr}")
                return

            self.repo_listbox.insert("end", f"{local_dir} -> {remote_url} [{branch}]")
            self.save_repo(local_dir, remote_url, branch, username, email)
            window.destroy()
        else:
            messagebox.showerror("Error", "All fields must be filled out")

    def set_git_user_info(self, local_dir, username, email):
        user_name_command = ["git", "config", "user.name", username]
        user_email_command = ["git", "config", "user.email", email]
        
        subprocess.run(user_name_command, cwd=local_dir)
        subprocess.run(user_email_command, cwd=local_dir)

    def configure_git_credentials(self, local_dir, remote_url, username, password):
        # Use credential helper to store credentials
        with open(os.path.join(local_dir, ".git", "config"), "a") as git_config:
            git_config.write(f"""
[credential]
    helper = store
[url "{remote_url}"]
    insteadOf = {remote_url}
""")
        
        # Store the credentials in the git credential store
        creds_command = ["git", "credential", "approve"]
        creds_input = f"url={remote_url.replace('https://', 'https://'+username+':'+password+'@')}\n"
        subprocess.run(creds_command, cwd=local_dir, input=creds_input.encode())

    def save_repo(self, local_dir, remote_url, branch, username, email):
        with open("repos.txt", "a") as file:
            file.write(f"{local_dir},{remote_url},{branch},{username},{email}\n")

    def load_repos(self):
        if os.path.exists("repos.txt"):
            with open("repos.txt", "r") as file:
                for line in file:
                    parts = line.strip().split(",")
                    if len(parts) == 5:
                        local_dir, remote_url, branch, username, email = parts
                        self.repo_listbox.insert("end", f"{local_dir} -> {remote_url} [{branch}]")
                    else:
                        messagebox.showerror("Error", f"Invalid line in repos.txt: {line}")

    def delete_selected_repos(self):
        selected_indices = self.repo_listbox.curselection()
        for index in reversed(selected_indices):
            self.repo_listbox.delete(index)
        self.save_repos_to_file()

    def save_repos_to_file(self):
        with open("repos.txt", "w") as file:
            for i in range(self.repo_listbox.size()):
                line = self.repo_listbox.get(i)
                local_dir, rest = line.split(" -> ")
                remote_url, branch = rest.strip().split(" [")
                branch = branch[:-1]
                username, email = "", ""
                file.write(f"{local_dir},{remote_url},{branch},{username},{email}\n")

    def open_settings_window(self):
        settings_window = ctk.CTkToplevel(self)
        settings_window.title("Settings")
        settings_window.geometry("400x400")

        settings_label = ctk.CTkLabel(settings_window, text="Settings", font=("Arial", 18))
        settings_label.pack(pady=10)

        # Add proxy settings
        proxy_label = ctk.CTkLabel(settings_window, text="Proxy URL")
        proxy_label.pack(pady=5)

        proxy_entry = ctk.CTkEntry(settings_window)
        proxy_entry.pack(pady=5)

        # Add theme settings
        theme_label = ctk.CTkLabel(settings_window, text="Theme")
        theme_label.pack(pady=5)

        theme_menu = ctk.CTkOptionMenu(settings_window, values=["dark", "light"], command=self.set_theme)
        theme_menu.pack(pady=5)

        # Add SSH Key Support setting
        self.ssh_var = tk.IntVar()
        ssh_checkbox = ctk.CTkCheckBox(settings_window, text="Enable SSH Key Support", variable=self.ssh_var, command=self.toggle_ssh_support)
        ssh_checkbox.pack(pady=5)

        save_button = ctk.CTkButton(settings_window, text="Save", command=lambda: self.save_settings(proxy_entry.get(), settings_window))
        save_button.pack(pady=10)

    def set_theme(self, choice):
        if choice == "light":
            ctk.set_appearance_mode(choice)
            ctk.set_default_color_theme("blue")  # Set a light color theme
        else:
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("green")
        
    def toggle_ssh_support(self):
        global SSH_ENABLED
        if self.ssh_var.get() == 1:
            SSH_ENABLED = True
            self.install_ssh_dependencies()
        else:
            SSH_ENABLED = False

    def install_ssh_dependencies(self):
        def install():
            result = subprocess.run([sys.executable, '-m', 'pip', 'install', 'paramiko'], capture_output=True, text=True)
            if result.returncode == 0:
                messagebox.showinfo("SSH Key Support", "Dependencies installed. Please restart the application.")
            else:
                messagebox.showerror("SSH Key Support", f"Failed to install dependencies. Error: {result.stderr}")
        
        threading.Thread(target=install).start()

    def save_settings(self, proxy_url, window):
        with open("settings.txt", "w") as file:
            file.write(f"proxy={proxy_url}\n")
            file.write(f"ssh={self.ssh_var.get()}\n")
        window.destroy()

    def load_settings(self):
        if os.path.exists("settings.txt"):
            with open("settings.txt", "r") as file:
                for line in file:
                    if line.startswith("proxy="):
                        proxy_url = line.strip().split("=")[1]
                        os.environ["HTTP_PROXY"] = proxy_url
                        os.environ["HTTPS_PROXY"] = proxy_url
                    if line.startswith("ssh="):
                        ssh_value = line.strip().split("=")[1]
                        if ssh_value == '1':
                            global SSH_ENABLED
                            SSH_ENABLED = True
                            self.ssh_var.set(1)

    def get_selected_repo_dir(self):
        selected_indices = self.repo_listbox.curselection()
        if not selected_indices:
            messagebox.showerror("Error", "Please select a repository")
            return None
        selected_line = self.repo_listbox.get(selected_indices[0])
        local_dir, rest = selected_line.split(" -> ")
        remote_url, branch = rest.strip().split(" [")
        branch = branch[:-1]
        return local_dir.strip(), remote_url.strip(), branch.strip()

    def git_init_and_pull(self):
        local_dir, remote_url, branch = self.get_selected_repo_dir()
        if local_dir:
            # Initialize if not already initialized
            if not os.path.exists(os.path.join(local_dir, '.git')):
                self.run_git_command("git init", local_dir)
                self.run_git_command(f"git remote add origin {remote_url}", local_dir)
            self.run_git_command(f"git pull origin {branch}", local_dir)

    def git_sync(self):
        local_dir, remote_url, branch = self.get_selected_repo_dir()
        if local_dir:
            self.run_git_command("git add .", local_dir)
            self.run_git_command("git commit -m 'Sync changes'", local_dir)
            self.handle_git_errors(f"git pull origin {branch}", local_dir)
            self.handle_git_errors(f"git push origin {branch}", local_dir)

    def handle_git_errors(self, command, repo_path):
        result = subprocess.run(command, cwd=repo_path, capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            self.terminal_output.insert("end", f"Output:\n{result.stdout}\n")
        else:
            self.terminal_output.insert("end", f"Error:\n{result.stderr}\n")
            self.terminal_output.see("end")
            self.resolve_git_errors(result.stderr, repo_path)

    def resolve_git_errors(self, error_message, repo_path):
        if "fatal: cannot lock ref 'HEAD'" in error_message:
            self.run_git_command("git reset --hard", repo_path)
        elif "error: Fehler beim Versenden einiger Referenzen" in error_message:
            self.run_git_command("git pull --rebase", repo_path)
        elif "fatal: Es muss angegeben werden, wie mit abweichenden Branches umgegangen werden sollen" in error_message:
            self.run_git_command("git config pull.rebase false", repo_path)
            self.run_git_command(f"git pull origin {self.get_selected_repo_dir()[2]}", repo_path)
        elif "fatal: verweigere den Merge von nicht zusammenhängenden Historien" in error_message:
            self.run_git_command(f"git pull origin {self.get_selected_repo_dir()[2]} --allow-unrelated-histories", repo_path)
        elif "error: Src-Refspec main entspricht keiner Referenz" in error_message:
            self.run_git_command(f"git push origin HEAD:{self.get_selected_repo_dir()[2]}", repo_path)
        elif "Merge conflict" in error_message or "CONFLICT" in error_message:
            self.resolve_merge_conflicts(repo_path)
        elif "Es gibt keine Tracking-Informationen für den aktuellen Branch" in error_message:
            self.run_git_command(f"git branch --set-upstream-to=origin/{self.get_selected_repo_dir()[2]} master", repo_path)
            self.run_git_command(f"git pull origin {self.get_selected_repo_dir()[2]}", repo_path)

    def resolve_merge_conflicts(self, repo_path):
        if self.conflict_resolution_var.get() == 1:
            self.run_git_command("git merge --strategy-option=theirs", repo_path)
        else:
            self.run_git_command("git merge --strategy-option=ours", repo_path)

    def run_git_command(self, command, repo_path):
        result = subprocess.run(command, cwd=repo_path, capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            self.terminal_output.insert("end", f"Output:\n{result.stdout}\n")
        else:
            self.terminal_output.insert("end", f"Error:\n{result.stderr}\n")
        self.terminal_output.see("end")

if __name__ == "__main__":
    app = GitManagerApp()
    app.mainloop()
