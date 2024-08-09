# Türkçe Metin & PDF Özetleme ve Çeviri Sistemi

Bu proje, Türkçe metinleri ve PDF dosyalarını özetleyen ve çeviren bir web uygulamasıdır.

## Özellikler

- PDF dosyalarından metin çıkarma
- çıkan metini bir bölümde göster
- başka metin kutusu daha olsun.
- 
- Türkçe metin özetleme
- Duygu analizi
- Anahtar kelime çıkarma
- Metin sınıflandırma 
- Türkçe-İngilizce çeviri
- çapraz çeviri 
- Soru-cevap işlevi

aynı zamanda yandan açılan bir drawing yada header olabilir.

## Kurulum


1. Repoyu klonlayın:
   ```
   git clone https://github.com/your-username/your-repo-name.git
   ```

2. Gerekli Python paketlerini yükleyin:
   ```
   pip install -r requirements.txt
   ```

3. Frontend bağımlılıklarını yükleyin:
   ```
   cd frontend
   npm install
   ```

## Kullanım

1. Backend'i başlatın:
   ```
   uvicorn app.main:app --reload
   ```

2. Frontend'i başlatın:
   ```
   cd frontend
   npm start
   ```

3. Tarayıcınızda `http://localhost:3000` adresine gidin.

## Testler

Testleri çalıştırmak için:
```
pytest
```

## Docker ile Çalıştırma

```
docker-compose up --build
```

## Katkıda Bulunma

1. Bu repoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Branch'inizi push edin (`git push origin feature/AmazingFeature`)
5. Bir Pull Request oluşturun

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.