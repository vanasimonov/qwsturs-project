@echo off
chcp 65001 >nul
title QWSTUR HWID & SYSTEM INSPECTOR // by qwstur
cls

:: ==============================================================================
::        ⚡ QWSTUR STORE - АВТОМАТИЧЕСКИЙ ЗАГРУЗЧИК И УСТАНОВЩИК // by qwstur
::        Владелец: @AimBoGAttack | Магазин: qwsturs store
:: ==============================================================================

set "PY_CMD="

where python >nul 2>nul
if %errorlevel% equ 0 (
    set "PY_CMD=python"
    goto :check_deps
)

where py >nul 2>nul
if %errorlevel% equ 0 (
    set "PY_CMD=py"
    goto :check_deps
)

for /d %%D in ("%LocalAppData%\Programs\Python\Python*") do (
    if exist "%%D\python.exe" (
        set "PY_CMD=%%D\python.exe"
        goto :check_deps
    )
)

for /d %%D in ("%ProgramFiles%\Python*") do (
    if exist "%%D\python.exe" (
        set "PY_CMD=%%D\python.exe"
        goto :check_deps
    )
)

cls
echo ==============================================================================
echo   ⚡ QWSTURS STORE // by qwstur
echo ==============================================================================
echo.
echo   [!] ОШИБКА: Python не найден на вашем компьютере!
echo.
echo   Для работы программы нужен бесплатный Python (3.10 или новее).
echo.
echo   1. Скачайте Python с официального сайта: https://www.python.org/downloads/
echo   2. ВАЖНО: При установке ОБЯЗАТЕЛЬНО поставьте галочку:
echo      [X] "Add python.exe to PATH"
echo.
echo ==============================================================================
echo   Связь с владельцем: https://t.me/AimBoGAttack
echo ==============================================================================
echo.
pause
exit /b 1

:check_deps
if exist requirements.txt (
    findstr /r /v "^[ 	]*#" requirements.txt | findstr /r "[a-zA-Z0-9]" >nul
    if %errorlevel% equ 0 (
        echo [*] Проверка и авто-установка необходимых библиотек...
        "%PY_CMD%" -m pip install -r requirements.txt --disable-pip-version-check
        if %errorlevel% neq 0 (
            echo [!] Не удалось обновить библиотеки через pip, пробуем прямой запуск...
        )
    )
)

"%PY_CMD%" main.py
if %errorlevel% neq 0 (
    echo.
    echo ==============================================================================
    echo   [!] Программа завершилась с кодом ошибки: %errorlevel%
    echo   Поддержка и связь с автором: https://t.me/AimBoGAttack (@AimBoGAttack)
    echo ==============================================================================
    echo.
    pause
)
