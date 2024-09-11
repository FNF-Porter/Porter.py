# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
	['psychtobase\\main.py'],
	pathex=[],
	binaries=[],
	datas=[],
	hiddenimports=[],
	hookspath=[],
	hooksconfig={},
	runtime_hooks=[],
	excludes=[],
	noarchive=False,
	# optimize=0, Crashes for some reason :shrug:
)
pyz = PYZ(a.pure)

import platform
iconArr = []

if platform.system() == 'Darwin':
	iconArr = ['icon.icns']
elif platform.system() == 'Windows':
	iconArr = ['icon.ico']

exe = EXE(
	pyz,
	a.scripts,
	a.binaries,
	a.datas,
	[],
	name='FNF Porter',
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
	icon=iconArr,
)

import shutil
if platform.system() == 'Windows':
	shutil.copyfile('ffmpeg.exe', '{0}/ffmpeg.exe'.format(DISTPATH))
	shutil.copyfile('FFMPEG-LICENSE', '{0}/FFMPEG_LICENSE.txt'.format(DISTPATH))