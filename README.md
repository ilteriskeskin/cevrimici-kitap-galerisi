# Çevrimiçi kitap galerisi

[kitaplar-api](https://collectapi.com/tr/api/book/kitaplar-api) ya da [Google Books API](https://developers.google.com/books/docs/overview) kullanılarak çevrimiçi kitap galerisi oluşturulacak 


**Proje Kurulumu**

```
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
python3 app.py
```

Kitaplar API ücretsiz key vermektedir ancak aylık 100 istek hakkı sunmaktadır. Bu yüzden Google Books API kullanmak daha uygun görünüyor. Herkesin kendine ait bir key oluşturması gerekmektedir.

**Proje Açıklaması**

* Proje kullanıcıların kitapları sorgulayabildiği online bir kütüphane olacak.
* Aradıkları kitapla ilgili detaylı bilgiler edinilebilecek.
* API'ın sunduğu bilgileri kullanıcıya sunacak.
* Kitabı almak isteyen olursa API'ın izin verdiği kadar epub olarak indirilebilir veya [Hattusa](hattusa.live) linkine yönlendirebilir.

Kalanı için issuelara bakabilirsiniz :)

**Katkıda Bulunmak İçin**

* Katkıda bulunmak için [issues](https://github.com/ilteriskeskin/cevrimici-kitap-galerisi/issues) sayfasından seçtiğiniz bir issueya yorum olarak
sizin görevi üstlendiğinizi belirtin.
* Sonrasında projeyi forklayın ve kendi bilgisayarınıza klonlayın.
* issue için gereklilikleri yaptıktan sonra push edin.
* Pull request açın ve kahvenizi yudumlayıp merge işlemini bekleyin :)
