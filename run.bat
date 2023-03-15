:start

@echo off
title Blur-AutoBid
app.exe

@echo Some error occurred, please check the log file.
@echo The program will restart in 5 seconds.
@echo If you want to stop the program, simply close this window.
@ping localhost -n 5 > nul
goto start