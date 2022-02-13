import smartpy as sp

contracts = [
    'recent_tzping',
]

for contract in contracts:
    print(f"Compiling {contract}...")
    sp.io.import_script_from_url(f"file:compile/{contract}.py")
