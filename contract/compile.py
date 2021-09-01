import smartpy as sp

MultisigEscrow = sp.io.import_script_from_url("file:contract.py").MultisigEscrow

sp.add_compilation_target(
    "Multisig Escrow",
    MultisigEscrow(
        owners = sp.set(
            [
                sp.address("tz1f85LjxaHfWfPuNtZFg1aVBiaAkVnVnKsH"),
                sp.address("tz1VPZyh4ZHjDDpgvznqQQXUCLcV7g91WGMz"),
                sp.address("tz1fs7ki5nVyZGaLw6VpY8Rv5xvnh1pgj28G")
            ]
        ),
        votesRequired = sp.nat(2)
    ),
    flags = [["default_record_layout", "comb"]]
)