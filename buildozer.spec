[app]
title = Pesteh Calculator
package.name = pestehapp
package.domain = ir.fatah
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,spec,yml,yaml
version = 1.0
requirements = python3,kivy==2.3.1,kivymd==1.1.1,pillow
orientation = portrait
fullscreen = 0
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
android.permissions = INTERNET
[buildozer]
log_level = 2
warn_on_root = 1