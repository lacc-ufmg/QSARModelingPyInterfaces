# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['GUI/main.py'],
             pathex=[os.path.dirname(os.path.realpath('__file__'))],
             binaries=[],
             datas=[('./GUI/Views/main.glade', 'Views'), ('./GUI/Views/main.glade', 'Views'), ('./GUI/Views/ga.glade', 'Views'), ('./GUI/Views/ops.glade', 'Views'), ('./GUI/Views/about.glade', 'Views'), ('./GUI/Views/varcut.glade', 'Views'), ('./GUI/Views/corrcut.glade', 'Views'), ('./GUI/Views/autocorrcut.glade', 'Views'), ('./GUI/Views/cross_validation.glade', 'Views'), ('./GUI/Views/yrlno.glade', 'Views'), ('./GUI/Views/external_validation.glade', 'Views')],
             hiddenimports=['cmath', 'sklearn.utils._weight_vector', 'pandas'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='qsarmodeling',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='qsarmodeling')
