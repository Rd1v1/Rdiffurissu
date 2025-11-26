#!/bin/bash

set -e 

# Переменные по умолчанию
PYTHON_VERSION="3.11"
GITHUB_URL="https://github.com/Rd1v1/Rdiffurissu.git"
REPO_DIR="calculator_repo"
TEMP_DIR="/tmp/calculator_build"

# Парсинг аргументов
for arg in "$@"; do
    case $arg in
        --python=*)
            PYTHON_VERSION="${arg#*=}"
            ;;
    esac
done

# Валидация версии Python
if [[ "$PYTHON_VERSION" != "3.9" && "$PYTHON_VERSION" != "3.11" ]]; then
    echo "Ошибка: Поддерживаются только версии 3.9 и 3.11"
    exit 1
fi

echo "Развертывание приложения Calculator"
echo "Версия Python: $PYTHON_VERSION"
echo ""

# Очистка и подготовка
echo "Подготовка окружения..."
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"
cd "$TEMP_DIR"
echo "Окружение готово"
echo ""

# Загрузка проекта
echo "Загрузка проекта..."
git clone "$GITHUB_URL" "$REPO_DIR"
cd "$REPO_DIR"
echo "Загрузка выполнена"
echo ""

# Установка зависимостей
echo "Установка зависимостей для сборки..."
apt update
apt install -y python${PYTHON_VERSION} python${PYTHON_VERSION}-dev python${PYTHON_VERSION}-tk python3-pip
echo "Зависимости установлены"
echo ""

echo "Установка PyInstaller..."
python${PYTHON_VERSION} -m pip install --upgrade pip --break-system-packages
pip install pyinstaller --break-system-packages
echo "PyInstaller установлен"
echo ""

# Сборка проекта
echo "Сборка проекта..."
python${PYTHON_VERSION} -m PyInstaller --onefile --windowed calculator.py
echo "Проект собран"
echo ""

# Запуск unit тестов
echo "Выполнение unit тестов..."
python${PYTHON_VERSION} -m unittest unittests.py -v
echo "Unit тесты пройдены"
echo ""

# Создание DEB установщика
echo "Создание DEB установщика..."
BUILD_SCRIPT="Installers/Debian/Debian Installer ${PYTHON_VERSION}/build_deb.sh"

if [ ! -f "$BUILD_SCRIPT" ]; then
    echo "Ошибка: Скрипт сборки не найден: $BUILD_SCRIPT"
    exit 1
fi

bash "$BUILD_SCRIPT"
echo "DEB установщик создан"
echo ""

# Поиск и перемещение DEB файла
echo "Перемещение установщика в /tmp/..."
DEB_FILE=$(find . -name "*.deb" -type f | head -1)

if [ -z "$DEB_FILE" ]; then
    echo "Ошибка: DEB файл не найден"
    exit 1
fi

cp "$DEB_FILE" /tmp/
DEB_NAME=$(basename "$DEB_FILE")
echo "Установщик перемещен: /tmp/$DEB_NAME"
echo ""

# Установка приложения
echo "Установка приложения..."
apt install -y "/tmp/$DEB_NAME"
echo "Приложение установлено"
echo ""

# Завершение
echo "Развертывание завершено успешно!"
echo ""
echo "Установленный пакет: $DEB_NAME"
echo "Путь к пакету: /tmp/$DEB_NAME"
