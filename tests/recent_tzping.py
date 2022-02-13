import smartpy as sp

TzPing = sp.io.import_script_from_url("file:smart_contracts/recent_tzping.py").TzPing

@sp.add_test(name = "TzPing", is_default = True)
def test():
    scenario = sp.test_scenario()
    scenario.add_flag("default_record_layout", "comb")
    scenario.h1("TzPing Contract")
    scenario.table_of_contents()

    # Creating test accounts
    admin = sp.test_account("admin")
    alice = sp.test_account("alice")
    bob = sp.test_account("bob")
    user1 = sp.test_account("user1")
    user2 = sp.test_account("user2")
    user3 = sp.test_account("user3")

    subscriber1 = sp.test_account("subscriber1")
    subscriber2 = sp.test_account("subscriber2")
    subscriber3 = sp.test_account("subscriber3")
    subscriber4 = sp.test_account("subscriber4")


    scenario.h2("Initialise contract")
    c1 = TzPing(admin.address)
    scenario += c1

    scenario.h2("Set Admin, failing case")
    c1.setAdmin(alice.address).run(sender = bob, valid = False, exception="NOT_ADMIN")

    scenario.h2("Set Admin")
    c1.setAdmin(alice.address).run(sender = admin)

    scenario.h2("Creating channel")
    c1.createChannel(
        managers = sp.set([alice.address, bob.address, user1.address]),
        ipfsHash = "QmZcjtDZVGenfkHG321UfhPKEn7saKVQJJabiDEnKmNEB7",
    ).run(sender = user1)

    scenario.h2("Setting owner, failing case")
    c1.setOwner(
        channelId = sp.nat(1),
        owner = user2.address
    ).run(sender = alice, valid = False, exception="NOT_OWNER")

    scenario.h2("Setting owner")
    c1.setOwner(
        channelId = sp.nat(1),
        owner = user2.address
    ).run(sender = user1)

    scenario.h2("Adding manager, failing case")
    c1.addManager(
        channelId = sp.nat(1),
        manager = user2.address
    ).run(sender = user3, valid = False, exception="NOT_OWNER_OR_MANAGER")

    scenario.h2("Adding manager")
    c1.addManager(
        channelId = sp.nat(1),
        manager = user2.address
    ).run(sender = alice)

    scenario.h2("Removing manager, failing case")
    c1.removeManager(
        channelId = 1,
        manager = alice.address
    ).run(sender = user3, valid = False, exception="NOT_OWNER_OR_MANAGER")

    scenario.h2("Removing manager")
    c1.removeManager(
        channelId = 1,
        manager = alice.address
    ).run(sender = bob)

    scenario.h2("Deleting channel, failing case")
    c1.deleteChannel(sp.nat(1)).run(sender = bob, valid = False, exception="NOT_OWNER")

    # scenario.h2("Deleting channel")
    # c1.deleteChannel(sp.nat(1)).run(sender = user2)
        
    scenario.h2("Subscribe channel")
    c1.subscribeOrUnsubscribe([sp.record(
        channelId = 1, 
        subscribedOrNot = True
    )]).run(sender = subscriber1)

    scenario.h2("Subscribe channel sub2")
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
        managers = sp.set([alice.address, bob.address]),
        ipfsHash = "QmZcjtDZVGenfkHG321UfhPKEn7saKVQJJabiDEnKmNEB7",
    ).run(sender = user1)
    
    scenario.h2("Subscribe second channel")
    c1.subscribeOrUnsubscribe([sp.record(
        channelId = 2, 
        subscribedOrNot = True
    )]).run(sender = subscriber1)

    scenario.h2("Subscribe second channel, check")
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

    scenario.h2("Send Notification")
    c1.sendNotifications(
        channelId = 1,
        ipfsHash = "QmZcjtDZVGenfkHG321UfhPKEn7saKVQJJabiDEnKmNEB7"
    ).run(sender = user1)

    scenario.h2("Send Notification")
    c1.sendNotifications(
        channelId = 2,
        ipfsHash = "QmZcjtDZVGenfkHG321UfhPKEn7saKVQJJabiDEnKmNEB7"
    ).run(sender = alice)
    
    scenario.h2("Send Notification")
    c1.sendNotifications(
        channelId = 2,
        ipfsHash = "QmZcjtDZVGenfkHG321UfhPKEn7saKVQJJabiDEnKmNEB7"
    ).run(sender = user3, valid = False)

    scenario.h2("Send selective notification")
    c1.selectiveNotifications(
        channelId = 1,
        ipfsHash = "QmZcjtDZVGenfkHG321UfhPKEn7saKVQJJabiDEnKmNEB7",
        receivers = sp.list([subscriber3.address, subscriber4.address])
    ).run(sender = bob)