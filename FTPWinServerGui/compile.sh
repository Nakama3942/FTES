#!/bin/bash
pyinstaller --onefile --name ftess --noconsole main.pyw

# Удаление ненужной директории и файла
rm -rf build
rm ftess.spec

# Копирование директорий в dist
cp -r font dist/
cp -r icon dist/
cp -r style dist/

# Переименование dist
mv dist FTES-WSG