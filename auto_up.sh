#!/bin/bash

# Folder project
cd /data/data/com.termux/files/home/folder_script  # Ganti sesuai path folder scriptmu

# Tambahkan semua perubahan
git add .

# Commit dengan timestamp
git commit -m "Update script otomatis $(date +"%Y-%m-%d %H:%M:%S")" || echo "Tidak ada perubahan"

# Push ke GitHub
git push origin main
