@echo off

set DIR=%~dps0
:: remove trailing backslash
if "%DIR:~-1%" == "\" (
    set DIR=%DIR:~0,-1%
)

if "%~1"=="-v" (
    set XCOPY_FLAG=/f
) else (
    set XCOPY_FLAG=/q
)

set ROOT=%DIR%\..
set /p VERSION=<%ROOT%\io_scene_nif\VERSION
set NAME=blender_nif_plugin
set PYFFI_VERSION=2.2.4.dev3
set DEPS="io_scene_nif\dependencies"
if exist %DIR%\temp rmdir /s /q %DIR%\temp

if not "%~1"=="-q" (
    echo NAME: %NAME%
    echo VERSION: %VERSION%
    echo PYFFI_VERSION: %PYFFI_VERSION%
)

mkdir %DIR%\temp

pushd %DIR%\temp
mkdir io_scene_nif
xcopy /s %XCOPY_FLAG% %ROOT%\io_scene_nif io_scene_nif
mkdir %DEPS%

python -m pip install "PyFFI==%PYFFI_VERSION%" --target="%DEPS%"

xcopy %XCOPY_FLAG% %ROOT%\*.rst io_scene_nif
popd

powershell -executionpolicy bypass -Command "%DIR%\zip.ps1" -source "%DIR%\temp" -destination "%DIR%\%NAME%-%VERSION%.zip"
rmdir /s /q %DIR%\temp
