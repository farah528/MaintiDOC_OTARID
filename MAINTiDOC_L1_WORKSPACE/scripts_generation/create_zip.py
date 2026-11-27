import os, zipfile

workspace_dir = os.path.abspath("MAINTiDOC_L1_WORKSPACE")
source_dir = os.path.join(workspace_dir, "L1_MaintiDoc_OTARID")
zip_path = os.path.join(workspace_dir, "L1_MaintiDoc_OTARID.zip")

if os.path.exists(zip_path):
    os.remove(zip_path)

print(f"Creating ZIP archive: {zip_path}...")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            full_path = os.path.join(root, file)
            # Relative path starting with L1_MaintiDoc_OTARID
            rel_path = os.path.relpath(full_path, workspace_dir)
            zipf.write(full_path, rel_path)

print(f"ZIP created successfully: {os.path.getsize(zip_path)} bytes ({os.path.getsize(zip_path) / (1024*1024):.2f} MB)")

# Verify ZIP structure
with zipfile.ZipFile(zip_path, "r") as zipf:
    namelist = zipf.namelist()
    print(f"Total files in ZIP: {len(namelist)}")
    # Check that every single file starts with L1_MaintiDoc_OTARID/
    for n in namelist:
        assert n.startswith("L1_MaintiDoc_OTARID/"), f"File outside root directory: {n}"
    
    # Check top-level elements
    top_level = set()
    for n in namelist:
        parts = n.split("/")
        if len(parts) > 1:
            top_level.add(parts[1])
    
    print("Top-level elements inside root folder:", sorted(top_level))
    expected_top = {"L1_MaintiDoc_OTARID_Corpus", "L1_MaintiDoc_OTARID_LienGitHub.txt", "L1_MaintiDoc_OTARID_Rapport.pdf", "README.md"}
    assert top_level == expected_top, f"Mismatch in top level elements: {top_level ^ expected_top}"

print("ZIP archive verified 100% compliant with submission specifications!")
