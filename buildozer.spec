[app]
title = My Safe App
package.name = myapp
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# CRITICAL: Using older, stable versions to prevent crashes
requirements = python3,kivy==2.2.1,kivymd==1.1.1,pillow

orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 31
android.minapi = 21
android.ndk_api = 21
android.skip_update = False
android.accept_sdk_license = True
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 0
