@echo off
echo [PdfBurst Build Script]
echo 必要なライブラリの確認中...
pip install --upgrade pymupdf pillow pyinstaller pyinstaller-hooks-contrib

echo.
echo ビルドを開始します (onefile, noconsole)...
pyinstaller --onefile --noconsole --name PdfBurst --exclude-module pytest pdf_burst.py

echo.
echo ビルドが完了しました。
echo 'dist' フォルダ内に PdfBurst.exe が生成されています。
pause
