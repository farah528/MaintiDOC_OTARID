import urllib.request, json, ssl, os
import pypdfium2 as pdfium

ctx = ssl._create_unverified_context()
headers = {'User-Agent': 'Mozilla/5.0'}

downloads = [
    # Compressors
    ("C01_sullair", "https://archive.org/download/manualzilla-id-5636308/5636308.pdf"),
    ("C02_scroll", "https://archive.org/download/manualzilla-id-7414769/7414769.pdf"),
    ("C03_miller", "https://archive.org/download/manualzilla-id-7007460/7007460.pdf"),
    ("C04_dod", "https://archive.org/download/DTIC_ADA132506/DTIC_ADA132506.pdf"),
    # Fire alarms
    ("F01_2xf", "https://archive.org/download/manualzilla-id-6875802/6875802.pdf"),
    ("F02_conv", "https://archive.org/download/manualzilla-id-5780839/5780839.pdf"),
    ("F03_mx", "https://archive.org/download/manualzilla-id-5745935/5745935.pdf"),
    ("F04_ebl", "https://archive.org/download/manualzilla-id-6885445/6885445.pdf")
]

for name, url in downloads:
    target = f"test_{name}.pdf"
    if os.path.exists(target):
        print(f"{target} already exists, skipping download.")
    else:
        try:
            print(f"Downloading {name} from {url}...")
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, context=ctx, timeout=30) as r, open(target, "wb") as f:
                f.write(r.read())
            print(f"Downloaded {target}: {os.path.getsize(target)} bytes")
        except Exception as e:
            print(f"Failed {name}: {e}")
            continue

    try:
        doc = pdfium.PdfDocument(target)
        print(f"--> {name}: {len(doc)} pages")
    except Exception as e:
        print(f"Error reading {target}: {e}")
