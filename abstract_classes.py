from abc import ABC, abstractmethod

# İLKE 1: SOYUTLAMA (ABSTRACTION)
# ===============================
# Soyutlama, gereksiz detayları gizleyip önemli özellikleri ortaya çıkarır.
# Bu ilke ile:
# - Karmaşık sistemleri basitleştiririz
# - Gerçeklemeden bağımsız arayüzler tanımlarız
# - Doğru soyutlama, kodun genişletilebilirliğini artırır

class DrawingTool(ABC):
    """
    Çizim araçları için soyut temel sınıf.
    
    Bu sınıf, tüm çizim araçlarının uygulaması gereken temel metotları tanımlar.
    ABC (Abstract Base Class) kullanılarak, bu sınıftan doğrudan nesne oluşturulması engellenir.
    İlgili tüm çizim araçları bu soyut sınıfı miras almalıdır.
    """
    
    @abstractmethod
    def draw(self, canvas, x, y, brush_size, color):
        """
        Çizim işlemini gerçekleştiren soyut metot.
        
        Tüm alt sınıflar bu metodu kendi çizim mantıklarına göre uygulamalıdır.
        @abstractmethod dekoratörü sayesinde, bu metodu uygulamayan alt sınıflar 
        örneklenemez (instantiate).
        """
        pass
    
    @property
    @abstractmethod
    def name(self):
        """
        Aracın adını döndüren soyut özellik (property).
        
        Her çizim aracının kullanıcı arayüzünde görüntülenecek bir adı olmalıdır.
        Bu özellik, arayüzdeki butonlar ve durum çubuğunda kullanılır.
        """
        pass