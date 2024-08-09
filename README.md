# Türkçe Doğal Dil İşleme Projesi

Bu proje, Türkçe metinler üzerinde çeşitli doğal dil işleme görevlerini gerçekleştirmek için tasarlanmış kapsamlı bir uygulamadır. Projenin amacı, Türkçe dili için güçlü ve kullanımı kolay NLP araçları sunmaktır.

## Özellikler

1. **Anahtar Kelime Çıkarma**: Metinlerden önemli anahtar kelimeleri otomatik olarak çıkarır.
2. **Soru Cevaplama**: Verilen bir metin ve soru üzerinden otomatik cevap üretir.
3. **Duygu Analizi**: Metinlerin duygusal tonunu analiz eder (olumlu, olumsuz, nötr).
4. **Metin Özetleme**: Uzun metinleri daha kısa ve öz hale getirir.
5. **Metin Sınıflandırma**: Metinleri önceden belirlenmiş kategorilere ayırır.
6. **Çeviri**: Türkçe metinleri diğer dillere çevirir veya diğer dillerden Türkçe'ye çevirir.
7. **PDF İşleme**: PDF dosyalarından metin çıkarma ve analiz etme.

## Kurulum

1. Repo'yu klonlayın:
   ```
   git clone https://github.com/your-username/turkce-nlp.git
   ```

2. Gerekli paketleri yükleyin:
   ```
   pip install -r requirements.txt
   ```

3. Gerekli ortam değişkenlerini ayarlayın (`.env` dosyasını kullanın).

4. Uygulamayı başlatın:
   ```
   python main.py
   ```
   ya da
      ```
   uvicorn main:app --reload
   ```

## Kullanım

### Backend

Backend servisi, Flask kullanılarak oluşturulmuştur. API endpoint'leri şunlardır:

- `/extract-keywords`: Anahtar kelime çıkarma
- `/answer-question`: Soru cevaplama
- `/analyze-sentiment`: Duygu analizi
- `/summarize`: Metin özetleme
- `/classify`: Metin sınıflandırma
- `/translate`: Çeviri
- `/process-pdf`: PDF işleme

Backend için gerekli Python paketlerini yükleyin:
   ```
   cd backend
   pip install -r requirements.txt
   ```

Her endpoint için POST isteği yapılmalı ve gerekli parametreler JSON formatında gönderilmelidir.

### Frontend

Frontend, React kullanılarak geliştirilmiştir. Kullanıcı dostu bir arayüz ile tüm NLP işlemlerini gerçekleştirebilirsiniz.

1. Frontend klasörüne gidin:
   ```
   cd frontend
   ```

2. Bağımlılıkları yükleyin:
   ```
   yarn install
   ```

3. Uygulamayı başlatın:
   ```
   yarn start
   ```

## Testler

Testleri çalıştırmak için:

```
python -m pytest tests/
```

## Katkıda Bulunma

# Katkıda Bulunanlar

Bu projede emeği geçen herkese teşekkür ederiz. Aşağıda projeye katkıda bulunan kişilerin listesi yer almaktadır:

| İsim | Rol |
| -- | --- |
| [Yasin Tanış](https://github.com/ysntns) | Ana Geliştirici |
|[Yasin Tanış](https://github.com/ysntns)  | Backend Geliştirici |
| [Yasin Tanış](https://github.com/ysntns) | Frontend Geliştirici |
|[Yasin Tanış](https://github.com/ysntns)  | NLP Modelleri Geliştirici |
|  [Yasin Tanış](https://github.com/ysntns)| Veri Bilimci |
|[Yasin Tanış](https://github.com/ysntns)  | Dokümantasyon ve Test |


## Nasıl Katkıda Bulunabilirsiniz?

1. Bu repo'yu fork edin.
2. Yeni bir branch oluşturun (`git checkout -b feature/AmazingFeature`).
3. Değişikliklerinizi commit edin (`git commit -m 'Add some AmazingFeature'`).
4. Branch'inizi push edin (`git push origin feature/AmazingFeature`).
5. Bir Pull Request oluşturun.

Lütfen katkıda bulunmadan önce `CONTRIBUTING.md` dosyasını okuyunuz.

## Lisans

Bu proje   Apache License  altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakınız.# veri_kaganligi
