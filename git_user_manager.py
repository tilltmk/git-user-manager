import customtkinter as ctk
import os
import json
import subprocess
from tkinter import messagebox

class AddCredentialDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add Credential")
        self.geometry("400x400")
        self.configure(fg_color="#444444")  # Ansprechenderes Schwarz
        
        self.username_label = ctk.CTkLabel(self, text="Enter username:", text_color="white")
        self.username_label.pack(pady=5)
        
        self.username_entry = ctk.CTkEntry(self, width=250)
        self.username_entry.pack(pady=5)
        
        self.password_label = ctk.CTkLabel(self, text="Enter password:", text_color="white")
        self.password_label.pack(pady=5)
        
        self.password_entry = ctk.CTkEntry(self, show="*", width=250)
        self.password_entry.pack(pady=5)
        
        self.url_label = ctk.CTkLabel(self, text="Enter remote URL:", text_color="white")
        self.url_label.pack(pady=5)
        
        self.url_entry = ctk.CTkEntry(self, width=250)
        self.url_entry.pack(pady=5)
        
        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.on_submit)
        self.submit_button.pack(pady=20)

        self.username = None
        self.password = None
        self.url = None

    def on_submit(self):
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()
        self.url = self.url_entry.get()
        self.destroy()

class RepoPathDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Enter Repository Path")
        self.geometry("400x150")
        self.configure(fg_color="#444444")  # Ansprechenderes Schwarz

        self.path_label = ctk.CTkLabel(self, text="Enter repository path:", text_color="white")
        self.path_label.pack(pady=5)
        
        self.path_entry = ctk.CTkEntry(self, width=250)
        self.path_entry.pack(pady=5)
        
        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.on_submit)
        self.submit_button.pack(pady=20)

        self.path = None

    def on_submit(self):
        self.path = self.path_entry.get()
        self.destroy()

