from cx_Freeze import setup, Executable

setup(
    name="Virtual Pet",
    version="1.0",
    description="Virtual Pet Desktop Application",
    options={
        "build_exe": {
            "includes": ["atexit", "PyQt5.QtCore", "PyQt5.QtGui", "PyQt5.QtWidgets"],
            "include_files": ["assets", "icon.ico"],
            "build_exe": "build_cxfreeze"
        }
    },
    executables=[Executable("main.py", base="Win32GUI", icon="icon.ico")]
)
