# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path

block_cipher = None

a = Analysis(
    ['main_react.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('app', 'app'),
        ('frontend/dist', 'frontend/dist'),
        ('assets', 'assets'),
    ],
    hiddenimports=[
        'pyzipper',
        'flask',
        'flask_cors',
        'webview',
        'win32com',
        'win32com.client',
        'pythoncom',
        'win32api',
        'win32gui',
        'win32con'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='SORTIFY',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets\\logo.ico'],
    version='file_version_info.txt',
    manifest='app_manifest.xml',
)
