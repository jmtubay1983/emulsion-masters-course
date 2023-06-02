@echo off

set "script=%HOME%\.emulsionrc\emulsion-powershell-completion.ps1"

powershell -ExecutionPolicy Bypass -File "%script%"
