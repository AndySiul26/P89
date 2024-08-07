@echo off

:: Cambia "main" por el nombre de tu rama si es diferente
set BRANCH=main

:: Solicita el mensaje de commit
set /p COMMIT_MESSAGE="Ingresa tu mensaje de commit: "

:: Navega al directorio del proyecto
:: cd ruta/a/tu/proyecto

:: Agrega todos los cambios al staging area
git add .

:: Realiza el commit con el mensaje ingresado
git commit -m "%COMMIT_MESSAGE%"

:: Empuja los cambios a la rama especificada en el repositorio remoto
git push origin %BRANCH%

echo Commit realizado y push exitoso a la rama %BRANCH%.