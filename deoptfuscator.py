 #!/usr/bin/env python3
import sys
import os
sys.path.insert(0, 'deobfuscator')
import deobfuscator,sys,requests
def download_file(url, file_name):
    get_response = requests.get(url,stream=True)
    with open(file_name, 'wb') as f:
        for chunk in get_response.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    return file_name

os.environ['ANDROID_HOST_OUT'] = os.path.join(os.getcwd(), "android")
APK = "https://d-06.winudf.com/b/APK/Y29tLndlby5wcm9qZWN0el81XzZiZmZkNGJm?_fn=SkFDTyAtINis2KfZg9mIXzEuMC4wX0Fwa3B1cmUuYXBr&_p=Y29tLndlby5wcm9qZWN0eg%3D%3D&is_hot=false&k=9b7cff9dcc863fe4244dda214d8abb996575a260"
apk_name = download_file(APK, "jaco.1.0.0.0.apk")
outpath = apk_name.replace(".apk", "de.apk")
tmp = outpath.split("/")[-1]
outpath = outpath.replace(tmp, "")
os.system("rm -rf .apk .std* .profile meta")
os.system("java -jar tools/apktool.jar d -r -s " + apk_name  + " -o .apk")
dex_li = [a for a in os.listdir(".apk") if a.endswith(".dex") and a.startswith("classes")]
os.mkdir(".apk/const")
#os.makedirs(outpath, exist_ok=True)
print(dex_li)
for dex in dex_li:
	deobfuscator.main(".apk/"+dex)
	os.system("tools/redex-all -c tools/default.config .apk/const/const.dex -o .apk/const")
	print("tools/redex-all .apk/const/const.dex -o .apk/const")
	os.system("mv .apk/const/classes.dex .apk/"+dex)

apk_name = apk_name.replace(".apk", "_deobfuscated.apk")
apk_name = os.path.basename(apk_name)
os.system("java -jar tools/apktool.jar b ./.apk -o " + apk_name)

os.system("zipalign -f -v 4 " + apk_name + " " + apk_name.replace(".apk", "_align.apk"))
os.system("apksigner sign --ks deoptfuscator.keystore --ks-pass pass:123456 " + apk_name.replace(".apk", "_align.apk"))
os.system("rm -rf " + apk_name)
