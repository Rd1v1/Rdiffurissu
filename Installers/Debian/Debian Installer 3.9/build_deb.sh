#!/bin/bash

echo "Подготовка к сборке DEB пакета для Python 3.9..."

# Переменные
PACKAGE_NAME="calculator"
VERSION="1.0.8"
PYTHON_VERSION="3."
BUILD_DIR="build_deb9"
PACKAGE_DIR="${BUILD_DIR}/${PACKAGE_NAME}-${VERSION}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../" && pwd)"

# Очистка предыдущей сборки
rm -rf "${BUILD_DIR}"
mkdir -p "${BUILD_DIR}"

# Сборка бинарного файла из исходников
echo "Установка зависимостей для сборки..."
apt-get update
apt-get install -y python3.9 python3.9-dev python3.9-tk python9-pip

echo "Установка PyInstaller..."
python3.9 -m pip install --upgrade pip
pip install pyinstaller --break-system-packages

echo "Сборка исполняемого файла..."
python3.9 -m PyInstaller \
    --onefile \
    --windowed \
    --name "Calculator-Linux-${PYTHON_VERSION}" \
    --distpath "./dist" \
    --workpath "./build" \
    --specpath "./spec" \
    "${PROJECT_ROOT}/calculator.py"

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
if [ ! -f "dist/Calculator-Linux-${PYTHON_VERSION}" ]; then
    echo "Ошибка: dist/Calculator-Linux-${PYTHON_VERSION} не найден"
    exit 1
fi

cp "dist/Calculator-Linux-${PYTHON_VERSION}" "${PACKAGE_DIR}/usr/lib/calculator/"
chmod +x "${PACKAGE_DIR}/usr/lib/calculator/Calculator-Linux-${PYTHON_VERSION}"

# Копирование скриптов из DEBIAN директории
cp "${SCRIPT_DIR}/DEBIAN/control" "${PACKAGE_DIR}/DEBIAN/"
cp "${SCRIPT_DIR}/DEBIAN/postinst" "${PACKAGE_DIR}/DEBIAN/"
cp "${SCRIPT_DIR}/DEBIAN/prerm" "${PACKAGE_DIR}/DEBIAN/"

# Выставление прав
chmod 755 "${PACKAGE_DIR}/DEBIAN/postinst"
chmod 755 "${PACKAGE_DIR}/DEBIAN/prerm"

# 3. Сборка пакета
echo "Сборка DEB пакета..."
dpkg-deb --build "${PACKAGE_DIR}"

# Перемещение готового пакета
mv "${PACKAGE_DIR}.deb" "${SCRIPT_DIR}/Calculator-Linux-3.9.deb"

echo "DEB пакет успешно создан: Calculator-Linux-3.9.deb"
echo "Путь: ${SCRIPT_DIR}/Calculator-Linux-3.9.deb"
