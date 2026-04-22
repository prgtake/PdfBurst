# PdfCrop (v1.0.0)

PdfCropは、PDFファイルから特定の範囲を選択して高画質な画像（JPEG）として切り出すためのデスクトップアプリケーションです。直感的なGUI操作で、論文や資料から図表を素早く抽出することに特化しています。

## 特徴

- **高画質レンダリング**: 内部で高倍率レンダリング（2.0倍）を行うため、切り出した画像がボケにくく鮮明です。
- **自由な範囲選択**: マウスドラッグで保存したい範囲を自由に指定できます。
- **連続自動保存モード**: 「保存ダイアログ」をスキップして、クリック＆ドラッグだけで次々と保存できる効率的なモードを搭載しています。
- **ズーム表示**: 画面上での表示倍率（50%〜200%）を変更でき、細かい図表も正確に選択可能です。
- **スクロール対応**: 大きなページでもスクロールバーで全体を確認できます。

## セットアップ

### 必要条件

- Python 3.8 以上
- 以下のライブラリが必要です：
  - `PyMuPDF` (fitz)
  - `Pillow` (PIL)
  - `tkinter` (通常はPythonに標準搭載されています)

### インストール方法

1. リポジトリをクローンまたはダウンロードします。
2. 必要なライブラリをインストールします：

```bash
pip install pymupdf pillow
```

## 使い方

1. アプリを起動します：
   ```bash
   python pdf_cropper.py
   ```
2. **「PDFを開く」**ボタンをクリックし、対象のPDFファイルを選択します。
3. 必要に応じて**「前」「次」**ボタンでページを移動したり、**「表示倍率」**を調整したりします。
4. PDF上の保存したい範囲を**マウスでドラッグ**して囲みます。
   - **通常モード**: ドラッグを離すと保存確認ダイアログが表示されます。
   - **連続自動保存モード**: チェックを入れている場合、ドラッグを離した瞬間に実行ファイルと同じディレクトリに自動で保存されます。
5. 保存された画像は、指定した場所（またはアプリと同じフォルダ）にJPEG形式で出力されます。

## ライセンス

このプロジェクトは MIT ライセンス の元で公開されています。
Copyright (c) 2026 Datan (データン)

---

# PdfCrop (v1.0.0)

PdfCrop is a desktop application designed to crop specific areas from PDF files and save them as high-quality JPEG images. With its intuitive GUI, it is specifically tailored for quickly extracting figures and tables from research papers and documents.

## Features

- **High-Quality Rendering**: Uses internal high-resolution rendering (2.0x zoom) to ensure cropped images are sharp and clear.
- **Free-Form Selection**: Easily select the area you want to save by clicking and dragging your mouse.
- **Continuous Auto-Save Mode**: Includes an efficient mode that skips the "Save As" dialog, allowing you to save multiple crops rapidly with just a drag-and-release action.
- **Zoom Display**: Adjust the on-screen display scale (from 50% to 200%) to precisely select small details.
- **Scroll Support**: Handles large pages with scrollbars to ensure you can view the entire document.

## Setup

### Prerequisites

- Python 3.8 or higher
- The following libraries are required:
  - `PyMuPDF` (fitz)
  - `Pillow` (PIL)
  - `tkinter` (Usually included with Python)

### Installation

1. Clone or download the repository.
2. Install the required libraries:

```bash
pip install pymupdf pillow
```

## Usage

1. Launch the application:
   ```bash
   python pdf_cropper.py
   ```
2. Click the **"Open PDF"** button and select your target PDF file.
3. Use the **"Prev"** and **"Next"** buttons to navigate through pages, and adjust the **"Zoom"** level if necessary.
4. **Drag your mouse** over the area of the PDF you want to save.
   - **Normal Mode**: A confirmation dialog will appear when you release the mouse.
   - **Continuous Auto-Save Mode**: If checked, the image will be saved automatically to the application's directory as soon as you release the mouse.
5. Cropped images are saved as JPEG files in your chosen location (or the application's folder).

## License

This project is licensed under the MIT License.
Copyright (c) 2026 Datan (データン)
