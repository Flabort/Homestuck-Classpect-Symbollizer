# Classpect Symbollizer

A tool to quickly generate classpect symbols from the official class symbol spokes provided by AH.

## Link to Download precompiled:

Version 1.0: [Google Drive zip link](https://drive.google.com/file/d/1uxXPTvoMbD1Tv2Mh77sfkqP08g2scAqA/view?usp=sharing)
Note: Windows Defender may false flag part of the PyInstaller package used and suggested by NiceGui as a trojan. I don't know why, but I hope that gets fixed by the PyInstaller devs

## Installation from source

1. Download the source
2. Unzip the source somewhere
3. Open a terminal in the folder where you unzipped the source
4. Run the commands in one of these two code blocks:

```
python -m venv venv
venv/bin/activate
pip install requirements.txt
```

or

```
python -m venv venv
venv/bin/activate
pip install nicegui
pip install pillow
pip install pyinstaller  // optional
```

5. While the venv is still activated, run either

```
nicegui-pack --onefile --clean --name "Classpect Symbolizer" wheel.py
mv './dist/Classpect Symbolizer.exe' ./
```

or

```
python wheel.py
```

Note: the first method requires PyInstaller, so either the requirements.txt or the third `pip install` iin the 2nd method from step 4 is required to perform `nicegui-pack`.

6. If you ran the first method in step 5, open the exe file; make sure it's in the same folder as the images/ folder, as it looks for the images in a relative path. If you used the second method, the program should already be running.

# Changelog:

V 1.0 (Aug 19, 2026): Release
