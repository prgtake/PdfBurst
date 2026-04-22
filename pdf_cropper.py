# =====================================================
#  PdfCrop (v1.0.0)
#  Copyright (c) 2026 Datan (データン)
#  Licensed under the MIT License.
#  (See LICENSE file for details)
# =====================================================

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import fitz  # PyMuPDF
from PIL import Image, ImageTk
import os
import datetime
import sys

# =====================================================
#  アプリのバージョン定義 
# =====================================================
APP_VERSION = "1.0.0"

# =====================================================
#  ディレクトリ設定（EXE化対応）
# =====================================================
if getattr(sys, 'frozen', False):
    # EXEとして実行されている場合（EXEファイルがある場所）
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # 通常のスクリプトとして実行されている場合
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class PdfCropperApp:
    def __init__(self, root):
        self.root = root
        # タイトルバーにアプリ名とバージョンを表示するように修正
        self.root.title(f"PdfCrop (v{APP_VERSION})")
        self.root.geometry("1000x800")

        # --- 状態管理変数 ---
        self.doc = None          # 開いているPDFドキュメント
        self.current_page = 0    # 現在表示中のページ
        
        # ★画質維持のための分離管理
        self.render_zoom = 2.0   # 保存用の高画質レンダリング倍率（固定）
        self.display_scale = 1.0 # 画面表示用の倍率（1.0 = 100%）
        
        self.base_pil_image = None # レンダリングされた高画質Pillow画像
        self.tk_image = None       # Canvas表示用のリサイズ済みImageTkオブジェクト
        
        # ドラッグ操作用
        self.start_x = None
        self.start_y = None
        self.rect_id = None      # Canvas上の矩形オブジェクトのID
        self._status_timer = None # ステータスメッセージ消去用タイマー

        # --- UI部品の配置 ---
        # 上部操作パネル
        toolbar = tk.Frame(root, bd=1, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        tk.Button(toolbar, text="PDFを開く", command=self.open_pdf, bg="#3d7ebf", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(toolbar, text="◀ 前", command=self.prev_page).pack(side=tk.LEFT, padx=5)
        self.page_label = tk.Label(toolbar, text="ページ: 0/0")
        self.page_label.pack(side=tk.LEFT, padx=5)
        tk.Button(toolbar, text="次 ▶", command=self.next_page).pack(side=tk.LEFT, padx=5)
        
        # ★表示倍率の変更 UI
        tk.Label(toolbar, text="表示倍率:").pack(side=tk.LEFT, padx=(20, 2))
        self.zoom_var = tk.StringVar(value="100%")
        zoom_cb = ttk.Combobox(toolbar, textvariable=self.zoom_var, values=["50%", "75%", "100%", "125%", "150%", "200%"], width=5, state="readonly")
        zoom_cb.pack(side=tk.LEFT)
        zoom_cb.bind("<<ComboboxSelected>>", self.on_zoom_change)

        # ★自動保存モード UI
        self.auto_save_var = tk.BooleanVar(value=False)
        tk.Checkbutton(toolbar, text="連続自動保存（ダイアログなし）", variable=self.auto_save_var, fg="#a00").pack(side=tk.LEFT, padx=(20, 5))

        # ★通知メッセージ用ラベル
        self.status_label = tk.Label(toolbar, text="", fg="blue", font=("", 10, "bold"))
        self.status_label.pack(side=tk.LEFT, padx=10)

        # 画像表示エリア（スクロール付き）
        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, bg="gray", cursor="crosshair")
        
        # スクロールバー
        v_scroll = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        h_scroll = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        # 配置
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # --- マウスイベントのバインド ---
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)   # クリック
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)      # ドラッグ中
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)  # 離す

    def open_pdf(self):
        filename = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not filename:
            return

        try:
            self.doc = fitz.open(filename)
            self.current_page = 0
            self.show_page()
        except Exception as e:
            messagebox.showerror("エラー", f"PDFを開けませんでした:\n{e}")

    def on_zoom_change(self, event=None):
        """表示倍率が変更された時の処理"""
        val_str = self.zoom_var.get().replace("%", "")
        try:
            self.display_scale = int(val_str) / 100.0
            self.show_page()  # 画像を再描画
        except ValueError:
            pass

    def show_page(self):
        if not self.doc:
            return

        # ページ情報を更新
        total_pages = len(self.doc)
        self.page_label.config(text=f"ページ: {self.current_page + 1}/{total_pages}")

        # PDFページを画像（Pixmap）に変換（常にrender_zoom=2.0で高画質に取得）
        page = self.doc.load_page(self.current_page)
        mat = fitz.Matrix(self.render_zoom, self.render_zoom)
        pix = page.get_pixmap(matrix=mat)

        # PixmapをPillow Imageに変換（高画質ベース画像）
        img_mode = "RGBA" if pix.alpha else "RGB"
        self.base_pil_image = Image.frombytes(img_mode, [pix.width, pix.height], pix.samples)
        if self.base_pil_image.mode == "RGBA":
             self.base_pil_image = self.base_pil_image.convert("RGB") # JPG保存のためにRGBに変換

        # ★画面表示用にリサイズ（表示倍率を適用）
        disp_w = int(self.base_pil_image.width * (self.display_scale / self.render_zoom))
        disp_h = int(self.base_pil_image.height * (self.display_scale / self.render_zoom))
        
        resized_img = self.base_pil_image.resize((disp_w, disp_h), Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(resized_img)

        self.canvas.delete("all") 
        self.canvas.create_image(0, 0, image=self.tk_image, anchor=tk.NW)
        self.canvas.config(scrollregion=(0, 0, disp_w, disp_h))
        self.rect_id = None

    def next_page(self):
        if self.doc and self.current_page < len(self.doc) - 1:
            self.current_page += 1
            self.show_page()

    def prev_page(self):
        if self.doc and self.current_page > 0:
            self.current_page -= 1
            self.show_page()

    def show_status(self, msg, color="blue"):
        """ステータスメッセージを一時的に表示する"""
        self.status_label.config(text=msg, fg=color)
        if self._status_timer:
            self.root.after_cancel(self._status_timer)
        self._status_timer = self.root.after(3000, lambda: self.status_label.config(text=""))

    def _get_canvas_coords(self, event):
        return self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)

    def on_mouse_down(self, event):
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        self.start_x, self.start_y = self._get_canvas_coords(event)
        
        self.rect_id = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline="red", width=2, dash=(4, 4)
        )

    def on_mouse_drag(self, event):
        if not self.start_x: return
        cur_x, cur_y = self._get_canvas_coords(event)
        self.canvas.coords(self.rect_id, self.start_x, self.start_y, cur_x, cur_y)

    def on_mouse_up(self, event):
        if not self.start_x: return
        end_x, end_y = self._get_canvas_coords(event)
        
        x1, y1 = min(self.start_x, end_x), min(self.start_y, end_y)
        x2, y2 = max(self.start_x, end_x), max(self.start_y, end_y)

        if x2 - x1 < 10 or y2 - y1 < 10:
            self.canvas.delete(self.rect_id)
            self.rect_id = None
            return

        ratio = self.render_zoom / self.display_scale
        real_x1 = int(x1 * ratio)
        real_y1 = int(y1 * ratio)
        real_x2 = int(x2 * ratio)
        real_y2 = int(y2 * ratio)

        if self.auto_save_var.get():
            self.auto_save_crop(real_x1, real_y1, real_x2, real_y2)
        else:
            if messagebox.askyesno("確認", "この範囲を図としてJPGで保存しますか？"):
                self.crop_and_save(real_x1, real_y1, real_x2, real_y2)
            else:
                self.canvas.delete(self.rect_id)
                self.rect_id = None

        self.start_x = None
        self.start_y = None

    def auto_save_crop(self, x1, y1, x2, y2):
        if not self.base_pil_image: return
        crop_box = (x1, y1, x2, y2)
        try:
            cropped_img = self.base_pil_image.crop(crop_box)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"crop_p{self.current_page+1}_{timestamp}.jpg"
            save_path = os.path.join(BASE_DIR, filename)
            cropped_img.save(save_path, "JPEG", quality=95)
            self.show_status(f"✔ 自動保存: {filename}")
        except Exception as e:
            self.show_status(f"エラー: 保存失敗", color="red")
        finally:
            self.canvas.delete(self.rect_id)
            self.rect_id = None

    def crop_and_save(self, x1, y1, x2, y2):
        if not self.base_pil_image: return
        crop_box = (x1, y1, x2, y2)
        try:
            cropped_img = self.base_pil_image.crop(crop_box)
            save_filename = filedialog.asksaveasfilename(
                defaultextension=".jpg",
                filetypes=[("JPEG Files", "*.jpg")],
                title="図を保存",
                initialdir=BASE_DIR,
                initialfile=f"crop_p{self.current_page+1}.jpg"
            )
            if save_filename:
                cropped_img.save(save_filename, "JPEG", quality=95)
                self.show_status(f"✔ 保存しました: {os.path.basename(save_filename)}")
        except Exception as e:
            messagebox.showerror("エラー", f"保存に失敗しました:\n{e}")
        finally:
            self.canvas.delete(self.rect_id)
            self.rect_id = None

if __name__ == "__main__":
    root = tk.Tk()
    app = PdfCropperApp(root)
    root.mainloop()