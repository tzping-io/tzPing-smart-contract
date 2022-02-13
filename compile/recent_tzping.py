import smartpy as sp

TzPing = sp.io.import_script_from_url("file:smart_contracts/recent_tzping.py").TzPing

sp.add_compilation_target(
    "TzPing",
    TzPing(sp.address("tz1f85LjxaHfWfPuNtZFg1aVBiaAkVnVnKsH")),
    flags = [["default_record_layout", "comb"]]
)
