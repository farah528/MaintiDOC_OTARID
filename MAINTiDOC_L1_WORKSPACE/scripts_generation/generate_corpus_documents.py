import os, shutil
import pypdfium2 as pdfium
from playwright.sync_api import sync_playwright
from PIL import Image, ImageOps, ImageFilter
import io

base1 = os.path.abspath("MAINTiDOC_L1_WORKSPACE/L1_MaintiDoc_OTARID/L1_MaintiDoc_OTARID_Corpus")
base2 = os.path.abspath("MAINTiDOC_L1_WORKSPACE/maintidoc/corpus")

f1_dir1 = os.path.join(base1, "documents", "famille_1")
f2_dir1 = os.path.join(base1, "documents", "famille_2")
f1_dir2 = os.path.join(base2, "documents", "famille_1")
f2_dir2 = os.path.join(base2, "documents", "famille_2")

for d in [f1_dir1, f2_dir1, f1_dir2, f2_dir2]:
    os.makedirs(d, exist_ok=True)

print("--- 1. Packaging Real Documents from verified sources ---")

def extract_pages(src_pdf, start_page, end_page, out_name, target_dirs):
    src = pdfium.PdfDocument(src_pdf)
    new_doc = pdfium.PdfDocument.new()
    page_indices = list(range(start_page - 1, min(end_page, len(src))))
    new_doc.import_pages(src, page_indices)
    
    path1 = os.path.join(target_dirs[0], out_name)
    new_doc.save(path1)
    path2 = os.path.join(target_dirs[1], out_name)
    shutil.copy2(path1, path2)
    print(f"Extracted {len(page_indices)} pages from {src_pdf} -> {out_name}")

def copy_pdf(src_pdf, out_name, target_dirs):
    path1 = os.path.join(target_dirs[0], out_name)
    shutil.copy2(src_pdf, path1)
    path2 = os.path.join(target_dirs[1], out_name)
    shutil.copy2(src_pdf, path2)
    doc = pdfium.PdfDocument(path1)
    print(f"Copied {src_pdf} -> {out_name} ({len(doc)} pages, {os.path.getsize(path1)} bytes)")

# Compresseurs réels:
copy_pdf("test_C01_sullair.pdf", "C01.pdf", [f1_dir1, f1_dir2]) # Manuel général
copy_pdf("test_C02_scroll.pdf", "C02.pdf", [f1_dir1, f1_dir2])  # Manuel d'utilisation
copy_pdf("test_C03_miller.pdf", "C03.pdf", [f1_dir1, f1_dir2])  # Maintenance préventive
copy_pdf("test_C04_dod.pdf", "C04.pdf", [f1_dir1, f1_dir2])     # Fiche technique
extract_pages("test_C01_sullair.pdf", 16, 21, "C05.pdf", [f1_dir1, f1_dir2]) # Procédure démarrage/arrêt (6 pages)
extract_pages("test_C01_sullair.pdf", 33, 36, "C06.pdf", [f1_dir1, f1_dir2]) # Procédure vidange/huile (4 pages)
extract_pages("test_C02_scroll.pdf", 18, 21, "C07.pdf", [f1_dir1, f1_dir2])  # Remplacement filtres (4 pages)
extract_pages("test_C01_sullair.pdf", 9, 13, "C08.pdf", [f1_dir1, f1_dir2])   # Tableau codes alarme (5 pages)

# Fire alarm réels:
copy_pdf("test_F01_2xf.pdf", "F01.pdf", [f2_dir1, f2_dir2])   # Manuel installation
copy_pdf("test_F02_conv.pdf", "F02.pdf", [f2_dir1, f2_dir2])  # Manuel d'utilisation
copy_pdf("test_F03_mx.pdf", "F03.pdf", [f2_dir1, f2_dir2])    # Manuel maintenance
copy_pdf("test_F04_ebl.pdf", "F04.pdf", [f2_dir1, f2_dir2])   # Fiche technique / exploitation
extract_pages("test_F01_2xf.pdf", 35, 40, "F05.pdf", [f2_dir1, f2_dir2]) # Procédure mise en service (6 pages)
extract_pages("test_F01_2xf.pdf", 45, 48, "F06.pdf", [f2_dir1, f2_dir2]) # Procédure test détecteurs (4 pages)
extract_pages("test_F01_2xf.pdf", 59, 61, "F07.pdf", [f2_dir1, f2_dir2]) # Procédure réinitialisation (3 pages)
extract_pages("test_F01_2xf.pdf", 11, 15, "F08.pdf", [f2_dir1, f2_dir2]) # Tableau codes défauts (5 pages)

print("Real PDF extractions completed successfully!")
