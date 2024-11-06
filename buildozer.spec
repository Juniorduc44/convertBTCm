[app]
title = Bitcoin Converter
package.name = bitcoinconverter
package.domain = org.btcconverter

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Updated requirements
requirements = python3,kivy==2.2.1,blockchain,certifi,urllib3,requests

version = 1.0

# Android specific
android.minapi = 21
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.archs = arm64-v8a

# Building options
android.accept_sdk_license = True
p4a.bootstrap = sdl2
p4a.branch = develop
android.allow_backup = True

# Basic settings
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1