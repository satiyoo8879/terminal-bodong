#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
BODONG CLI — ABSURD DIGITAL LAB UTILITY
"Build Your App, Not Your Limit. Dari Sampah Kode, Lahir Karya Luar Biasa."
===============================================================================
Perangkat baris perintah (CLI) serbaguna berbasis Python murni untuk:
1. Membersihkan folder cache dan file sampah proyek (Cache Sweeper).
2. Merapikan struktur direktori yang berantakan (Directory Organizer).
3. Membuat kerangka file boilerplate proyek otomatis (Boilerplate Generator).
4. Memindai statistik dan kesehatan direktori proyek (Project Radar).
===============================================================================
"""

from __future__ import annotations

import argparse
import datetime
import os
import shutil
import sys
import time
from pathlib import Path
from typing import Dict, List, Set, Tuple

APP_NAME = "BODONG CLI"
APP_VERSION = "1.0.0"
APP_TAGLINE = "Build Your App, Not Your Limit."


# =============================================================================
# 1. TERMINAL UI & ANSI STYLING (PYTHON MURNI)
# =============================================================================
class TermUI:
    """Mengelola warna ANSI, tabel terminal, dan komponen antarmuka interaktif."""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # Palet warna khas Limbah Bodong
    YELLOW = "\033[38;5;214m"   # Accent Kuning (#FFC52E)
    RED = "\033[38;5;203m"      # Merah Misil (#F04444)
    BLUE = "\033[38;5;75m"      # Biru Elektrik (#4AA8FF)
    GREEN = "\033[38;5;114m"    # Hijau Sukses
    GRAY = "\033[38;5;245m"     # Abu-abu Muted (#A5ADBA)
    WHITE = "\033[97m"

    @staticmethod
    def enable_windows_ansi() -> None:
        """Mengaktifkan dukungan urutan escape ANSI pada terminal Windows."""
        if os.name == "nt":
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                # ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
                handle = kernel32.GetStdHandle(-11)
                mode = ctypes.c_ulong()
                if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
                    kernel32.SetConsoleMode(handle, mode.value | 0x0004)
            except Exception:
                os.system("")

    @classmethod
    def banner(cls) -> None:
        """Menampilkan header ASCII misil Limbah Bodong."""
        art = f"""
{cls.YELLOW}{cls.BOLD}  ======================================================================={cls.RESET}
{cls.WHITE}{cls.BOLD}   _____ _____ ____  __  __ ___ _   _    _    _ 
  |_   _| ____|  _ \\|  \\/  |_ _| \\ | |  / \\  | |
    | | |  _| | |_) | |\\/| || ||  \\| | / _ \\ | |
    | | | |___|  _ <| |  | || || |\\  |/ ___ \\| |___
    |_| |_____|_| \\_\\_|  |_|___|_| \\_/_/   \\_\\_____|
          ____   ___  ____   ___  _   _  ____ 
         | __ ) / _ \\|  _ \\ / _ \\| \\ | |/ ___|
         |  _ \\| | | | | | | | | |  \\| | |  _ 
         | |_) | |_| | |_| | |_| | |\\  | |_| |
         |____/ \\___/|____/ \\___/|_| \\_|\\____|{cls.RESET}   {cls.RED}{cls.BOLD}[v{APP_VERSION}]{cls.RESET}

  {cls.YELLOW}>> LIMBAH BODONG — ABSURD DIGITAL LAB{cls.RESET}
  {cls.GRAY}"{APP_TAGLINE}"{cls.RESET}
{cls.YELLOW}{cls.BOLD}  ======================================================================={cls.RESET}"""
        print(art)

    @classmethod
    def info(cls, msg: str) -> None:
        print(f"  {cls.BLUE}[INFO]{cls.RESET} {msg}")

    @classmethod
    def success(cls, msg: str) -> None:
        print(f"  {cls.GREEN}[OK]{cls.RESET}   {msg}")

    @classmethod
    def warn(cls, msg: str) -> None:
        print(f"  {cls.YELLOW}[WARN]{cls.RESET} {msg}")

    @classmethod
    def error(cls, msg: str) -> None:
        print(f"  {cls.RED}[ERR]{cls.RESET}  {msg}")

    @classmethod
    def section(cls, title: str) -> None:
        print(f"\n  {cls.YELLOW}{cls.BOLD}:: {title.upper()}{cls.RESET}")
        print(f"  {cls.GRAY}{'-' * 68}{cls.RESET}")

    @classmethod
    def print_table(cls, headers: List[str], rows: List[List[str]]) -> None:
        """Mencetak tabel teks rapi secara dinamis tanpa library eksternal."""
        if not rows:
            return

        col_widths = [len(h) for h in headers]
        for row in rows:
            for idx, val in enumerate(row):
                if idx < len(col_widths):
                    col_widths[idx] = max(col_widths[idx], len(str(val)))

        sep = "  +" + "+".join("-" * (w + 2) for w in col_widths) + "+"
        header_line = "  |" + "|".join(
            f" {cls.YELLOW}{cls.BOLD}{headers[i]:<{col_widths[i]}}{cls.RESET} "
            for i in range(len(headers))
        ) + "|"

        print(sep)
        print(header_line)
        print(sep)
        for row in rows:
            row_line = "  |" + "|".join(
                f" {str(row[i]):<{col_widths[i]}} " for i in range(len(headers))
            ) + "|"
            print(row_line)
        print(sep)


# =============================================================================
# 2. FUNGSI HELPER UKURAN & KEAMANAN PATH
# =============================================================================
def format_bytes(size: int) -> str:
    """Mengubah ukuran byte menjadi format yang mudah dibaca (B, KB, MB, GB)."""
    float_size = float(max(size, 0))
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if float_size < 1024.0 or unit == "TB":
            return f"{float_size:.2f} {unit}" if unit != "B" else f"{int(float_size)} B"
        float_size /= 1024.0
    return f"{float_size:.2f} TB"


def get_path_size(path: Path) -> int:
    """Menghitung ukuran file atau akumulasi seluruh isi direktori."""
    if not path.exists():
        return 0
    if path.is_file() or path.is_symlink():
        try:
            return path.stat().st_size
        except OSError:
            return 0

    total = 0
    for root, _, files in os.walk(path):
        for f in files:
            fp = Path(root) / f
            try:
                if not fp.is_symlink():
                    total += fp.stat().st_size
            except OSError:
                continue
    return total


def confirm_action(prompt_text: str) -> bool:
    """Meminta konfirmasi [y/N] dari pengguna di terminal."""
    try:
        ans = input(f"\n  {TermUI.YELLOW}[?]{TermUI.RESET} {prompt_text} (y/N): ").strip().lower()
        return ans in ("y", "yes", "ya")
    except (KeyboardInterrupt, EOFError):
        print()
        return False


# =============================================================================
# 3. MODUL 1: PEMBERSIH CACHE PROYEK (CACHE SWEEPER)
# =============================================================================
CACHE_DIR_NAMES: Set[str] = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".cache",
    ".parcel-cache",
    ".next",
    ".nuxt",
    ".turbo",
    ".gradle",
    "build",
    "dist",
    "coverage",
    ".tox",
}

HEAVY_DIR_NAMES: Set[str] = {
    "node_modules",
    "vendor",
}

CACHE_FILE_NAMES: Set[str] = {
    ".ds_store",
    "thumbs.db",
    "desktop.ini",
    ".eslintcache",
}

CACHE_FILE_EXTENSIONS: Set[str] = {
    ".pyc",
    ".pyo",
    ".pyd",
    ".tmp",
    ".bak",
    ".swp",
    ".log",
    ".orig",
}

PROTECTED_DIRS: Set[str] = {
    ".git",
    ".svn",
    ".hg",
    ".idea",
    ".vscode",
    "venv",
    ".venv",
    "env",
}


def scan_cache_targets(
    base_dir: Path, include_heavy: bool = False
) -> List[Tuple[Path, str, int]]:
    """
    Memindai direktori untuk menemukan folder cache dan file sampah.
    Mengembalikan list tuple: (Path, Jenis, UkuranByte).
    """
    targets: List[Tuple[Path, str, int]] = []
    target_dirs = set(CACHE_DIR_NAMES)
    if include_heavy:
        target_dirs |= HEAVY_DIR_NAMES

    for root, dirs, files in os.walk(base_dir, topdown=True):
        # Jangan masuk ke folder terproteksi seperti .git atau .venv
        dirs[:] = [d for d in dirs if d not in PROTECTED_DIRS]

        matched_dirs = [d for d in dirs if d in target_dirs]
        for d in matched_dirs:
            full_dir = Path(root) / d
            size = get_path_size(full_dir)
            kind = "Heavy Dependency" if d in HEAVY_DIR_NAMES else "Folder Cache"
            targets.append((full_dir, kind, size))
            # Hentikan penelusuran ke dalam sub-folder yang sudah ditandai hapus
            dirs.remove(d)

        for f in files:
            f_lower = f.lower()
            full_file = Path(root) / f
            ext = full_file.suffix.lower()
            if f_lower in CACHE_FILE_NAMES or ext in CACHE_FILE_EXTENSIONS:
                size = get_path_size(full_file)
                targets.append((full_file, f"File Sampah ({ext or f_lower})", size))

    return targets


def run_cleaner(
    target_dir: str,
    dry_run: bool = False,
    include_heavy: bool = False,
    auto_yes: bool = False,
) -> None:
    """Menjalankan proses pembersihan cache proyek."""
    base_path = Path(target_dir).resolve()
    TermUI.section(f"Pembersih Cache Proyek — Target: {base_path}")

    if not base_path.exists() or not base_path.is_dir():
        TermUI.error(f"Direktori tidak ditemukan: {base_path}")
        return

    TermUI.info("Memindai tumpukan cache dan residu kompilasi...")
    found = scan_cache_targets(base_path, include_heavy=include_heavy)

    if not found:
        TermUI.success("Direktori sudah bersih! Tidak ada sampah cache yang ditemukan.")
        return

    rows: List[List[str]] = []
    total_bytes = 0
    for idx, (item_path, kind, size) in enumerate(found, start=1):
        total_bytes += size
        rel_path = str(item_path.relative_to(base_path))
        if len(rel_path) > 44:
            rel_path = "..." + rel_path[-41:]
        rows.append([str(idx), rel_path, kind, format_bytes(size)])

    TermUI.print_table(["No", "Lokasi Path", "Kategori", "Ukuran"], rows)
    print(
        f"\n  {TermUI.BOLD}Total Ditemukan:{TermUI.RESET} {len(found)} item "
        f"({TermUI.YELLOW}{TermUI.BOLD}{format_bytes(total_bytes)}{TermUI.RESET} potensi ruang lega)"
    )

    if dry_run:
        TermUI.warn("Mode Simulasi (--dry-run) aktif. Tidak ada file atau folder yang dihapus.")
        return

    if not auto_yes and not confirm_action("Eksekusi penghapusan seluruh item cache di atas?"):
        TermUI.warn("Operasi pembersihan dibatalkan oleh pengguna.")
        return

    deleted_count = 0
    freed_bytes = 0

    for item_path, _, size in found:
        try:
            if item_path.is_dir() and not item_path.is_symlink():
                shutil.rmtree(item_path)
            else:
                item_path.unlink(missing_ok=True)
            deleted_count += 1
            freed_bytes += size
        except Exception as exc:
            TermUI.error(f"Gagal menghapus {item_path.name}: {exc}")

    TermUI.success(
        f"Berhasil melenyapkan {deleted_count}/{len(found)} item! "
        f"Ruang penyimpanan lega: {TermUI.YELLOW}{TermUI.BOLD}{format_bytes(freed_bytes)}{TermUI.RESET}"
    )


# =============================================================================
# 4. MODUL 2: PERAPI DIREKTORI BERANTAKAN (DIRECTORY ORGANIZER)
# =============================================================================
CATEGORY_MAP: Dict[str, Set[str]] = {
    "images": {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico", ".bmp"},
    "documents": {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".md", ".rtf"},
    "archives": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"},
    "media": {".mp3", ".wav", ".ogg", ".flac", ".mp4", ".mkv", ".mov", ".avi", ".webm"},
    "data": {".json", ".csv", ".sql", ".xml", ".yaml", ".yml", ".db", ".sqlite"},
    "scripts_code": {".py", ".php", ".js", ".ts", ".html", ".css", ".sh", ".bat", ".c", ".cpp", ".ino"},
    "installers": {".exe", ".msi", ".dmg", ".deb", ".rpm", ".apk"},
}

PROTECTED_ROOT_FILES: Set[str] = {
    "bodong_cli.py",
    "bodong.bat",
    "readme.md",
    "license",
    ".gitignore",
    ".env",
    ".env.example",
    "composer.json",
    "composer.lock",
    "package.json",
    "package-lock.json",
    "requirements.txt",
    "pyproject.toml",
    "index.php",
    "app.php",
    "contact.php",
    "database.sql",
}


def determine_category(file_path: Path, mode: str = "type") -> str:
    """Menentukan nama folder tujuan berdasarkan tipe kategori atau ekstensi."""
    ext = file_path.suffix.lower()
    if mode == "ext":
        return ext.lstrip(".") if ext else "tanpa_ekstensi"

    for folder_name, extensions in CATEGORY_MAP.items():
        if ext in extensions:
            return folder_name
    return "others"


def safe_destination_path(dest_dir: Path, filename: str) -> Path:
    """Mencegah penimpaan file dengan menambahkan sufiks angka jika nama sudah ada."""
    candidate = dest_dir / filename
    if not candidate.exists():
        return candidate

    stem = Path(filename).stem
    suffix = Path(filename).suffix
    counter = 1
    while True:
        new_name = f"{stem}_{counter}{suffix}"
        candidate = dest_dir / new_name
        if not candidate.exists():
            return candidate
        counter += 1


def run_tidy(
    target_dir: str,
    mode: str = "type",
    dry_run: bool = False,
    auto_yes: bool = False,
) -> None:
    """Merapikan file yang tercecer di satu direktori ke dalam sub-folder terstruktur."""
    base_path = Path(target_dir).resolve()
    TermUI.section(f"Perapi Direktori Berantakan — Target: {base_path}")

    if not base_path.exists() or not base_path.is_dir():
        TermUI.error(f"Direktori tidak ditemukan: {base_path}")
        return

    plans: List[Tuple[Path, Path, str]] = []
    script_self = Path(__file__).resolve()

    for item in sorted(base_path.iterdir()):
        if not item.is_file() or item.is_symlink():
            continue
        if item.resolve() == script_self:
            continue
        if item.name.startswith(".") or item.name.lower() in PROTECTED_ROOT_FILES:
            continue

        category_folder = determine_category(item, mode=mode)
        dest_dir = base_path / category_folder
        dest_path = safe_destination_path(dest_dir, item.name)
        plans.append((item, dest_path, category_folder))

    if not plans:
        TermUI.success("Tidak ada file berantakan yang perlu dipindahkan di direktori ini.")
        return

    rows: List[List[str]] = []
    for idx, (src, dst, cat) in enumerate(plans, start=1):
        rows.append([
            str(idx),
            src.name[:32],
            f"{cat}/",
            dst.name[:32],
            format_bytes(get_path_size(src)),
        ])

    TermUI.print_table(["No", "File Asal", "Folder Tujuan", "Nama Akhir", "Ukuran"], rows)
    print(f"\n  {TermUI.BOLD}Total File Akan Dirapikan:{TermUI.RESET} {len(plans)} file")

    if dry_run:
        TermUI.warn("Mode Simulasi (--dry-run) aktif. Tidak ada file yang dipindahkan.")
        return

    if not auto_yes and not confirm_action("Pindahkan dan rapikan file sesuai tabel di atas?"):
        TermUI.warn("Operasi perapian direktori dibatalkan.")
        return

    moved_count = 0
    for src, dst, _ in plans:
        try:
            dst.parent.mkdir(parents=True, exist_ok=True)
            # Hitung ulang path aman apabila ada file bernama sama pada batch yang sama
            final_dst = safe_destination_path(dst.parent, src.name)
            shutil.move(str(src), str(final_dst))
            moved_count += 1
        except Exception as exc:
            TermUI.error(f"Gagal memindahkan {src.name}: {exc}")

    TermUI.success(f"Selesai! {moved_count}/{len(plans)} file berhasil dirapikan ke dalam sub-folder.")


# =============================================================================
# 5. MODUL 3: PEMBUAT KERANGKA BOILERPLATE (BOILERPLATE GENERATOR)
# =============================================================================
def get_boilerplate_templates(project_name: str) -> Dict[str, Dict[str, str]]:
    """Menyediakan koleksi template proyek siap pakai."""
    year = datetime.datetime.now().year
    slug = project_name.lower().replace(" ", "-").replace("_", "-")

    return {
        "php-native": {
            ".gitignore": "/vendor/\n/.env\n*.log\n.DS_Store\nThumbs.db\n",
            "README.md": (
                f"# {project_name}\n\n"
                f"Proyek **PHP Native + PDO + Tailwind CSS** hasil generatasi otomatis **Bodong CLI**.\n\n"
                f"## Cara Menjalankan\n"
                f"1. Letakkan folder `{slug}` di dalam `laragon/www/` atau `xampp/htdocs/`.\n"
                f"2. Sesuaikan konfigurasi database pada `config/database.php`.\n"
                f"3. Buka `http://localhost/{slug}` di browser.\n"
            ),
            "config/database.php": (
                "<?php\n"
                "declare(strict_types=1);\n\n"
                "define('DB_HOST', 'localhost');\n"
                f"define('DB_NAME', '{slug.replace('-', '_')}');\n"
                "define('DB_USER', 'root');\n"
                "define('DB_PASS', '');\n\n"
                "function e(?string $str): string {\n"
                "    return htmlspecialchars((string) ($str ?? ''), ENT_QUOTES, 'UTF-8');\n"
                "}\n"
            ),
            "assets/css/style.css": (
                "/* Custom Stylesheet — Generated by Bodong CLI */\n"
                ":root {\n"
                "    --bg-dark: #0B0D12;\n"
                "    --accent-yellow: #FFC52E;\n"
                "}\n"
            ),
            "assets/js/main.js": (
                "document.addEventListener('DOMContentLoaded', () => {\n"
                f"    console.log('{project_name} siap dijalankan!');\n"
                "});\n"
            ),
            "index.php": (
                "<?php\n"
                "require_once __DIR__ . '/config/database.php';\n"
                f"$title = '{project_name}';\n"
                "?>\n"
                "<!DOCTYPE html>\n"
                "<html lang=\"id\">\n"
                "<head>\n"
                "    <meta charset=\"UTF-8\">\n"
                "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
                "    <title><?= e($title) ?></title>\n"
                "    <script src=\"https://cdn.tailwindcss.com\"></script>\n"
                "    <link rel=\"stylesheet\" href=\"assets/css/style.css\">\n"
                "</head>\n"
                "<body class=\"bg-[#0B0D12] text-[#F7F7F5] min-h-screen flex items-center justify-center p-6\">\n"
                "    <main class=\"max-w-xl w-full bg-[#171B24] border border-[#2A303B] rounded-2xl p-8 space-y-4\">\n"
                "        <span class=\"inline-block px-3 py-1 rounded bg-[#FFC52E] text-[#0B0D12] font-mono text-xs font-bold\">\n"
                "            BODONG CLI BOILERPLATE\n"
                "        </span>\n"
                "        <h1 class=\"text-3xl font-extrabold tracking-tight\"><?= e($title) ?></h1>\n"
                "        <p class=\"text-[#A5ADBA] text-sm leading-relaxed\">\n"
                "            Kerangka proyek PHP Native telah siap. Edit file <code class=\"text-[#FFC52E]\">index.php</code> untuk mulai membangun eksperimenmu.\n"
                "        </p>\n"
                f"        <footer class=\"pt-4 border-t border-[#2A303B] text-xs text-[#A5ADBA] font-mono\">&copy; {year} {project_name}</footer>\n"
                "    </main>\n"
                "    <script src=\"assets/js/main.js\"></script>\n"
                "</body>\n"
                "</html>\n"
            ),
        },
        "web-static": {
            ".gitignore": ".DS_Store\nThumbs.db\n*.log\n",
            "README.md": f"# {project_name}\n\nStarter kit Web Statis (HTML5 + Tailwind CSS + Vanilla JS) buatan **Bodong CLI**.\n",
            "assets/css/style.css": "/* Custom CSS */\nhtml { scroll-behavior: smooth; }\n",
            "assets/js/app.js": (
                "document.addEventListener('DOMContentLoaded', () => {\n"
                f"    console.log('[{project_name}] Lab Digital Aktif.');\n"
                "});\n"
            ),
            "index.html": (
                "<!DOCTYPE html>\n"
                "<html lang=\"id\">\n"
                "<head>\n"
                "    <meta charset=\"UTF-8\">\n"
                "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
                f"    <title>{project_name}</title>\n"
                "    <script src=\"https://cdn.tailwindcss.com\"></script>\n"
                "    <link rel=\"stylesheet\" href=\"assets/css/style.css\">\n"
                "</head>\n"
                "<body class=\"bg-[#0B0D12] text-[#F7F7F5] min-h-screen flex items-center justify-center p-6\">\n"
                "    <div class=\"max-w-lg w-full bg-[#171B24] border border-[#2A303B] rounded-2xl p-8\">\n"
                "        <p class=\"font-mono text-xs text-[#FFC52E] uppercase tracking-widest mb-2\">STATIC WEB STARTER</p>\n"
                f"        <h1 class=\"text-3xl font-extrabold mb-3\">{project_name}</h1>\n"
                "        <p class=\"text-sm text-[#A5ADBA] leading-relaxed\">Struktur dasar HTML5, Tailwind CDN, dan Vanilla JS siap dimodifikasi.</p>\n"
                "    </div>\n"
                "    <script src=\"assets/js/app.js\"></script>\n"
                "</body>\n"
                "</html>\n"
            ),
        },
        "python-app": {
            ".gitignore": "__pycache__/\n*.py[cod]\n.venv/\nvenv/\n.env\n.pytest_cache/\n",
            "README.md": (
                f"# {project_name}\n\n"
                f"Kerangka aplikasi Python modular yang dibuat otomatis dengan **Bodong CLI**.\n\n"
                f"## Eksekusi\n"
                f"```bash\n"
                f"python main.py\n"
                f"```\n"
            ),
            "requirements.txt": "# Tambahkan dependensi paket Python di sini\n",
            "src/__init__.py": f'"""Paket utama {project_name}."""\n',
            "src/core.py": (
                "def run_app() -> None:\n"
                f'    print("[{project_name}] Aplikasi Python berhasil dijalankan!")\n'
            ),
            "tests/__init__.py": "",
            "main.py": (
                "#!/usr/bin/env python3\n"
                "# -*- coding: utf-8 -*-\n"
                "from src.core import run_app\n\n"
                "if __name__ == '__main__':\n"
                "    run_app()\n"
            ),
        },
    }


def run_init_boilerplate(
    project_name: str,
    template_key: str = "php-native",
    dest_root: str = ".",
) -> None:
    """Membuat folder proyek baru beserta seluruh kerangka file boilerplate."""
    clean_name = project_name.strip()
    if not clean_name:
        TermUI.error("Nama proyek tidak boleh kosong.")
        return

    templates = get_boilerplate_templates(clean_name)
    if template_key not in templates:
        TermUI.error(
            f"Template '{template_key}' tidak dikenali. Pilihan: {', '.join(templates.keys())}"
        )
        return

    folder_slug = clean_name.lower().replace(" ", "-")
    project_dir = (Path(dest_root).resolve() / folder_slug)

    TermUI.section(f"Boilerplate Generator — Proyek: {clean_name} ({template_key})")

    if project_dir.exists() and any(project_dir.iterdir()):
        TermUI.error(f"Folder tujuan '{project_dir}' sudah ada dan tidak kosong!")
        return

    file_map = templates[template_key]
    created_rows: List[List[str]] = []

    try:
        project_dir.mkdir(parents=True, exist_ok=True)
        for idx, (rel_file_path, content) in enumerate(file_map.items(), start=1):
            full_path = project_dir / rel_file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding="utf-8")
            created_rows.append([
                str(idx),
                rel_file_path,
                format_bytes(len(content.encode("utf-8"))),
                "Dibuat",
            ])

        # Tambahkan folder uploads/.gitkeep untuk php-native
        if template_key == "php-native":
            gitkeep = project_dir / "uploads" / ".gitkeep"
            gitkeep.parent.mkdir(parents=True, exist_ok=True)
            gitkeep.write_text("", encoding="utf-8")
            created_rows.append([str(len(created_rows) + 1), "uploads/.gitkeep", "0 B", "Dibuat"])

        TermUI.print_table(["No", "File Boilerplate", "Ukuran", "Status"], created_rows)
        TermUI.success(f"Proyek '{clean_name}' siap digunakan di: {project_dir}")
    except Exception as exc:
        TermUI.error(f"Gagal membuat kerangka proyek: {exc}")


# =============================================================================
# 6. MODUL 4: PEMINDAI STATISTIK DIREKTORI (PROJECT RADAR)
# =============================================================================
def run_project_scan(target_dir: str) -> None:
    """Memindai statistik jumlah file, ekstensi teratas, dan potensi sampah cache."""
    base_path = Path(target_dir).resolve()
    TermUI.section(f"Project Radar — Analisis Direktori: {base_path}")

    if not base_path.exists() or not base_path.is_dir():
        TermUI.error(f"Direktori tidak ditemukan: {base_path}")
        return

    ext_stats: Dict[str, List[int]] = {}
    total_files = 0
    total_dirs = 0
    total_size = 0

    for root, dirs, files in os.walk(base_path):
        dirs[:] = [d for d in dirs if d != ".git"]
        total_dirs += len(dirs)
        for f in files:
            fp = Path(root) / f
            try:
                fsize = fp.stat().st_size if not fp.is_symlink() else 0
            except OSError:
                fsize = 0
            total_files += 1
            total_size += fsize
            ext = fp.suffix.lower() or "(tanpa ekstensi)"
            if ext not in ext_stats:
                ext_stats[ext] = [0, 0]
            ext_stats[ext][0] += 1
            ext_stats[ext][1] += fsize

    sorted_exts = sorted(ext_stats.items(), key=lambda x: x[1][1], reverse=True)[:8]
    rows = [
        [ext, str(data[0]), format_bytes(data[1])]
        for ext, data in sorted_exts
    ]

    if rows:
        TermUI.print_table(["Ekstensi File", "Jumlah File", "Total Ukuran"], rows)

    cache_items = scan_cache_targets(base_path, include_heavy=False)
    cache_bytes = sum(item[2] for item in cache_items)

    print(f"\n  {TermUI.BOLD}Ringkasan Laboratorium:{TermUI.RESET}")
    print(f"  - Total Sub-folder : {total_dirs}")
    print(f"  - Total File       : {total_files}")
    print(f"  - Ukuran Proyek    : {TermUI.BLUE}{format_bytes(total_size)}{TermUI.RESET}")
    print(
        f"  - Residu Cache     : {len(cache_items)} item "
        f"({TermUI.YELLOW}{format_bytes(cache_bytes)}{TermUI.RESET})"
    )


# =============================================================================
# 7. MODE MENU TERMINAL INTERAKTIF
# =============================================================================
def interactive_menu() -> None:
    """Menjalankan antarmuka interaktif berbasis menu di terminal."""
    TermUI.banner()

    while True:
        cwd = str(Path.cwd())
        print(f"\n  {TermUI.GRAY}Lokasi Aktif: {cwd}{TermUI.RESET}")
        print(f"  {TermUI.YELLOW}[1]{TermUI.RESET} Bersihkan Folder Cache & Sampah Proyek (Clean)")
        print(f"  {TermUI.YELLOW}[2]{TermUI.RESET} Rapikan Struktur Direktori Berantakan (Tidy)")
        print(f"  {TermUI.YELLOW}[3]{TermUI.RESET} Buat Kerangka File Boilerplate Baru (Init)")
        print(f"  {TermUI.YELLOW}[4]{TermUI.RESET} Pindai Statistik & Kesehatan Direktori (Scan)")
        print(f"  {TermUI.RED}[0]{TermUI.RESET} Keluar dari Bodong CLI")

        try:
            choice = input(f"\n  {TermUI.YELLOW}bodong-cli >{TermUI.RESET} Pilih menu [0-4]: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n")
            TermUI.info("Sampai jumpa di eksperimen berikutnya!")
            break

        if choice == "0":
            TermUI.info("Keluar dari laboratorium. Build • Break • Repeat!")
            break

        elif choice == "1":
            target = input("  Masukkan path folder target (kosongkan untuk folder saat ini): ").strip() or "."
            heavy_ans = input("  Sertakan node_modules & vendor? (y/N): ").strip().lower()
            sim_ans = input("  Jalankan mode simulasi / dry-run terlebih dahulu? (y/N): ").strip().lower()
            run_cleaner(
                target_dir=target,
                dry_run=sim_ans in ("y", "yes", "ya"),
                include_heavy=heavy_ans in ("y", "yes", "ya"),
            )

        elif choice == "2":
            target = input("  Masukkan path folder yang ingin dirapikan (default '.'): ").strip() or "."
            mode_in = input("  Mode pengelompokan — [1] Kategori Tipe File, [2] Ekstensi (default 1): ").strip()
            mode = "ext" if mode_in == "2" else "type"
            sim_ans = input("  Jalankan mode simulasi / dry-run terlebih dahulu? (y/N): ").strip().lower()
            run_tidy(
                target_dir=target,
                mode=mode,
                dry_run=sim_ans in ("y", "yes", "ya"),
            )

        elif choice == "3":
            proj_name = input("  Nama proyek baru (contoh: Kasir Bodong): ").strip()
            print("  Pilihan Template:")
            print("    1. php-native  (PHP Native + PDO + Tailwind CSS)")
            print("    2. web-static  (HTML5 + Tailwind CSS + Vanilla JS)")
            print("    3. python-app  (Struktur Aplikasi Python Modular)")
            tpl_choice = input("  Pilih nomor atau nama template [1-3] (default 1): ").strip()
            tpl_map = {"1": "php-native", "2": "web-static", "3": "python-app"}
            tpl_key = tpl_map.get(tpl_choice, tpl_choice or "php-native")
            dest = input("  Lokasi pembuatan folder (kosongkan untuk direktori saat ini): ").strip() or "."
            run_init_boilerplate(project_name=proj_name, template_key=tpl_key, dest_root=dest)

        elif choice == "4":
            target = input("  Masukkan path direktori yang ingin dipindai (default '.'): ").strip() or "."
            run_project_scan(target_dir=target)

        else:
            TermUI.warn("Pilihan tidak valid. Silakan masukkan angka 0 sampai 4.")


# =============================================================================
# 8. PARSER ARGUMEN BARIS PERINTAH (CLI SUBCOMMANDS)
# =============================================================================
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bodong",
        description=f"{APP_NAME} v{APP_VERSION} — {APP_TAGLINE}",
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-perintah utama Bodong CLI")

    # Subcommand: clean
    p_clean = subparsers.add_parser("clean", help="Bersihkan folder cache dan file residu proyek")
    p_clean.add_argument("path", nargs="?", default=".", help="Path direktori target (default: .)")
    p_clean.add_argument("--dry-run", action="store_true", help="Simulasi tanpa menghapus file")
    p_clean.add_argument("--heavy", action="store_true", help="Sertakan node_modules dan vendor")
    p_clean.add_argument("-y", "--yes", action="store_true", help="Langsung eksekusi tanpa konfirmasi")

    # Subcommand: tidy
    p_tidy = subparsers.add_parser("tidy", help="Rapikan file berantakan ke dalam sub-folder kategori")
    p_tidy.add_argument("path", nargs="?", default=".", help="Path direktori target (default: .)")
    p_tidy.add_argument(
        "--mode",
        choices=["type", "ext"],
        default="type",
        help="Kelompokkan berdasarkan kategori tipe ('type') atau ekstensi ('ext')",
    )
    p_tidy.add_argument("--dry-run", action="store_true", help="Simulasi tanpa memindahkan file")
    p_tidy.add_argument("-y", "--yes", action="store_true", help="Langsung eksekusi tanpa konfirmasi")

    # Subcommand: init
    p_init = subparsers.add_parser("init", help="Buat kerangka file boilerplate proyek baru")
    p_init.add_argument("name", help="Nama proyek yang ingin dibuat")
    p_init.add_argument(
        "-t",
        "--template",
        choices=["php-native", "web-static", "python-app"],
        default="php-native",
        help="Pilihan template boilerplate (default: php-native)",
    )
    p_init.add_argument("-d", "--dest", default=".", help="Direktori tujuan pembuatan proyek")

    # Subcommand: scan
    p_scan = subparsers.add_parser("scan", help="Pindai statistik ukuran dan kesehatan direktori")
    p_scan.add_argument("path", nargs="?", default=".", help="Path direktori target (default: .)")

    return parser


def main() -> None:
    TermUI.enable_windows_ansi()
    parser = build_parser()

    if len(sys.argv) == 1:
        interactive_menu()
        return

    args = parser.parse_args()
    TermUI.banner()

    if args.command == "clean":
        run_cleaner(
            target_dir=args.path,
            dry_run=args.dry_run,
            include_heavy=args.heavy,
            auto_yes=args.yes,
        )
    elif args.command == "tidy":
        run_tidy(
            target_dir=args.path,
            mode=args.mode,
            dry_run=args.dry_run,
            auto_yes=args.yes,
        )
    elif args.command == "init":
        run_init_boilerplate(
            project_name=args.name,
            template_key=args.template,
            dest_root=args.dest,
        )
    elif args.command == "scan":
        run_project_scan(target_dir=args.path)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()