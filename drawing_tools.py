import tkinter as tk
import math
from abstract_classes import DrawingTool

# İLKE 4: ÇOK BİÇİMLİLİK (POLYMORPHISM)
# =====================================
# Çok biçimlilik, farklı sınıfların aynı arayüzü paylaşarak 
# farklı davranışlar sergilemesidir.
# Bu ilke ile:
# - Kod esnekliği ve genişletilebilirliği sağlanır
# - Aynı arayüzü kullanan farklı nesneler oluşturulur
# - İstemci kodu, kullandığı nesnenin tam tipini bilmeden çalışabilir

# Aşağıdaki çizim araçları, DrawingTool soyut sınıfından türetilmiş
# ve aynı arayüzü (draw metodu) kullanarak farklı davranışlar sergiliyor.

class OvalBrush(DrawingTool):
    """
    Oval fırça aracı - DrawingTool soyut sınıfının somut bir uygulaması.
    Kullanıcının fare pozisyonunda oval şekiller çizer.
    """
    def draw(self, canvas, x, y, brush_size, color):
        # Çok biçimlilik: Aynı metodun farklı bir implementasyonu
        # Bu metot oval şekiller çizerek draw arayüzünü uygular
        x1, y1 = (x - brush_size), (y - brush_size)
        x2, y2 = (x + brush_size), (y + brush_size)
        return canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)
    
    @property
    def name(self):
        # name property'sinin uygulanması
        return "Oval Fırça"

class SquareBrush(DrawingTool):
    """
    Kare fırça aracı - DrawingTool soyut sınıfının somut bir uygulaması.
    Kullanıcının fare pozisyonunda kare şekiller çizer.
    """
    def draw(self, canvas, x, y, brush_size, color):
        # Çok biçimlilik, bu metot kare şekiller çizerek draw arayüzünü uygular
        x1, y1 = (x - brush_size), (y - brush_size)
        x2, y2 = (x + brush_size), (y + brush_size)
        return canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)
    
    @property
    def name(self):
        # name property'sinin uygulanması
        return "Kare Fırça"
        
class StarBrush(DrawingTool):
    """
    Yıldız fırça aracı - DrawingTool soyut sınıfının somut bir uygulaması.
    Kullanıcının fare pozisyonunda yıldız şekiller çizer.
    """
    def draw(self, canvas, x, y, brush_size, color):
        # Çok biçimlilik: Aynı metodun farklı bir implementasyonu
        # Bu metot yıldız şekiller çizerek draw arayüzünü uygular
        
        # Yıldız için köşe noktaları
        points = []
        outer_radius = brush_size * 2
        inner_radius = brush_size
        num_points = 5  # 5 köşeli yıldız
        
        for i in range(num_points * 2):
            # Dış ve iç noktalar arasında geçiş yap
            radius = outer_radius if i % 2 == 0 else inner_radius
            # Açı (radyan cinsinden)
            angle = i * (3.14159 / num_points)
            # X ve Y koordinatları
            px = x + radius * 0.8 * math.cos(angle)
            py = y + radius * 0.8 * math.sin(angle)
            points.extend([px, py])
            
        return canvas.create_polygon(points, fill=color, outline=color)
    
    @property
    def name(self):
        # name property'sinin uygulanması
        return "Yıldız Fırça"

class LineTool(DrawingTool):
    """
    Çizgi çizme aracı - DrawingTool soyut sınıfından türeyen
    ama daha karmaşık davranışı olan bir çizim aracı.
    """
    def __init__(self):
        # Bu araç için özel durum bilgilerini saklama
        self.start_x = None
        self.start_y = None
        self.temp_line = None
    
    # Çok biçimlilik: DrawingTool arayüzünün ötesinde ek metotlar ekleyebiliriz
    def start(self, canvas, x, y):
        """Çizgi çiziminin başlangıç noktasını kaydeder"""
        self.start_x = x
        self.start_y = y
        
    def drag(self, canvas, x, y, color):
        """Çizgi önizlemesini gösterir"""
        if self.temp_line:
            canvas.delete(self.temp_line)
        self.temp_line = canvas.create_line(
            self.start_x, self.start_y, x, y, 
            fill=color, width=2, dash=(4, 2)
        )
    
    def draw(self, canvas, x, y, brush_size, color):
        # Çok biçimlilik: Aynı arayüz (draw) ama farklı davranış
        if self.start_x is not None and self.start_y is not None:
            if self.temp_line:
                canvas.delete(self.temp_line)
                self.temp_line = None
            result = canvas.create_line(
                self.start_x, self.start_y, x, y, 
                fill=color, width=brush_size, smooth=True, 
                capstyle=tk.ROUND, joinstyle=tk.ROUND
            )
            self.start_x = None
            self.start_y = None
            return result
        return None
    
    @property
    def name(self):
        return "Çizgi Aracı"

class CircleTool(DrawingTool):
    """
    Daire çizme aracı - DrawingTool soyut sınıfından türeyen başka bir araç.
    """
    def __init__(self):
        self.start_x = None
        self.start_y = None
        self.temp_circle = None
    
    def start(self, canvas, x, y):
        """Daire çiziminin merkez noktasını kaydeder"""
        self.start_x = x
        self.start_y = y
        
    def drag(self, canvas, x, y, color):
        """Daire önizlemesini gösterir"""
        if self.start_x is None or self.start_y is None:
            return
        if self.temp_circle:
            canvas.delete(self.temp_circle)
        radius = ((x - self.start_x) ** 2 + (y - self.start_y) ** 2) ** 0.5
        self.temp_circle = canvas.create_oval(
            self.start_x - radius, self.start_y - radius,
            self.start_x + radius, self.start_y + radius,
            outline=color, dash=(4, 2), tags="preview"
        )
    
    def draw(self, canvas, x, y, brush_size, color):
        # Çok biçimlilik: Aynı arayüz (draw) ama farklı davranış
        if self.start_x is not None and self.start_y is not None:
            if self.temp_circle:
                canvas.delete(self.temp_circle)
                self.temp_circle = None
            radius = ((x - self.start_x) ** 2 + (y - self.start_y) ** 2) ** 0.5
            result = canvas.create_oval(
                self.start_x - radius, self.start_y - radius,
                self.start_x + radius, self.start_y + radius,
                outline=color, width=brush_size
            )
            self.start_x = None
            self.start_y = None
            return result
        return None
    
    @property
    def name(self):
        return "Daire Aracı"

class EraserTool(DrawingTool):
    """
    Silgi aracı - DrawingTool soyut sınıfının somut bir uygulaması.
    Tuval üzerindeki çizimleri silmek için kullanılır.
    """
    def draw(self, canvas, x, y, brush_size, color):
        # Çok biçimlilik: Aynı arayüz (draw) ile silgi işlevselliği sağlanıyor
        # Silgi aracı arka plan rengini kullanarak üzerine çizer
        bg_color = canvas["background"]
        x1, y1 = (x - brush_size), (y - brush_size)
        x2, y2 = (x + brush_size), (y + brush_size)
        return canvas.create_rectangle(x1, y1, x2, y2, fill=bg_color, outline=bg_color)
    
    @property
    def name(self):
        return "Silgi"