import smartpy as sp

filename = "recent_tzping"
print(f"Testing {filename}...")
tzping = sp.io.import_script_from_url(f"file:tests/{filename}.py")

