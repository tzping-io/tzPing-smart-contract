import smartpy as sp

TzPing = sp.io.import_script_from_url("file:smart_contracts/tzping.py").TzPing

sp.add_compilation_target(
    "TzPing",
    TzPing(
        admin = sp.address("tz1f85LjxaHfWfPuNtZFg1aVBiaAkVnVnKsH"),
        tokenId = sp.nat(1),
        tokenAddress = sp.address("KT1BzX9afE9j549Qtig3rJbKQ7xrRc7PHYHh")
    ),
    flags = [["default_record_layout", "comb"]]
)