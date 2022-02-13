import smartpy as sp

# how to get all subscribers addresses of a channel

class TzPing(sp.Contract):
    def __init__(self, admin):
        self.init(
            admin = admin,
            channelId = sp.nat(1),
            channels = sp.big_map(
                tkey = sp.TNat,
                tvalue = sp.TRecord(
                    owner = sp.TAddress,
                    managers = sp.TSet(sp.TAddress),
                    totalSubscribers = sp.TNat,
                    ipfsHash = sp.TString,
                )
            ),
            subscribers = sp.big_map(
                tkey = sp.TAddress,
                tvalue = sp.TSet(sp.TNat), #subcribed channels
            ),
            notificationId = sp.nat(1),
            notifications = sp.big_map(
                tkey = sp.TNat,
                tvalue = sp.TRecord(
                    channelId = sp.TNat,
                    ipfsHash = sp.TString
                )
            ),
            selectiveNotificationId = sp.nat(1),
            selectiveNotifications = sp.big_map(
                tkey = sp.TNat,
                tvalue = sp.TRecord(
                    channelId = sp.TNat,
                    ipfsHash = sp.TString,
                    receivers = sp.TList(sp.TAddress)
                )
            ),
            metadata = sp.utils.metadata_of_url("ipfs://QmS2gQbrT6jFuS7uz4GcT68bxtZXnrvmTTevE4DuL3M1zS")
        )

    @sp.entry_point
    def setAdmin(self, address):
        sp.set_type(address, sp.TAddress)

        sp.verify(sp.sender == self.data.admin, message="NOT_ADMIN")
        self.data.admin = address

    @sp.entry_point
    def createChannel(self, params):
        sp.set_type(params, sp.TRecord(
            managers = sp.TSet(sp.TAddress),
            ipfsHash = sp.TString,
        ))

        self.data.channels[self.data.channelId] = sp.record(
            owner = sp.sender,
            managers = params.managers,
            totalSubscribers = sp.nat(0),
            ipfsHash = params.ipfsHash,
        )

        self.data.channelId = self.data.channelId + 1


    @sp.entry_point
    def setOwner(self, params):
        sp.set_type(params, sp.TRecord(
            channelId = sp.TNat,
            owner = sp.TAddress
        ))

        sp.verify(sp.sender == self.data.channels[params.channelId].owner, message="NOT_OWNER")
        self.data.channels[params.channelId].owner = params.owner

    @sp.entry_point
    def addManager(self, params):
        sp.set_type(params, sp.TRecord(
            channelId = sp.TNat,
            manager = sp.TAddress
        ))

        sp.verify(
            (sp.sender == self.data.channels[params.channelId].owner) | (self.data.channels[params.channelId].managers.contains(sp.sender)),
            message = "NOT_OWNER_OR_MANAGER"
        )
        self.data.channels[params.channelId].managers.add(params.manager)

    @sp.entry_point
    def removeManager(self, params):
        sp.set_type(params, sp.TRecord(
            channelId = sp.TNat,
            manager = sp.TAddress
        ))

        sp.verify(
            (sp.sender == self.data.channels[params.channelId].owner) | (self.data.channels[params.channelId].managers.contains(sp.sender)),
            message = "NOT_OWNER_OR_MANAGER"
        )
        self.data.channels[params.channelId].managers.remove(params.manager)

    @sp.entry_point
    def deleteChannel(self, channelId):
        sp.set_type(channelId, sp.TNat)

        sp.verify(sp.sender == self.data.channels[channelId].owner, message="NOT_OWNER")
        del self.data.channels[channelId]

    @sp.entry_point
    def subscribeOrUnsubscribe(self, params):
        sp.set_type(params, sp.TList(sp.TRecord(
            channelId = sp.TNat,
            subscribedOrNot = sp.TBool
        )))

        sp.for query in params:
            sp.if query.subscribedOrNot:
                sp.if ~self.data.subscribers.contains(sp.sender):
                    self.data.subscribers[sp.sender] = sp.set()
                    
                sp.if ~self.data.subscribers[sp.sender].contains(query.channelId):
                    self.data.channels[query.channelId].totalSubscribers += 1
                    self.data.subscribers[sp.sender].add(query.channelId)
                
            sp.else:
                self.data.subscribers[sp.sender].remove(query.channelId)
                self.data.channels[query.channelId].totalSubscribers = sp.as_nat(self.data.channels[query.channelId].totalSubscribers - 1)

    @sp.entry_point
    def sendNotifications(self, params):
        sp.set_type(params, sp.TRecord(
            channelId = sp.TNat,
            ipfsHash = sp.TString
        ))

        sp.verify(
            (sp.sender == self.data.channels[params.channelId].owner) | (self.data.channels[params.channelId].managers.contains(sp.sender)),
            message = "NOT_OWNER_OR_MANAGER"
        )
        
        self.data.notifications[self.data.notificationId] = sp.record(
            channelId = params.channelId,
            ipfsHash = params.ipfsHash
        )

        self.data.notificationId += 1

    @sp.entry_point
    def selectiveNotifications(self, params):
        sp.set_type(params, sp.TRecord(
            channelId = sp.TNat,
            ipfsHash = sp.TString,
            receivers = sp.TList(sp.TAddress)
        ))
  
        sp.verify(
            (sp.sender == self.data.channels[params.channelId].owner) | (self.data.channels[params.channelId].managers.contains(sp.sender)),
            message = "NOT_OWNER_OR_MANAGER"
        )

        sp.for x in params.receivers:
            sp.verify(self.data.subscribers[x].contains(params.channelId), message="NOT_SUBSCRIBER")
        
        self.data.selectiveNotifications[self.data.selectiveNotificationId] = sp.record(
            channelId = params.channelId,
            ipfsHash = params.ipfsHash,
            receivers = params.receivers
        )

        self.data.selectiveNotificationId += 1


  