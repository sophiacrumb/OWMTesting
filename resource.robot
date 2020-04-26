*** Settings ***
Library    OperatingSystem
Library    Collections
Library    BuiltIn
Library    String
Library    SeleniumLibrary
Library    Screenshot
Library    DateTime
Library    Collections
Library    RequestsLibrary
Library    weather.py

#Process
#Screenshot
#String
#Telnet
#XML

*** Variables ***
${NAME}             Robot Framework
${VERSION}          2.0
${ROBOT}            ${NAME} ${VERSION}  #catenate 2 or more variables
${USER}             Chernousova Sophia

