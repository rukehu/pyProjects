@echo off

echo Convert *.ui ...
.\venv\Scripts\pyside2-uic.exe ui\designer\controlwidget.ui -o ui\designer\UI_controlwidget.py
.\venv\Scripts\pyside2-uic.exe ui\designer\infowidget.ui -o ui\designer\UI_infowidget.py
.\venv\Scripts\pyside2-uic.exe ui\designer\tablewidget.ui -o ui\designer\UI_tablewidget.py
.\venv\Scripts\pyside2-uic.exe ui\designer\TerminalWidget.ui -o ui\designer\UI_TerminalWidget.py