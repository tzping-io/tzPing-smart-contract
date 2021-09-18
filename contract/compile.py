import smartpy as sp

TzPing = sp.io.import_script_from_url("file:contract.py").TzPing

FA2_module = sp.io.import_script_from_url("file:FA2.py")
FA2 = FA2_module.FA2
FA2_config = FA2_module.FA2_config

sp.add_compilation_target(
    "Ping_token",
    FA2(
        config = FA2_config(non_fungible = False),
        metadata = sp.utils.metadata_of_url("ipfs://QmZHEaU5RpPfqWDBkpVwUdvmQUm1fFv91n7Vm5NqRmWYuF"),
        admin = sp.address("tz1f85LjxaHfWfPuNtZFg1aVBiaAkVnVnKsH")
    )
)

sp.add_compilation_target(
    "TzPing",
    TzPing(
        admin = sp.address("tz1f85LjxaHfWfPuNtZFg1aVBiaAkVnVnKsH"),
        tokenId = sp.nat(1),
        tokenAddress = sp.address("KT1BzX9afE9j549Qtig3rJbKQ7xrRc7PHYHh")
    ),
    flags = [["default_record_layout", "comb"]]
)