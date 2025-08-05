# İLKE 2: KAPSÜLLEME (ENCAPSULATION)
# ===================================
# Kapsülleme, bir nesnenin içsel durumunu dış dünyadan gizleme ve
# bu duruma erişimi kontrollü bir şekilde sağlama ilkesidir.
# Bu ilke ile:
# - Veri gizleme (data hiding) sağlanır
# - Nesnenin durumu üzerinde kontrol sağlanır
# - Nesnenin iç yapısı değiştiğinde dış arayüzünün etkilenmemesi sağlanır

class DrawingSettings:
    """
    Çizim ayarlarını yöneten sınıf.
    
    Bu sınıf, renkler ve fırça boyutu gibi çizim ayarlarını
    kapsüller ve kontrollü erişim sağlar.
    """
    def __init__(self):
        # Özel değişkenler (_) ile başlayarak kapsülleme uygulanıyor
        # Doğrudan erişim yerine, property'ler aracılığıyla kontrollü erişim sağlanır
        self._color = "#000000"  # Siyah
        self._brush_size = 5
        self._canvas_bg = "#FFFFFF"  # Beyaz
        
    @property
    def color(self):
        """Çizim rengi için getter"""
        return self._color
    
    @color.setter
    def color(self, value):
        """
        Çizim rengi için setter.
        Sadece geçerli renk değerleri atanmasını sağlar.
        """
        # Değer kontrolü yapılarak kapsüllemenin bir avantajı gösteriliyor
        if isinstance(value, str) and (value.startswith("#") or value in ['black', 'white', 'red', 'green', 'blue']):
            self._color = value
    
    @property
    def brush_size(self):
        """Fırça boyutu için getter"""
        return self._brush_size
    
    @brush_size.setter
    def brush_size(self, value):
        """
        Fırça boyutu için setter.
        Sadece 1-50 arasındaki değerlerin atanmasını sağlar.
        """
        # Değer kontrolü ile veri bütünlüğü korunuyor
        if isinstance(value, int) and 1 <= value <= 50:
            self._brush_size = value
            
    @property
    def canvas_bg(self):
        """Tuval arka plan rengi için getter"""
        return self._canvas_bg
    
    @canvas_bg.setter
    def canvas_bg(self, value):
        """
        Tuval arka plan rengi için setter.
        Sadece geçerli renk değerleri atanmasını sağlar.
        """
        if isinstance(value, str) and (value.startswith("#") or value in ['black', 'white']):
            self._canvas_bg = value

class PaintHistory:
    """
    Çizim geçmişini yöneten sınıf.
    
    Bu sınıf da kapsülleme ilkesini uygular. Geçmiş verilerini
    ve ilgili yöntemleri kapsüller.
    """
    def __init__(self, canvas):
        # Özel değişkenler ile kapsülleme
        self._canvas = canvas
        self._history = []
        self._current_step = -1
        self._max_history = 20
        
    def save_state(self):
        """Mevcut kanvas durumunu kaydeder"""
        if self._current_step < len(self._history) - 1:
            # Geçmiş akışını koru
            self._history = self._history[:self._current_step+1]
        
        # Kanvas öğelerini kaydet
        items_data = []
        for item_id in self._canvas.find_all():
            item_type = self._canvas.type(item_id)
            coords = self._canvas.coords(item_id)
            options = {}
            for option in ['fill', 'outline', 'width', 'dash']:
                try:
                    value = self._canvas.itemcget(item_id, option)
                    if value:
                        options[option] = value
                except:
                    pass
            items_data.append((item_type, coords, options))
        
        # İç veriyi güncelle ve sınırlama uygula - kapsülleme sayesinde 
        # bu karmaşık işlem dışarıya karşı basitleştirilir
        self._history.append(items_data)
        if len(self._history) > self._max_history:
            self._history.pop(0)
        self._current_step = len(self._history) - 1
        
    def undo(self):
        """Bir adım geri al - dış arayüz basit ve anlaşılır"""
        if self._current_step > 0:
            self._current_step -= 1
            self._restore_state()
            return True
        return False
    
    def redo(self):
        """Bir adım ileri al - dış arayüz basit ve anlaşılır"""
        if self._current_step < len(self._history) - 1:
            self._current_step += 1
            self._restore_state()
            return True
        return False
    
    def _restore_state(self):
        """
        Belirtilen adımdaki durumu geri yükle.
        
        Alt çizgi (_) ile başlayan metot ismi, bu metodun 
        sınıf içi kullanım için olduğunu belirtir (kapsülleme).
        """
        self._canvas.delete("all")
        if 0 <= self._current_step < len(self._history):
            for item_type, coords, options in self._history[self._current_step]:
                if item_type == "oval":
                    self._canvas.create_oval(coords, **options)
                elif item_type == "rectangle":
                    self._canvas.create_rectangle(coords, **options)
                elif item_type == "line":
                    self._canvas.create_line(coords, **options)
                elif item_type == "polygon":
                    self._canvas.create_polygon(coords, **options)