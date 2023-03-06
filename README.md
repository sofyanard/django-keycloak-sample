##### django-keycloak-sample

# Contoh Auth Django Apps dengan Keycloak / RH-SSO

### A. Django Project

Di contoh ini, aplikasi Django yang kita buat berjalan di http://localhost:8000


### B. Django / Python Library

Menambahkan library django-allauth
```codetype
pip install django-allauth
```


### C. Keycloak / RH-SSO Configuration

Buat realm dan client, misal:
* Realm: myrealm
* Client: testclient

Set Access Type jadi: confidential

Kemudian tambahkan Valid Redirect Urls:
http://localhost:8000/accounts/openid_connect/login/callback/


### D. ``` settings.py ``` Configuration

```codetype
INSTALLED_APPS = [
	……
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.keycloak',
]
```

```codetype
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]
```

```codetype
SOCIALACCOUNT_PROVIDERS = { # changed
        'keycloak': {
        'KEYCLOAK_URL': 'http://localhost:8080/auth',
        'KEYCLOAK_REALM': 'myrealm',
    },
}
```

```codetype
SITE_ID = 2
```
```SITE_ID``` ini disesuaikan dengan konfigurasi site di bagian Django-Admin

```codetype
LOGIN_REDIRECT_URL = '/hello'
```
```LOGIN_REDIRECT_URL``` ini endpoint yang akan dipanggil setelah authentikasi sukses


### E. ``` urls.py ``` Configuration

```codetype
from django.contrib import admin
from django.urls import path, include
from . import hello

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('hello/', hello.hello_world, name='hello_world'),
]
```


### F. Django-Admin Configuration

Tambahkan Site: localhost:8000

* sebelumnya sudah ada site ```example.com``` dengan ```SITE_ID``` = 1 \
sehingga site yang baru kita tambahkan akan memiliki ```SITE_ID``` = 2 \
```SITE_ID``` ini harus sesuai dengan yang kita set di ```settings.py```

Kemudian tambahkan Social Application
* Provider: Keycloak
* Client Id: testclient (sesuai dengan client-id di keycloak)
* Secret Key: [client-secret] (sesuai dengan client-secret di keycloak)
* Choosen Sites: tambahkan localhost:8000 (sesuai dengan aplikasi django kita)


### G. Test

Membuka login page: http://localhost:8000/accounts/login

### CATATAN:
2023-03-06: based on https://github.com/GeoNode/geonode/issues/9311 ..\
tambahkan di ```settings.py``` : ```SOCIALACCOUNT_LOGIN_ON_GET=True```\
dan di file ```requirements.txt``` ubah versi ```django-allauth``` ke 0.44.0\
(thanks to https://github.com/edwin)


### Referensi: 

```django-allauth``` documentation
https://django-allauth.readthedocs.io/en/latest/installation.html

https://gist.github.com/t-book/0fb30804e217bdeb064dd91b5041fbc9

https://github.com/GeoNode/geonode/issues/9311

