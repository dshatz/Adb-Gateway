# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['adbgateway/adbgateway.py'],
    pathex=[],
    binaries=[],
    datas=[('adbgateway/default.cfg', 'adbgateway')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='adbgateway',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    version='file_info.txt',
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
