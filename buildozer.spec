[app]

# (str) Title of your application
title = My Safe App

# (str) Package name
package.name = myapp

# (str) Package domain
package.domain = org.test

# (str) Source code where the main.py live
source.dir = .

# (str) Source filename
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 0.1

# (list) Application requirements
# We are using the "Old Reliable" versions that always work
requirements = python3,kivy==2.2.1,kivymd==1.1.1,pillow

# (str) Supported orientation
orientation = portrait

# (bool) Fullscreen
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API
android.api = 31
android.minapi = 21
android.ndk_api = 21

# (bool) Skip updates to save time
android.skip_update = False

# (bool) ACCEPT LICENSE (This fixes the broken pipe)
android.accept_sdk_license = True

# (str) The Android arch to build for
android.archs = arm64-v8a

[buildozer]

# (int) Log level
log_level = 2
warn_on_root = 0
