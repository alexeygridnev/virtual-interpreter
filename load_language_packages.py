# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import argostranslate.package
import argostranslate.translate

argostranslate.package.update_package_index()
available_packages = argostranslate.package.get_available_packages()

languages = ["Russian", 
             "English", 
             "French", 
             "German", 
             "Spansih", 
             "Italian", 
             "Chinese"]

required_packages = []


for package in available_packages:
    for language in languages:
        if language in str(package):
            required_packages.append(package)

for package in required_packages:
    argostranslate.package.install_from_path(package.download())

