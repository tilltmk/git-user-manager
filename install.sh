#!/bin/bash

# Zielpfade definieren
BINARY_PATH="$HOME/.local/share/applications/GitUserManager"
DESKTOP_FILE_PATH="$HOME/.local/share/applications/GitUserManager.desktop"
ICON_PATH="$HOME/.local/share/applications/icon.png"

# Erstellen des Verzeichnisses, falls es nicht existiert
mkdir -p "$(dirname "$BINARY_PATH")"

# Kopieren der Binary, der Desktop-Datei und des Icons
cp "dist/GitUserManager" "$BINARY_PATH"
cp "GitUserManager.desktop" "$DESKTOP_FILE_PATH"
cp "icon.png" "$ICON_PATH"

# Datei ausführbar machen
chmod +x "$BINARY_PATH"
chmod +x "$DESKTOP_FILE_PATH"

echo "Installation abgeschlossen!"
