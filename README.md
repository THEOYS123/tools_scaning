# *tools ini adalah alat pemindaian keamanan untuk website WordPress dengan fokus pada beberapa aspek penting:*

`

1. Pemindaian Jalur Sensitif: Memeriksa file dan direktori yang rentan di WordPress seperti wp-config.php, readme.html, dan .htaccess yang dapat mengungkapkan informasi sensitif atau berisiko.


2. Pemindaian Plugin Rentan: Memeriksa plugin WordPress yang terkenal memiliki kerentanannya, seperti Elementor, WooCommerce, dan UpdraftPlus, untuk potensi celah keamanan.


3. Pemindaian API Endpoint: Mengidentifikasi endpoint API di situs WordPress yang bisa terekspos dan digunakan untuk eksploitasi, seperti /wp-json/wp/v2/users/.


4. Pemindaian XSS (Cross-Site Scripting): Menguji parameter URL untuk celah XSS, menggunakan payload berbahaya untuk menguji apakah situs dapat terinfeksi dengan skrip berbahaya yang dapat mencuri data pengguna.


5. Rotasi User-Agent dan Proxy: Menggunakan rotasi user-agent dan proxy untuk menghindari pemblokiran oleh server dan untuk melindungi identitas selama pemindaian.


6. Mekanisme Retry: Jika permintaan HTTP gagal (misalnya error 500), script akan mencoba mengulang permintaan tersebut hingga 3 kali.


7. Hasil Pemindaian: Hasil pemindaian disimpan dalam format JSON untuk referensi lebih lanjut, mencatat URL yang ditemukan, status respons, dan hasil dari pemindaian XSS.



tools ini efektif untuk membantu mengidentifikasi celah keamanan di situs WordPress secara otomatis dan mendalam, serta menjaga privasi dengan menggunakan rotasi proxy dan user-agent.

`

---


# install && run
```
pkg update -y
pkg upgrade -y
pkg update && pkg upgrade -y
pip install requests termcolor fpdf
pkg install art
pkg install socket
git clone https://github.com/THEOYS123/tools_scaning.git
cd tools_scaning
python scan.py
```

# update tools 
```
cd tools_scaning
git pull
python scan.py
```

# install ulang tools
```
cd
rm -rf tools_scaning
pip install requests termcolor fpdf
pkg install art
git clone https://github.com/THEOYS123/tools_scaning.git
cd tools_scaning
python scan.py
```

# *Applications that can be used to scan pdf results 🌐*
```
> chrome/browser lainnya
> Microsoft Word
> canava
> google Drive
> WPS Office
```

# *📸screenshot hasil📸*

<p align="center">
  <a href="https://g.top4top.io/p_33173xdew5.jpg">
    <img src="https://g.top4top.io/p_33173xdew5.jpg" width="1500" height="900" />
  </a>
</p>


⚠️⚠️⚠️
> tools by RenXploit

> contact: 62895365187210
