@echo off

:: This script should be run as a .bat file
:: This script deletes all files named Output.csv and TestOutput.csv in the current
:: directory and any subdirectories

del Output.csv /s
del TestOutput.csv /s