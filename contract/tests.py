import smartpy as sp

TzPing = sp.io.import_script_from_url("file:contract.py").TzPing
FA2_module = sp.io.import_script_from_url("https://smartpy.io/dev/templates/FA2.py")
FA2 = FA2_module.FA2
FA2_config = FA2_module.FA2_config

@sp.add_test(name = "TzPing", is_default = True)
def test():
    scenario = sp.test_scenario()
    scenario.add_flag("default_record_layout", "comb")
    scenario.h1("TzPing Contract")
    scenario.table_of_contents()

    # Creating test accounts
    admin = sp.test_account("admin").address
    alice = sp.test_account("alice").address
    bob = sp.test_account("bob").address
    user1 = sp.test_account("user1").address
    user2 = sp.test_account("user2").address
    user3 = sp.test_account("user3").address

    subscriber1 = sp.test_account("subscriber1").address
    subscriber2 = sp.test_account("subscriber2").address
    subscriber3 = sp.test_account("subscriber3").address
    subscriber4 = sp.test_account("subscriber4").address


    scenario.h2("Initialise contract")
    c1 = TzPing(
        admin = sp.address("tz1f85LjxaHfWfPuNtZFg1aVBiaAkVnVnKsH")
    )
    scenario += c1

    scenario.h2("Initialise FA2 contract")

    c2 = FA2(
        config = FA2_config(non_fungible = False),
        metadata = sp.utils.metadata_of_url("https://example.com"),
        admin = admin
    )

    scenario += c2

    scenario.h2("Set Admin, failing case")
    c1.setAdmin(
        sp.address("tz1VPZyh4ZHjDDpgvznqQQXUCLcV7g91WGMz")
    ).run(sender = bob, valid = False)

    scenario.h2("Set Admin")
    c1.setAdmin(
        sp.address("tz1VPZyh4ZHjDDpgvznqQQXUCLcV7g91WGMz")
    ).run(sender = sp.address("tz1f85LjxaHfWfPuNtZFg1aVBiaAkVnVnKsH"))

    scenario.h2("Creating channel, failing case")
    c1.createChannel(
        managers = sp.set([alice, bob, user1]),
        ipfsHash = "QmZcjtDZVGenfkHG321UfhPKEn7saKVQJJabiDEnKmNEB7",
        token = sp.record(tokenAddress = c2.address, tokenId = 0)
    ).run(sender = user1, valid = False)

    scenario.h2("mint tokens")
    tok0_md = FA2.make_metadata(
        name = "The Token Zero",
        decimals = 18,
        symbol= "TK0" 
    )

    c2.mint(
        address = user1,
        amount = 100000,
        metadata = tok0_md,
        token_id = 0
    ).run(sender = admin)

    scenario.h2("Update operators")
    c2.update_operators(
        [
            sp.variant("add_operator", c2.operator_param.make(
                owner = user1,
                operator = c1.address,
                token_id = 0
            ))
        ]
    ).run(sender = admin)

    scenario.h2("Creating channel after minting tokens")
    c1.createChannel(
        managers = sp.set([alice, bob, user1]),
        ipfsHash = "QmZcjtDZVGenfkHG321UfhPKEn7saKVQJJabiDEnKmNEB7",
        token = sp.record(tokenAddress = c2.address, tokenId = 0)
    ).run(sender = user1)

    scenario.h2("Setting owner, failing case")
    c1.setOwner(
        channelId = sp.nat(1),
        owner = user2
    ).run(sender = alice, valid = False)

    scenario.h2("Setting owner")
    c1.setOwner(
        channelId = sp.nat(1),
        owner = user2
    ).run(sender = user1)

    scenario.h2("Adding manager, failing case")
    c1.addManager(
        channelId = sp.nat(1),
        manager = user2
    ).run(sender = user3, valid = False)

    scenario.h2("Adding manager")
    c1.addManager(
        channelId = sp.nat(1),
        manager = user2
    ).run(sender = alice)

    scenario.h2("Removing manager, failing case")
    c1.removeManager(
        channelId = 1,
        manager = alice
    ).run(sender = user3, valid = False)

    scenario.h2("Removing manager")
    c1.removeManager(
        channelId = 1,
        manager = alice
    ).run(sender = bob)

    scenario.h2("Deleting channel, failing case")
    c1.deleteChannel(sp.nat(1)).run(sender = bob, valid = False)

    # scenario.h2("Deleting channel")
    # c1.deleteChannel(sp.nat(1)).run(sender = user2)
        
    scenario.h2("Subscribe channel")
    c1.subscribeOrUnsubscribe([sp.record(
        channelId = 1, 
        subscribedOrNot = True
    )]).run(sender = subscriber1)

    scenario.h2("Subscribe channel 2")
    c1.subscribeOrUnsubscribe([sp.record(
        channelId = 1, 
        subscribedOrNot = True
    )]).run(sender = subscriber2)

    scenario.h2("Unsubscribe")
    c1.subscribeOrUnsubscribe([sp.record(
        channelId = 1, 
        subscribedOrNot = False
    )]).run(sender = subscriber2)

    scenario.h2("Creating second channel")
    c1.createChannel(
        managers = sp.set([alice, bob]),
        ipfsHash = "QmZcjtDZVGenfkHG321UfhPKEn7saKVQJJabiDEnKmNEB7",
        token = sp.record(tokenAddress = c2.address, tokenId = 0)
    ).run(sender = user1)
    
    scenario.h2("Subscribe second channel")
    c1.subscribeOrUnsubscribe([sp.record(
        channelId = 2, 
        subscribedOrNot = True
    )]).run(sender = subscriber1)

    scenario.h2("Subscribe second channel subs3")
    c1.subscribeOrUnsubscribe([sp.record(
        channelId = 2, 
        subscribedOrNot = True
    )]).run(sender = subscriber3)

    scenario.h2("Subscribe or unsubscribe multiple channels")
    c1.subscribeOrUnsubscribe([
        sp.record(
            channelId = 1, 
            subscribedOrNot = True
        ),
        sp.record(
            channelId = 2,
            subscribedOrNot = False
        )
    ]).run(sender = subscriber3)

    scenario.h2("Subscribe multiple channels")
    c1.subscribeOrUnsubscribe([
        sp.record(
            channelId = 1, 
            subscribedOrNot = True
        ),
        sp.record(
            channelId = 2,
            subscribedOrNot = True
        )
    ]).run(sender = subscriber4)

    scenario.h2("Disable adv")
    c1.advShowOrNot().run(sender = subscriber1)

    scenario.h2("Enable adv")
    c1.advShowOrNot().run(sender = subscriber1)

    scenario.h2("Send Notification")
    c1.sendNotifications(
        channelId = 1,
        ipfsHash = "QmZcjtDZVGenfkHG321UfhPKEn7saKVQJJabiDEnKmNEB7"
    )

    scenario.h2("Send Notification")
    c1.sendNotifications(
        channelId = 2,
        ipfsHash = "QmZcjtDZVGenfkHG321UfhPKEn7saKVQJJabiDEnKmNEB7"
    )