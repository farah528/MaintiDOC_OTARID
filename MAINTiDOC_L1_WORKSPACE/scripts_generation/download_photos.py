import urllib.request, ssl, os, shutil
from PIL import Image

ctx = ssl._create_unverified_context()
headers = {'User-Agent': 'MaintiDocBot/1.0 (academic research; contact@emsi.ma)'}

target_dirs = [
    os.path.abspath("MAINTiDOC_L1_WORKSPACE/L1_MaintiDoc_OTARID/L1_MaintiDoc_OTARID_Corpus/images"),
    os.path.abspath("MAINTiDOC_L1_WORKSPACE/maintidoc/corpus/images")
]

# URLs from Wikimedia Commons
# C12: Pressure gauges on a compressor (CC0)
url_c12 = "https://upload.wikimedia.org/wikipedia/commons/8/85/Pressure_gauges_on_a_compressor.jpg"
# F12: SMS Senator Fire Alarm Control Panel (CC0)
url_f12 = "https://upload.wikimedia.org/wikipedia/commons/6/62/SMS_Senator_Fire_Alarm_Control_Panel.jpg"

def download_and_save(url, filename):
    req = urllib.request.Request(url, headers=headers)
    print(f"Downloading {filename} from {url[:50]}...")
    with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
        data = resp.read()
    
    # Save to first dir and copy to second
    path1 = os.path.join(target_dirs[0], filename)
    with open(path1, "wb") as f:
        f.write(data)
    
    # Optimize with PIL to ensure valid JPEG and reasonable size
    img = Image.open(path1)
    print(f"Loaded {filename}: size {img.size}, format {img.format}")
    img.save(path1, "JPEG", quality=85)
    
    path2 = os.path.join(target_dirs[1], filename)
    shutil.copy2(path1, path2)
    print(f"Saved {filename} ({os.path.getsize(path1)} bytes) to both target dirs.")

download_and_save(url_c12, "C12.jpg")
download_and_save(url_f12, "F12.jpg")
print("C12 and F12 downloaded successfully!")
