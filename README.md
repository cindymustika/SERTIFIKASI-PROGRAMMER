# Restaurant Management System

Aplikasi manajemen restoran berbasis Python dengan GUI Tkinter untuk mengelola pelanggan, meja, dan reservasi.

## Deskripsi

Restaurant Management System adalah aplikasi desktop yang memungkinkan staf restoran atau manajer untuk mengelola operasional reservasi dengan efisien. Sistem ini menyediakan antarmuka yang mudah digunakan untuk melakukan operasi CRUD (Create, Read, Update, Delete) pada data pelanggan, meja, dan reservasi.

## Fitur

### Manajemen Pelanggan
- Menambahkan pelanggan baru dengan nama dan nomor telepon
- Melihat daftar semua pelanggan
- Memperbarui informasi pelanggan
- Menghapus data pelanggan

### Manajemen Meja
- Menambahkan meja baru dengan nomor dan kapasitas
- Melihat daftar meja beserta statusnya (available/booked)
- Memperbarui informasi meja
- Menghapus meja yang tidak sedang dibooking

### Manajemen Reservasi
- Membuat reservasi baru dengan memilih pelanggan dan meja
- Melihat semua reservasi yang ada
- Memperbarui detail reservasi
- Membatalkan reservasi (otomatis mengubah status meja menjadi available)

## Struktur Proyek

```
restaurant_app/
├── .venv/                  # Virtual environment
├── src/                    # Source code utama
│   ├── __init__.py
│   ├── customer.py         # Model dan repository Pelanggan
│   ├── database.py         # Koneksi dan setup database
│   ├── gui.py              # GUI aplikasi (Tkinter)
│   ├── main.py             # Entry point aplikasi
│   ├── reporting.py        # Fungsi pelaporan
│   ├── reservation.py      # Model dan repository Reservasi
│   └── table.py            # Model dan repository Meja
└── tests/                  # Unit tests
    ├── __init__.py
    ├── test_customer.py
    ├── test_reservation.py
    └── test_table.py
```

## Teknologi

- Python 3.x
- Tkinter - GUI framework
- MySQL - Database
- pytest - Testing framework

## Instalasi

1. Clone repository
   ```bash
   git clone <repository-url>
   cd restaurant_app
   ```

2. Buat virtual environment
   ```bash
   python -m venv .venv
   ```

3. Aktifkan virtual environment
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source .venv/bin/activate
     ```



## Cara Menggunakan

1. Pastikan virtual environment sudah diaktifkan

2. Jalankan aplikasi:
   ```bash
   python src/main.py
   ```
   
   atau
   
   ```bash
   cd src
   python main.py
   ```

## Menjalankan Tests

Jalankan semua tests:

```bash
pytest tests/
```

Jalankan file test tertentu:

```bash
pytest tests/test_customer.py
pytest tests/test_table.py
pytest tests/test_reservation.py
```

## Skema Database

### Tabel CUSTOMER
| Field | Type    | Deskripsi         |
|-------|---------|-------------------|
| id    | INTEGER | Primary Key       |
| name  | TEXT    | Nama pelanggan    |
| phone | TEXT    | Nomor telepon     |

### Tabel TABLE
| Field    | Type    | Deskripsi                |
|----------|---------|--------------------------|
| id       | INTEGER | Primary Key              |
| number   | TEXT    | Nomor meja               |
| capacity | INTEGER | Kapasitas meja           |
| status   | TEXT    | Status (available/booked)|

### Tabel RESERVATION
| Field       | Type    | Deskripsi             |
|-------------|---------|----------------------|
| id          | INTEGER | Primary Key          |
| customer_id | INTEGER | Foreign Key (CUSTOMER)|
| table_id    | INTEGER | Foreign Key (TABLE)  |
| date        | TEXT    | Tanggal reservasi    |
| time        | TEXT    | Waktu reservasi      |

