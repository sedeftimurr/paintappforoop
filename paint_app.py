import tkinter as tk
from tkinter import colorchooser, messagebox, filedialog, ttk
import json
from PIL import Image, ImageGrab, ImageTk
import os

from drawing_tools import OvalBrush, SquareBrush, StarBrush, LineTool, CircleTool, EraserTool
from settings import DrawingSettings, PaintHistory

# İLKE 3: KALITIM (INHERITANCE)
# ============================
# Kalıtım, bir sınıfın başka bir sınıfın özelliklerini 
# ve davranışlarını devralmasını sağlayan bir ilkedir.
# Bu ilke ile:
# - Kod tekrarını azaltırız
# - Hiyerarşik sınıf yapıları oluşturabiliriz
# - Davranış ve özellikleri genişletebiliriz

class PaintApp:
    """
    Temel Paint uygulaması sınıfı.
    
    Bu sınıf, paint uygulamasının temel işlevselliğini içerir.
    Kalıtım hiyerarşisinin üst sınıfıdır.
    """
    def __init__(self, root):
        self._root = root
        self._root.title("Sedef'in Paint Uygulaması")
        self._root.geometry("1080x1000")
        
        # Tema renkleri
        self.theme = {
            "primary": "#6495ED",  # Kornflower Blue
            "primary_light": "#87CEFA",  # Light Sky Blue
            "secondary": "#FFC0CB",  # Pink
            "background": "#F5F5F5",  # Whisper
            "card_bg": "#FFFFFF",  # White
            "text": "#333333",  # Dark Gray
            "accent": "#FF69B4",  # Hot Pink
            "success": "#4CAF50",  # Green
            "warning": "#FFC107",  # Amber
            "error": "#F44336",  # Red
        }
        
        # Uygulama simgesi için kaynak klasörü
        self.icon_path = "icons"
        if not os.path.exists(self.icon_path):
            os.makedirs(self.icon_path)
            
        # Font ayarları
        self.fonts = {
            "header": ("Segoe UI", 12, "bold"),
            "subheader": ("Segoe UI", 10, "bold"),
            "normal": ("Segoe UI", 9),
            "small": ("Segoe UI", 8)
        }
        
        # Ana pencere yapılandırması
        self._root.configure(bg=self.theme["background"])
        
        # Ayarları başlat
        self._settings = DrawingSettings()
        
        # Araç kutusunu oluştur
        self._tools = {
            "oval": OvalBrush(),
            "square": SquareBrush(),
            "star": StarBrush(),
            "line": LineTool(),
            "circle": CircleTool(),
            "eraser": EraserTool()
        }
        self._active_tool = "oval"
        
        # Arayüz elemanlarını oluştur
        self._create_widgets()
        
        # Geçmişi başlat
        self._history = PaintHistory(self._canvas)
        self._history.save_state()
        
        # Çizim olaylarını bağla
        self._setup_drawing_events()
        
        # Kısayol tuşları tanımla
        self._setup_keyboard_shortcuts()
    
    def _create_widgets(self):
        """Arayüz elemanlarını oluşturur"""
        # Ana düzen
        main_frame = tk.Frame(self._root, bg=self.theme["background"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Üst panel - Başlık ve bilgi
        top_panel = tk.Frame(main_frame, bg=self.theme["card_bg"], height=50)
        top_panel.pack(fill=tk.X, pady=(0, 10))
        
        # Başlık
        app_title = tk.Label(
            top_panel, 
            text="✨ Sedef'in Paint Stüdyosu ✨", 
            font=("Segoe UI", 18, "bold"), 
            bg=self.theme["card_bg"],
            fg=self.theme["primary"]
        )
        app_title.pack(pady=10)
        
        # Sol panel - Araçlar (dikey düzende)
        left_panel = tk.Frame(main_frame, bg=self.theme["card_bg"], width=150, bd=0)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10), pady=0)
        
        # Araç başlığı
        tool_label = tk.Label(
            left_panel, 
            text="🖌️ Çizim Araçları", 
            font=self.fonts["header"], 
            bg=self.theme["card_bg"],
            fg=self.theme["text"]
        )
        tool_label.pack(pady=(15, 10))
        
        # Araç butonları
        tools_frame = tk.Frame(left_panel, bg=self.theme["card_bg"], padx=10, pady=5)
        tools_frame.pack(fill=tk.X)
        
        self._tool_buttons = {}
        
        # Araç emojileri
        tool_icons = {
            "oval": "🔵",
            "square": "🟦",
            "star": "⭐",
            "line": "➖",
            "circle": "⭕",
            "eraser": "🧽"
        }
        
        # Her araç için grid yerleşimli butonlar oluştur
        row, col = 0, 0
        for tool_id, tool in self._tools.items():
            btn_frame = tk.Frame(tools_frame, bg=self.theme["card_bg"])
            btn_frame.grid(row=row, column=col, padx=5, pady=5)
            
            # Buton
            btn = tk.Button(
                btn_frame,
                text=f"{tool_icons[tool_id]} {tool.name}",
                width=12,
                height=2,
                bg=self.theme["primary_light"],
                fg=self.theme["text"],
                font=self.fonts["normal"],
                relief="raised",
                bd=0,
                activebackground=self.theme["primary"],
                activeforeground="white",
                cursor="hand2",
                command=lambda t=tool_id: self._select_tool(t)
            )
            btn.pack(fill=tk.X)
            self._tool_buttons[tool_id] = btn
            
            # 2 sütun olacak şekilde yerleştir
            col += 1
            if col > 1:
                col = 0
                row += 1
        
        # Araç butonlarını güncelle
        self._update_tool_buttons()
        
        # Ayarlar çerçevesi
        settings_frame = tk.LabelFrame(
            left_panel, 
            text="🎨 Renk ve Boyut", 
            font=self.fonts["subheader"],
            bg=self.theme["card_bg"],
            fg=self.theme["text"],
            padx=10, 
            pady=10
        )
        settings_frame.pack(fill=tk.X, pady=15, padx=10)
        
        # Renk seçici
        color_frame = tk.Frame(settings_frame, bg=self.theme["card_bg"])
        color_frame.pack(fill=tk.X, pady=5)
        
        color_btn = tk.Button(
            color_frame, 
            text="🎨 Renk Seç", 
            bg=self.theme["primary_light"],
            fg=self.theme["text"],
            font=self.fonts["normal"],
            relief="flat",
            bd=0,
            padx=5,
            pady=5,
            cursor="hand2",
            command=self._choose_color
        )
        color_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Renk gösterici
        self._color_preview = tk.Canvas(
            color_frame, 
            width=30, 
            height=30, 
            bg=self._settings.color,
            bd=0,
            highlightthickness=1,
            highlightbackground=self.theme["text"]
        )
        self._color_preview.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Hızlı renkler paleti
        palette_frame = tk.Frame(settings_frame, bg=self.theme["card_bg"])
        palette_frame.pack(fill=tk.X, pady=10)
        
        quick_colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF", "#000000", "#FFFFFF"]
        
        for i, color in enumerate(quick_colors):
            color_btn = tk.Button(
                palette_frame,
                bg=color,
                width=2,
                height=1,
                bd=0,
                relief="solid",
                highlightthickness=1,
                highlightbackground="#CCCCCC",
                cursor="hand2",
                command=lambda c=color: self._quick_color_select(c)
            )
            color_btn.grid(row=i//4, column=i%4, padx=2, pady=2, sticky="nsew")
        
        # Fırça boyutu
        brush_frame = tk.Frame(settings_frame, bg=self.theme["card_bg"])
        brush_frame.pack(fill=tk.X, pady=5)
        
        self._brush_size_label = tk.Label(
            brush_frame, 
            text=f"Boyut: {self._settings.brush_size}", 
            font=self.fonts["normal"],
            bg=self.theme["card_bg"],
            fg=self.theme["text"]
        )
        self._brush_size_label.pack(side=tk.TOP, pady=(0, 5))
        
        # Slider ile boyut ayarı
        self._brush_size_slider = ttk.Scale(
            brush_frame,
            from_=1,
            to=50,
            orient="horizontal",
            value=self._settings.brush_size,
            command=self._update_brush_size_from_slider
        )
        self._brush_size_slider.pack(fill=tk.X, pady=5)
        
        # Hızlı boyut butonları
        size_buttons_frame = tk.Frame(brush_frame, bg=self.theme["card_bg"])
        size_buttons_frame.pack(fill=tk.X, pady=5)
        
        sizes = [2, 5, 10, 20, 30]
        for size in sizes:
            size_btn = tk.Button(
                size_buttons_frame,
                text=str(size),
                width=2,
                bg=self.theme["primary_light"],
                fg=self.theme["text"],
                font=self.fonts["small"],
                bd=0,
                relief="flat",
                cursor="hand2",
                command=lambda s=size: self._set_brush_size(s)
            )
            size_btn.pack(side=tk.LEFT, padx=2, expand=True)
        
        # Dosya işlemleri
        file_frame = tk.LabelFrame(
            left_panel, 
            text="📁 Dosya İşlemleri", 
            font=self.fonts["subheader"],
            bg=self.theme["card_bg"],
            fg=self.theme["text"],
            padx=10, 
            pady=10
        )
        file_frame.pack(fill=tk.X, pady=15, padx=10)
        
        # Dosya butonları
        new_btn = tk.Button(
            file_frame, 
            text="🆕 Yeni", 
            bg=self.theme["primary_light"],
            fg=self.theme["text"],
            font=self.fonts["normal"],
            relief="flat",
            bd=0,
            padx=5,
            pady=8,
            cursor="hand2",
            command=self._clear_canvas
        )
        new_btn.pack(fill=tk.X, pady=3)
        
        save_btn = tk.Button(
            file_frame, 
            text="💾 Kaydet", 
            bg=self.theme["primary_light"],
            fg=self.theme["text"],
            font=self.fonts["normal"],
            relief="flat",
            bd=0,
            padx=5,
            pady=8,
            cursor="hand2",
            command=self._save_drawing
        )
        save_btn.pack(fill=tk.X, pady=3)
        
        # Geçmiş işlemleri
        history_frame = tk.LabelFrame(
            left_panel, 
            text="⏱️ Geçmiş", 
            font=self.fonts["subheader"],
            bg=self.theme["card_bg"],
            fg=self.theme["text"],
            padx=10, 
            pady=10
        )
        history_frame.pack(fill=tk.X, pady=15, padx=10)
        
        history_buttons_frame = tk.Frame(history_frame, bg=self.theme["card_bg"])
        history_buttons_frame.pack(fill=tk.X)
        
        undo_btn = tk.Button(
            history_buttons_frame, 
            text="⬅️ Geri Al", 
            bg=self.theme["primary_light"],
            fg=self.theme["text"],
            font=self.fonts["normal"],
            relief="flat",
            bd=0,
            padx=5,
            pady=8,
            cursor="hand2",
            command=self._undo
        )
        undo_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))
        
        redo_btn = tk.Button(
            history_buttons_frame, 
            text="➡️ İleri Al", 
            bg=self.theme["primary_light"],
            fg=self.theme["text"],
            font=self.fonts["normal"],
            relief="flat",
            bd=0,
            padx=5,
            pady=8,
            cursor="hand2",
            command=self._redo
        )
        redo_btn.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(2, 0))
        
        # Kısayollar bilgisi
        shortcuts_label = tk.Label(
            history_frame, 
            text="Ctrl+Z: Geri Al\nCtrl+Y: İleri Al", 
            font=self.fonts["small"],
            bg=self.theme["card_bg"],
            fg=self.theme["text"],
            justify=tk.LEFT
        )
        shortcuts_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Sağ panel - Çizim alanı
        right_panel = tk.Frame(main_frame, bg=self.theme["card_bg"], bd=1, relief="solid")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Kanvas üst kısmı - bilgi çubuğu
        canvas_header = tk.Frame(right_panel, bg=self.theme["primary"], height=30)
        canvas_header.pack(fill=tk.X)
        
        self._canvas_info = tk.Label(
            canvas_header,
            text="Hazır",
            bg=self.theme["primary"],
            fg="white",
            font=self.fonts["normal"],
            anchor=tk.W,
            padx=10
        )
        self._canvas_info.pack(side=tk.LEFT, fill=tk.Y)
        
        # Kanvas arka plan seçenekleri
        bg_label = tk.Label(
            canvas_header,
            text="Arka plan:",
            bg=self.theme["primary"],
            fg="white",
            font=self.fonts["normal"]
        )
        bg_label.pack(side=tk.RIGHT, padx=(0, 5))
        
        white_bg = tk.Button(
            canvas_header,
            text="⬜",
            bg="white",
            fg="black",
            width=2,
            height=1,
            bd=1,
            relief="solid",
            cursor="hand2",
            command=lambda: self._change_canvas_bg("white")
        )
        white_bg.pack(side=tk.RIGHT, padx=2)
        
        black_bg = tk.Button(
            canvas_header,
            text="⬛",
            bg="black",
            fg="white",
            width=2,
            height=1,
            bd=1,
            relief="solid",
            cursor="hand2",
            command=lambda: self._change_canvas_bg("black")
        )
        black_bg.pack(side=tk.RIGHT, padx=2)
        
        light_bg = tk.Button(
            canvas_header,
            text="🔆",
            bg="#F5F5F5",
            fg="black",
            width=2,
            height=1,
            bd=1,
            relief="solid",
            cursor="hand2",
            command=lambda: self._change_canvas_bg("#F5F5F5")
        )
        light_bg.pack(side=tk.RIGHT, padx=2)
        
        # Kanvas
        self._canvas = tk.Canvas(
            right_panel, 
            bg=self._settings.canvas_bg,
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0
        )
        self._canvas.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Durum çubuğu
        status_bar_frame = tk.Frame(self._root, bg=self.theme["primary"], height=25)
        status_bar_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self._status_bar = tk.Label(
            status_bar_frame, 
            text="Hazır", 
            bg=self.theme["primary"],
            fg="white",
            font=self.fonts["small"],
            anchor=tk.W,
            padx=10
        )
        self._status_bar.pack(side=tk.LEFT, fill=tk.Y)
        
        # Kredi
        credit_label = tk.Label(
            status_bar_frame,
            text="© 2025 Sedef",
            bg=self.theme["primary"],
            fg="white",
            font=self.fonts["small"],
            padx=10
        )
        credit_label.pack(side=tk.RIGHT)
    
    def _setup_drawing_events(self):
        """Çizim olaylarını bağlar"""
        self._canvas.bind("<ButtonPress-1>", self._start_draw)
        self._canvas.bind("<B1-Motion>", self._draw)
        self._canvas.bind("<ButtonRelease-1>", self._end_draw)
        self._canvas.bind("<Motion>", self._update_status_bar)
    
    def _setup_keyboard_shortcuts(self):
        """Klavye kısayollarını ayarlar"""
        self._root.bind("<Control-z>", lambda e: self._undo())
        self._root.bind("<Control-y>", lambda e: self._redo())
        self._root.bind("<Control-s>", lambda e: self._save_drawing())
        self._root.bind("<Control-n>", lambda e: self._clear_canvas())
        
        # Araç kısayolları
        self._root.bind("1", lambda e: self._select_tool("oval"))
        self._root.bind("2", lambda e: self._select_tool("square"))
        self._root.bind("3", lambda e: self._select_tool("star"))
        self._root.bind("4", lambda e: self._select_tool("line"))
        self._root.bind("5", lambda e: self._select_tool("circle"))
        self._root.bind("6", lambda e: self._select_tool("eraser"))
        
        # Fırça boyutu kısayolları
        self._root.bind("+", lambda e: self._increase_brush_size())
        self._root.bind("-", lambda e: self._decrease_brush_size())
    
    def _select_tool(self, tool_id):
        """Seçili aracı değiştirir"""
        if tool_id in self._tools:
            self._active_tool = tool_id
            self._update_tool_buttons()
            self._canvas_info.config(text=f"Aktif Araç: {self._tools[tool_id].name}")
    
    def _update_tool_buttons(self):
        """Araç butonlarını günceller"""
        for tool_id, button in self._tool_buttons.items():
            if tool_id == self._active_tool:
                button.config(
                    relief=tk.SUNKEN, 
                    bg=self.theme["primary"],
                    fg="white"
                )
            else:
                button.config(
                    relief=tk.RAISED, 
                    bg=self.theme["primary_light"],
                    fg=self.theme["text"]
                )
    
    def _choose_color(self):
        """Renk seçimi diyalogunu gösterir"""
        color = colorchooser.askcolor(initialcolor=self._settings.color)[1]
        if color:
            self._settings.color = color
            self._color_preview.config(bg=self._settings.color)
    
    def _quick_color_select(self, color):
        """Hızlı renk seçimi"""
        self._settings.color = color
        self._color_preview.config(bg=self._settings.color)
    
    def _increase_brush_size(self):
        """Fırça boyutunu artırır"""
        self._settings.brush_size = min(50, self._settings.brush_size + 2)
        self._update_brush_size_label()
        self._brush_size_slider.set(self._settings.brush_size)
    
    def _decrease_brush_size(self):
        """Fırça boyutunu azaltır"""
        self._settings.brush_size = max(1, self._settings.brush_size - 2)
        self._update_brush_size_label()
        self._brush_size_slider.set(self._settings.brush_size)
    
    def _set_brush_size(self, size):
        """Fırça boyutunu ayarlar"""
        self._settings.brush_size = size
        self._update_brush_size_label()
        self._brush_size_slider.set(size)
    
    def _update_brush_size_from_slider(self, value):
        """Slider'dan fırça boyutunu günceller"""
        size = int(float(value))
        self._settings.brush_size = size
        self._update_brush_size_label()
    
    def _update_brush_size_label(self):
        """Fırça boyutu etiketini günceller"""
        self._brush_size_label.config(text=f"Boyut: {self._settings.brush_size}")
    
    def _clear_canvas(self):
        """Kanvası temizler"""
        if messagebox.askyesno(
            "Temizle", 
            "Tüm çizim silinecek. Emin misiniz?",
            icon="question"
        ):
            self._canvas.delete("all")
            self._history.save_state()
    
    def _start_draw(self, event):
        """Çizim başlangıcını işler"""
        tool = self._tools[self._active_tool]
        
        # Çizgi veya daire gibi araçlar için başlangıç noktasını kaydet
        if hasattr(tool, 'start'):
            tool.start(self._canvas, event.x, event.y)
    
    def _draw(self, event):
        """Çizim hareketini işler"""
        tool = self._tools[self._active_tool]
        
        # Çizgi veya daire gibi araçlar için önizleme
        if hasattr(tool, 'drag'):
            tool.drag(self._canvas, event.x, event.y, self._settings.color)
        else:
            # Normal fırça araçları için
            tool.draw(
                self._canvas, 
                event.x, 
                event.y, 
                self._settings.brush_size, 
                self._settings.color
            )
        
        # Durum çubuğunu güncelle
        self._status_bar.config(text=f"Çizim: ({event.x}, {event.y}) - Araç: {self._tools[self._active_tool].name}")
    
    def _end_draw(self, event):
        """Çizim bitişini işler ve geçmişe kaydeder"""
        tool = self._tools[self._active_tool]
        
        # Eğer araçta 'end' metodu varsa (örneğin çizgi, daire gibi araçlar)
        if hasattr(tool, 'end'):
            tool.end(
                self._canvas, 
                event.x, 
                event.y, 
                self._settings.brush_size, 
                self._settings.color
            )
        
        # Her çizim işleminden sonra mevcut durumu kaydet
        self._history.save_state()
    
    def _undo(self):
        """Geri al işlemini gerçekleştirir"""
        self._history.undo()
        self._status_bar.config(text="Son işlem geri alındı")
    
    def _redo(self):
        """İleri al işlemini gerçekleştirir"""
        self._history.redo()
        self._status_bar.config(text="Son işlem tekrar uygulandı")
    
    def _save_drawing(self):
        """Çizimi dosyaya kaydeder - PhotoImage kullanarak doğrudan kaydeder"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Dosyaları", "*.png"), ("Tüm Dosyalar", "*.*")]
        )
        if file_path:
            try:
                # Canvas'ı widget olarak al ve sınırlarını belirle
                x = self._canvas.winfo_rootx()
                y = self._canvas.winfo_rooty()
                width = self._canvas.winfo_width()
                height = self._canvas.winfo_height()
                
                # Ekran görüntüsü alma yöntemini kullan
                try:
                    # PIL kullan
                    # Ekran görüntüsü al
                    img = ImageGrab.grab(bbox=(x, y, x+width, y+height))
                    img.save(file_path)
                    messagebox.showinfo(
                        "Kaydedildi", 
                        "Çizim başarıyla kaydedildi!",
                        icon="info"
                    )
                    self._status_bar.config(text=f"Çizim kaydedildi: {file_path}")
                except ImportError:
                    messagebox.showerror(
                        "Hata", 
                        "PIL kütüphanesi bulunamadı. Lütfen 'pip install pillow' komutunu çalıştırın.",
                        icon="error"
                    )
                except Exception as e:
                    # PIL hata verirse alternatif yöntemi dene
                    messagebox.showerror(
                        "Hata", 
                        f"PIL ile kaydetme başarısız: {str(e)}\nPostscript yöntemi deneniyor...",
                        icon="error"
                    )
                    self._save_as_postscript(file_path)
            except Exception as e:
                messagebox.showerror(
                    "Hata", 
                    f"Kaydederken bir hata oluştu: {str(e)}",
                    icon="error"
                )

    def _save_as_postscript(self, file_path):
        """Çizimi postscript olarak kaydeder"""
        ps_file = file_path.replace(".png", ".ps")
        if not ps_file.endswith(".ps"):
            ps_file += ".ps"
        
        try:
            self._canvas.postscript(file=ps_file, colormode='color')
            messagebox.showinfo(
                "Bilgi", 
                f"Çizim postscript formatında kaydedildi: {ps_file}",
                icon="info"
            )
            self._status_bar.config(text=f"Postscript kaydedildi: {ps_file}")
        except Exception as e:
            messagebox.showerror(
                "Hata", 
                f"Postscript olarak kaydetme başarısız: {str(e)}",
                icon="error"
            )
    
    def _update_status_bar(self, event):
        """Durum çubuğunu günceller"""
        self._status_bar.config(text=f"Fare: ({event.x}, {event.y}) - Araç: {self._tools[self._active_tool].name}")
    
    def _change_canvas_bg(self, color):
        """Kanvas arka planını değiştirir"""
        self._settings.canvas_bg = color
        self._canvas.config(bg=self._settings.canvas_bg)
        self._status_bar.config(text=f"Arka plan rengi değiştirildi: {color}")

class AdvancedPaintApp(PaintApp):
    """Gelişmiş Paint uygulaması sınıfı"""
    def __init__(self, root):
        super().__init__(root)
        self._root.title("Sedef'in Paint Uygulaması")
        self._root.configure(bg="#f0f0f0")
        
        # Uygulama simgesi eklenebilir (varsa)
        # self._root.iconbitmap("paint_icon.ico")
        
        # Font ayarları
        self._default_font = ("Segoe UI", 10)
        self._root.option_add("*Font", self._default_font)
        
        # Ek araçlar ekle
        self._add_advanced_features()
        
    def _add_advanced_features(self):
        """Gelişmiş özellikler ekler"""
        # Ana çerçeve - tüm ek özellikleri içerecek
        advanced_frame = tk.Frame(self._root, bg="#f0f0f0", pady=8, padx=10)
        advanced_frame.pack(side=tk.BOTTOM, fill=tk.X, before=self._status_bar)
        
        # Arkaplan rengi seçimi
        bg_frame = tk.LabelFrame(
            advanced_frame, 
            text="Arkaplan Rengi", 
            padx=8, 
            pady=8, 
            bg="#e8e8e8",
            font=("Segoe UI", 9, "bold"),
            relief=tk.GROOVE
        )
        bg_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Arkaplan renk butonları - daha fazla renk seçeneği
        bg_colors = [
            ("Beyaz", "white", "black"),
            ("Siyah", "black", "white"),
            ("Açık Mavi", "#e6f2ff", "black"),
            ("Açık Sarı", "#ffffcc", "black")
        ]
        
        for text, bg, fg in bg_colors:
            bg_btn = tk.Button(
                bg_frame,
                text=text,
                bg=bg,
                fg=fg,
                command=lambda color=bg: self._change_canvas_bg(color),
                width=10,
                relief=tk.RAISED,
                borderwidth=2,
                cursor="hand2"
            )
            bg_btn.pack(side=tk.LEFT, padx=4, pady=2)
        
        # Özel arkaplan rengi seçici
        custom_bg_btn = tk.Button(
            bg_frame,
            text="Özel Renk",
            command=self._choose_custom_bg,
            width=10,
            relief=tk.RAISED,
            borderwidth=2,
            cursor="hand2"
        )
        custom_bg_btn.pack(side=tk.LEFT, padx=4, pady=2)
        
        # Ekstra özellikler bölümü
        extra_frame = tk.LabelFrame(
            advanced_frame, 
            text="Ekstra Özellikler", 
            padx=8, 
            pady=8, 
            bg="#e8e8e8",
            font=("Segoe UI", 9, "bold"),
            relief=tk.GROOVE
        )
        extra_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Temizle butonu
        clear_btn = tk.Button(
            extra_frame,
            text="Temizle",
            command=self._clear_canvas,
            width=10,
            bg="#ff9999",
            relief=tk.RAISED,
            borderwidth=2,
            cursor="hand2"
        )
        clear_btn.pack(side=tk.LEFT, padx=4, pady=2)
        
        # Kaydet butonu
        save_btn = tk.Button(
            extra_frame,
            text="Kaydet",
            command=self._save_image,
            width=10,
            bg="#99ccff",
            relief=tk.RAISED,
            borderwidth=2,
            cursor="hand2"
        )
        save_btn.pack(side=tk.LEFT, padx=4, pady=2)
        
        # Hakkında butonu - sağ tarafa hizalı
        about_frame = tk.Frame(advanced_frame, bg="#f0f0f0")
        about_frame.pack(side=tk.RIGHT, padx=10, pady=5)
        
        about_btn = tk.Button(
            about_frame, 
            text="Hakkında", 
            command=self._show_about, 
            width=12,
            bg="#e0e0e0",
            relief=tk.RAISED,
            borderwidth=2,
            cursor="hand2"
        )
        about_btn.pack(pady=2)

    def _change_canvas_bg(self, color):
        """Kanvas arka planını değiştirir"""
        self._settings.canvas_bg = color
        self._canvas.config(bg=self._settings.canvas_bg)
        self._status_bar.config(text=f"Arkaplan rengi: {color} olarak değiştirildi")
    
    def _choose_custom_bg(self):
        """Özel arkaplan rengi seçmek için renk seçiciyi açar"""
        from tkinter import colorchooser
        color = colorchooser.askcolor(title="Arkaplan Rengi Seç")[1]
        if color:
            self._change_canvas_bg(color)
    
    def _clear_canvas(self):
        """Kanvası temizler"""
        self._canvas.delete("all")
        self._status_bar.config(text="Kanvas temizlendi")
    
    def _save_image(self):
        """Çizimi resim olarak kaydeder"""
        from tkinter import filedialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG dosyası", "*.png"), ("Tüm dosyalar", "*.*")]
        )
        if file_path:
            try:
                # Burada gerçek kaydetme kodunu ekleyin
                # Örnek: self._canvas.postscript(file=file_path, colormode='color')
                self._status_bar.config(text=f"Resim kaydedildi: {file_path}")
            except Exception as e:
                self._status_bar.config(text=f"Hata: {e}")

    def _show_about(self):
        """Hakkında diyaloğunu gösterir"""
        about_window = tk.Toplevel(self._root)
        about_window.title("Hakkında")
        about_window.geometry("400x300")
        about_window.resizable(False, False)
        about_window.configure(bg="#f8f8f8")
        
        # Pencere simgesini ana pencereyle aynı yap
        if hasattr(self._root, "iconbitmap"):
            about_window.iconbitmap(self._root.iconbitmap())
        
        # Logo ve başlık
        logo_frame = tk.Frame(about_window, height=80, bg="#f8f8f8")
        logo_frame.pack(fill=tk.X, pady=15)
        
        logo_label = tk.Label(
            logo_frame,
            text="Sedef'in Paint Uygulaması",
            font=("Segoe UI", 18, "bold"),
            fg="#3366cc",
            bg="#f8f8f8"
        )
        logo_label.pack()
        
        version_label = tk.Label(
            logo_frame,
            text="Versiyon 1.0",
            font=("Segoe UI", 10),
            fg="#666666",
            bg="#f8f8f8"
        )
        version_label.pack(pady=5)
        
        # Bilgi metni
        info_frame = tk.Frame(about_window, bg="#f8f8f8")
        info_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=10)
        
        info_text = tk.Text(
            info_frame,
            wrap=tk.WORD,
            width=40,
            height=6,
            font=("Segoe UI", 10),
            bd=0,
            padx=5,
            pady=5,
            bg="#f8f8f8"
        )
        info_text.insert(tk.END, "Bu uygulanma Sedef Timur tarafından \nNesneye Dayalı Programlama dersi için geliştirilmiştir.")
        info_text.config(state=tk.DISABLED)
        info_text.pack(fill=tk.BOTH, expand=True)
        
        # Telif hakkı
        copyright_label = tk.Label(
            about_window,
            text="© 2025 Sedef Timur. Tüm hakları saklıdır.",
            font=("Segoe UI", 8),
            fg="#888888",
            bg="#f8f8f8"
        )
        copyright_label.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedPaintApp(root)
    root.mainloop()