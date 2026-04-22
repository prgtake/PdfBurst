@echo off
echo [PdfCrop Build Script]
echo 必要なライブラリの確認中...
pip install pymupdf pillow pyinstaller

echo.
echo ビルドを開始します (onefile, noconsole)...
pyinstaller --onefile --noconsole --name PdfCrop pdf_cropper.py

echo.
echo ビルドが完了しました。
echo 'dist' フォルダ内に PdfCrop.exe が生成されています。
pause
