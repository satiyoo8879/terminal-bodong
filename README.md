# 🚀 TERMINAL BODONG (Bodong CLI)

> **"Build Your App, Not Your Limit."**  
> *Dari Sampah Kode, Lahir Karya Luar Biasa.*

![Python](https://img.shields.io/badge/Python-3.7+-blue?style=flat-square&logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/Dependencies-0%20(Pure%20Python)-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Win%20%7C%20Linux%20%7C%20macOS-lightgray?style=flat-square)

**Terminal Bodong** adalah perangkat baris perintah (*Command Line Interface*) serbaguna yang dirancang khusus untuk mempercepat alur kerja *developer* di lingkungan lokal. 

Dibangun menggunakan **Python murni (100% Standard Library)** tanpa memerlukan paket eksternal via `pip`. Ringan, portabel, dan langsung bisa dijalankan di Windows (CMD / PowerShell / Terminal Laragon), Linux, maupun macOS.

---

## ✨ Fitur Utama

- 🧹 **Cache Sweeper (`clean`)**
  Membersihkan folder sampah kompilasi (`__pycache__`, `.pytest_cache`, `build/`, `dist/`) dan file residu secara aman untuk melegakan ruang penyimpanan. Tersedia mode `--heavy` untuk melibas `node_modules` atau `vendor`.
- 🗂️ **Directory Organizer (`tidy`)**
  Merapikan file yang berserakan di satu folder ke dalam sub-folder yang terstruktur rapi berdasarkan kategori (Images, Documents, Scripts, dll) atau berdasarkan ekstensi file.
- 🏗️ **Boilerplate Generator (`init`)**
  Membuat kerangka proyek (*starter kit*) siap pakai hanya dalam hitungan detik. Tersedia untuk PHP Native, Web Statis, dan Python modular.
- 📡 **Project Radar (`scan`)**
  Memindai statistik direktori, menghitung total ukuran file, menampilkan ekstensi terbanyak, dan mendeteksi ukuran sampah *cache* yang bersembunyi.
- 🛡️ **Safe Mode (`--dry-run`)**
  Ragu menghapus atau memindahkan file? Gunakan bendera `--dry-run` untuk menyimulasikan proses dan melihat daftar file tanpa memodifikasi satu byte pun data asli Anda.

---

## ⚙️ Persyaratan Sistem

- **Python 3.7** atau lebih baru terpasang di sistem operasi Anda.
- *Zero dependencies* — Tidak perlu `pip install -r requirements.txt`.

---

## 🚀 Cara Instalasi

### 1. Clone Repositori
```bash
git clone [https://github.com/username/terminal-bodong.git](https://github.com/username/terminal-bodong.git)
cd terminal-bodong