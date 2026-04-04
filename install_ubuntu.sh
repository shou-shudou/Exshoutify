#!/bin/bash

# Script to set up a virtual environment for Python on Ubuntu

# Update package list and install prerequisites
echo "Updating package list..."
sudo apt update -y

echo "Installing Python3 and venv..."
sudo apt install python3 python3-venv -y

# Create a directory for the project
read -p "Enter the project directory name: " project_dir
echo "Creating project directory: $project_dir"
mkdir -p "$project_dir"
cd "$project_dir" || exit

# Create a virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

echo "Virtual environment setup complete!"
echo "To activate the virtual environment, use: source venv/bin/activate"