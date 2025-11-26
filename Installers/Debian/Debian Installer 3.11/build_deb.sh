#!/bin/bash

echo "Подготовка к сборке DEB пакета для Python 3.11..."

# Переменные
PACKAGE_NAME="calculator"
VERSION="1.0.8"
PYTHON_VERSION="3.11"
BUILD_DIR="build_deb"
PACKAGE_DIR="${BUILD_DIR}/${PACKAGE_NAME}-${VERSION}"

# Очистка предыдущей сборки
rm -rf "${BUILD_DIR}"
mkdir -p "${BUILD_DIR}"

# Сборка бинарного файла из исходников
echo "Установка зависимостей для сборки..."
apt-get update
apt-get install -y python3.11 python3.11-dev python3.11-tk python3-pip

echo "Установка PyInstaller..."
python3.11 -m pip install --upgrade pip
pip install pyinstaller --break-system-packages

echo "Сборка исполняемого файла..."
python3.11 -m PyInstaller \
    --onefile \
    --windowed \
    --name "calculator-Linux-${PYTHON_VERSION}" \
    --distpath "./dist" \
    --workpath "./build" \
    --specpath "./spec" \
    ../../../calculator.py

if [ $? -ne 0 ]; then
    echo "Ошибка при сборке бинарного файла"
    exit 1
fi

echo "Бинарный файл успешно создан"

# 2. Создание структуры DEB пакета
echo "Создание структуры DEB пакета..."

mkdir -p "${PACKAGE_DIR}/usr/lib/calculator"
mkdir -p "${PACKAGE_DIR}/DEBIAN"

# Копирование бинарного файла
if [ ! -f "dist/calculator-Linux-${PYTHON_VERSION}" ]; then
    echo "Ошибка: dist/calculator-Linux-${PYTHON_VERSION} не найден"
    exit 1
fi

cp "dist/calculator-Linux-${PYTHON_VERSION}" "${PACKAGE_DIR}/usr/lib/calculator/"
chmod +x "${PACKAGE_DIR}/usr/lib/calculator/calculator-Linux-${PYTHON_VERSION}"

# Копирование скриптов
cp "./DEBIAN/control" "${PACKAGE_DIR}/DEBIAN/"
cp "./DEBIAN/postinst" "${PACKAGE_DIR}/DEBIAN/"
cp "./DEBIAN/prerm" "${PACKAGE_DIR}/DEBIAN/"

# Выставление прав
chmod 755 "${PACKAGE_DIR}/DEBIAN/postinst"
chmod 755 "${PACKAGE_DIR}/DEBIAN/prerm"

# 3. Сборка пакета
echo "Сборка DEB пакета..."
dpkg-deb --build "${PACKAGE_DIR}"

# Перемещение готового пакета
mv "${PACKAGE_DIR}.deb" "calculator-3.11.deb"

echo "DEB пакет успешно создан: calculator-3.11.deb"