class GitCredentialManager(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Git Credential Manager")
        self.geometry("800x700")

        # Colors and Theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Load credentials and repos
        self.credentials = self.load_credentials()
        self.repos = self.load_repositories()
        self.selected_credentials = []

        # Main Frame
        self.main_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#444444")  # Ansprechenderes Schwarz
        self.main_frame.pack(pady=20, padx=20, expand=True, fill="both")

        self.title_label = ctk.CTkLabel(self.main_frame, text="Git Credential Manager", font=("", 24), text_color="white")
        self.title_label.pack(pady=20)

        # Credential Frame
        self.credential_frame_title = ctk.CTkLabel(self.main_frame, text="Credentials", font=("", 20), text_color="white")
        self.credential_frame_title.pack(pady=(10, 5))
        
        self.credential_frame = ctk.CTkFrame(self.main_frame, corner_radius=15, fg_color="#444444")
        self.credential_frame.pack(pady=(5, 20), expand=True, fill="both")

        # Repository Textbox
        self.repo_textbox_title = ctk.CTkLabel(self.main_frame, text="Repositories", font=("", 20), text_color="white")
        self.repo_textbox_title.pack(pady=(10, 5))
        
        self.repo_textbox = ctk.CTkTextbox(self.main_frame, width=80, height=10)
        self.repo_textbox.pack(pady=(5, 20), expand=True, fill="both")
        self.repo_textbox.configure(state="disabled")

        # Output Textbox
        self.output_textbox_title = ctk.CTkLabel(self.main_frame, text="Output", font=("", 20), text_color="white")
        self.output_textbox_title.pack(pady=(20, 5))
        
        self.output_textbox = ctk.CTkTextbox(self.main_frame, width=80, height=10)
        self.output_textbox.pack(pady=(5, 20), expand=True, fill="both")
        self.output_textbox.configure(state="disabled")

        self.update_credential_frame()
        self.update_repo_textbox()

        # Buttons with padding
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="#444444")
        self.button_frame.pack(pady=20)

        self.add_button = ctk.CTkButton(self.button_frame, text="Add", command=self.add_credential, width=100)
        self.add_button.pack(side="left", padx=10)

        self.edit_button = ctk.CTkButton(self.button_frame, text="Edit", command=self.edit_credential, width=100)
        self.edit_button.pack(side="left", padx=10)

        self.delete_button = ctk.CTkButton(self.button_frame, text="Delete", command=self.delete_credential, width=100)
        self.delete_button.pack(side="left", padx=10)

        self.manage_repos_button = ctk.CTkButton(self.button_frame, text="Manage Repos", command=self.manage_repos, width=150)
        self.manage_repos_button.pack(side="left", padx=10)

    def load_credentials(self):
        if os.path.exists("credentials.json"):
            with open("credentials.json", "r") as file:
                return json.load(file)
        else:
            return []

    def save_credentials(self):
        with open("credentials.json", "w") as file:
            json.dump(self.credentials, file)

    def load_repositories(self):
        repos = []
        home_dir = os.path.expanduser("~")
        for root, dirs, files in os.walk(home_dir):
            if ".git" in dirs:
                repos.append(root)
        return repos

    def update_credential_frame(self):
        for widget in self.credential_frame.winfo_children():
            widget.destroy()

        self.selected_credentials.clear()
        for index, credential in enumerate(self.credentials):
            var = ctk.StringVar(value=credential.get("url", ""))
            checkbox = ctk.CTkCheckBox(
                self.credential_frame,
                text=f"{credential['username']} ({credential['url']})",
                variable=var, 
                onvalue=credential['url'],
                offvalue="", 
                fg_color="#444444",  # Corrected here
                text_color="white"
            )
            checkbox.grid(row=index, column=0, sticky="w", padx=20, pady=5)
            self.selected_credentials.append(checkbox)

    def update_repo_textbox(self):
        self.repo_textbox.configure(state="normal")
        self.repo_textbox.delete(1.0, ctk.END)
        for repo in self.repos:
            self.repo_textbox.insert(ctk.END, f"{repo}\n")  # Removed numbering
        self.repo_textbox.configure(state="disabled")

    def add_credential(self):
        dialog = AddCredentialDialog(self)
        self.wait_window(dialog)

        username = dialog.username
        password = dialog.password
        url = dialog.url

        if username and password and url:
            self.credentials.append({"username": username, "password": password, "url": url})
            self.save_credentials()
            self.update_credential_frame()
        else:
            messagebox.showerror("Error", "Username, password, and remote URL cannot be empty.")

    def edit_credential(self):
        selected_indices = [i for i, checkbox in enumerate(self.selected_credentials) if checkbox.get()]

        if not selected_indices:
            messagebox.showwarning("Warning", "No credential selected to edit.")
            return

        index = selected_indices[0]
        self.selected_credential = self.credentials[index]

        if self.selected_credential:
            dialog = AddCredentialDialog(self)
            dialog.username_entry.insert(0, self.selected_credential["username"])
            dialog.password_entry.insert(0, self.selected_credential["password"])
            dialog.url_entry.insert(0, self.selected_credential["url"])
            self.wait_window(dialog)

            username = dialog.username
            password = dialog.password
            url = dialog.url

            if username and password:
                self.selected_credential["username"] = username
                self.selected_credential["password"] = password
                self.selected_credential["url"] = url
                self.save_credentials()
                self.update_credential_frame()
            else:
                messagebox.showerror("Error", "Username, password, and remote URL cannot be empty.")
        else:
            messagebox.showerror("Error", "No credential selected.")

    def delete_credential(self):
        selected_indices = [i for i, checkbox in enumerate(self.selected_credentials) if checkbox.get()]

        if not selected_indices:
            messagebox.showwarning("Warning", "No credential selected to delete.")
            return

        for index in selected_indices:
            del self.credentials[index]

        self.save_credentials()
        self.update_credential_frame()

    def manage_repos(self):
        selected_indices = [i for i, checkbox in enumerate(self.selected_credentials) if checkbox.get()]

        if not selected_indices:
            messagebox.showwarning("Warning", "No credential selected to manage repositories.")
            return

        dialog = RepoPathDialog(self)
        self.wait_window(dialog)

        repo_path = dialog.path

        if not repo_path or not os.path.isdir(repo_path):
            messagebox.showerror("Error", "Invalid repository path.")
            return

        self.output_textbox.configure(state="normal")
        self.output_textbox.delete(1.0, ctk.END)

        for index in selected_indices:
            selected_credential = self.credentials[index]
            try:
                # Check if the directory is already a Git repository
                if not os.path.isdir(os.path.join(repo_path, ".git")):
                    init_result = subprocess.run(["git", "init"], cwd=repo_path, check=True, capture_output=True, text=True)
                    self.output_textbox.insert(ctk.END, init_result.stdout + '\n')

                config_name_result = subprocess.run(["git", "config", "--local", "user.name", selected_credential["username"]], cwd=repo_path, check=True, capture_output=True, text=True)
                self.output_textbox.insert(ctk.END, config_name_result.stdout + '\n')

                config_email_result = subprocess.run(["git", "config", "--local", "user.email", f"{selected_credential['username']}@example.com"], cwd=repo_path, check=True, capture_output=True, text=True)
                self.output_textbox.insert(ctk.END, config_email_result.stdout + '\n')

                remote_result = subprocess.run(["git", "remote", "add", "origin", selected_credential["url"]], cwd=repo_path, check=True, capture_output=True, text=True)
                self.output_textbox.insert(ctk.END, remote_result.stdout + '\n')

                self.output_textbox.insert(ctk.END, "Repository configured successfully.\n")
            except subprocess.CalledProcessError as e:
                self.output_textbox.insert(ctk.END, "Error: " + e.stderr + '\n')

        self.output_textbox.configure(state="disabled")

if __name__ == "__main__":
    app = GitCredentialManager()
    app.mainloop()
