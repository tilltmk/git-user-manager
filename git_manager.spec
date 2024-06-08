# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['git_user_manager.py'],
    pathex=[],
    binaries=[],
    datas=[('icon.png', '.')],
    hiddenimports=['keyring.backends.Windows', 'keyring.backends.macOS', 'keyring.backends.SecretService'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='GitManager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon='icon.png',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='GitManager'
)
