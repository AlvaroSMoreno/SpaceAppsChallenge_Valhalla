# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['space.py'],
             pathex=['C:\\Users\\Usuario\\Desktop\\spaceapps\\game'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
a.datas += [("./res/tomar.gif", "res/tomar.gif", "DATA")]
a.datas += [("./res/earth.gif", "res/earth.gif", "DATA")]
a.datas += [("./res/sun.gif", "res/sun.gif", "DATA")]
a.datas += [("./res/sat1.gif", "res/sat1.gif", "DATA")]
a.datas += [("./res/bip2.wav", "res/bip2.wav", "DATA")]
a.datas += [("./res/win.wav", "res/win.wav", "DATA")]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='space',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
