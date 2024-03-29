[app]

title = Wasserwaage
package.name = wasserwaage
package.domain = gsog.de


kivy==master
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,mp3

version = 0.1
requirements = python3,kivy,plyer,paho-mqtt

android.permissions = INTERNET
android.orientation = landscape
orientation = landscape
fullscreen = 0
android.archs = arm64-v8a
p4a.branch = release-2022.12.20

# iOS specific
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = main
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.12.2
ios.codesign.allowed = false

icon.filename = icon.png
icon.entry_point = main.ScaleApp

[buildozer]
log_level = 2
warn_on_root = 1
