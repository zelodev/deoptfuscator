 #!/usr/bin/env python3
import sys
import os
sys.path.insert(0, 'deobfuscator')
import deobfuscator,sys,requests

def download_file(url):
    get_response = requests.get(url,stream=True)
    file_name  = url.split("/")[-1]
    with open(file_name, 'wb') as f:
        for chunk in get_response.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    return file_name
	
#from os.path import getsize
APK = "https://d.apkpure.com/b/APK/com.weo.projectz?versionCode=5&nc=arm64-v8a%2Carmeabi-v7a&sv=21"
apk_name = download_file(APK)
outpath = apk_name.replace(".apk", "de.apk")
tmp = outpath.split("/")[-1]
outpath = outpath.replace(tmp, "")
os.system("rm -rf .apk .std* .profile meta")
os.system("java -jar $TOOLS/apktool.jar d -r -s " + apk_name  + " -o .apk")
dex_li = [a for a in os.listdir(".apk") if a.endswith(".dex") and a.startswith("classes")]
os.mkdir(".apk/const")
#os.makedirs(outpath, exist_ok=True)

for dex in dex_li:
	deobfuscator.main(".apk/"+dex)
	os.system("$TOOLS/redex-all -c $TOOLS/default.config .apk/const/const.dex -o .apk/const")
	print("$TOOLS/redex-all .apk/const/const.dex -o .apk/const")
	os.system("mv .apk/const/classes.dex .apk/"+dex)

apk_name = apk_name.replace(".apk", "_deobfuscated.apk")
apk_name = os.path.basename(apk_name)
os.system("java -jar $TOOLS/apktool.jar b ./.apk -o " + apk_name)

os.system("zipalign -f -v 4 " + apk_name + " " + apk_name.replace(".apk", "_align.apk"))
os.system("apksigner sign --ks deoptfuscator.keystore --ks-pass pass:123456 " + apk_name.replace(".apk", "_align.apk"))
os.system("rm -rf " + apk_name)
