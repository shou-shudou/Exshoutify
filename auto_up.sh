#!/bin/bash

# ==== Konfigurasi ====
FOLDER_PROJECT=~/github  # Ganti dengan folder tempat scriptmu
REPO_URL=https://github.com/ShouShudou/Exshoutify.git
BRANCH=master            # Ganti ke main kalau repo pakai main

# Pindah ke folder project
cd "$FOLDER_PROJECT" || { echo "Folder project tidak ditemukan!"; exit 1; }

# Cek apakah remote origin sudah ada
git remote get-url origin >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Remote origin tidak ditemukan, menambahkan..."
    git remote add origin $REPO_URL
fi

# Tambahkan semua perubahan
git add .

# Commit dengan timestamp (hanya jika ada perubahan)
git commit -m "Update script otomatis $(date +"%Y-%m-%d %H:%M:%S")" 2>/dev/null || echo "Tidak ada perubahan untuk commit."

# Push ke GitHub
git push origin $BRANCH
