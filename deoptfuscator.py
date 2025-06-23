#!/usr/bin/env python3
import sys
import os
import requests

# Set up module path
sys.path.insert(0, 'deobfuscator')
import deobfuscator

def download_file(url, file_name):
    get_response = requests.get(url, stream=True)
    with open(file_name, 'wb') as f:
        for chunk in get_response.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    return file_name

# Set ANDROID_HOST_OUT environment variable
os.environ['ANDROID_HOST_OUT'] = os.path.join(os.getcwd(), "android")

# APK URL and download
APK_URL = "https://github.com/tribalfs/GalaxyMaxHzPub/releases/download/v8.1/galaxy_max_hz_v8.1.apk"
apk_name = "galaxy_max_hz_v8.1.apk"
download_file(APK_URL, apk_name)

# Output paths
outpath = apk_name.replace(".apk", "de.apk")
tmp = os.path.basename(outpath)
outpath = outpath.replace(tmp, "")

# Clean up previous runs
os.system("rm -rf .apk .std* .profile meta")

# Decode APK
os.system("java -jar tools/apktool.jar d -r -s " + apk_name + " -o .apk")

# Process .dex files
dex_li = [a for a in os.listdir(".apk") if a.endswith(".dex") and a.startswith("classes")]
os.mkdir(".apk/const")
print(dex_li)
for dex in dex_li:
    deobfuscator.main(".apk/" + dex)
    os.system("tools/redex-all -c tools/default.config .apk/const/const.dex -o .apk/const")
    print("tools/redex-all .apk/const/const.dex -o .apk/const")
    os.system("mv .apk/const/classes.dex .apk/" + dex)

# Rebuild APK
rebuilt_apk = apk_name.replace(".apk", "_deobfuscated.apk")
rebuilt_apk = os.path.basename(rebuilt_apk)
os.system("java -jar tools/apktool.jar b ./.apk -o " + rebuilt_apk)

# Align and sign
aligned_apk = rebuilt_apk.replace(".apk", "_align.apk")
os.system("zipalign -f -v 4 " + rebuilt_apk + " " + aligned_apk)
os.system("apksigner sign --ks deoptfuscator.keystore --ks-pass pass:123456 " + aligned_apk)

# Clean up
os.system("rm -rf " + rebuilt_apk)
