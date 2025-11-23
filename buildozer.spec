[app]
title = Physics Solver
package.name = physicssolver
package.domain = org.jabulani

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt

version = 0.1
requirements = python3,kivy,numpy

[buildozer]
log_level = 2

[app]
presplash.filename = %(source.dir)s/presplash.png
icon.filename = %(source.dir)s/icon.png

android.permissions = 
android.api = 33
android.minapi = 21
