import smartpy as sp

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
                    token = sp.TRecord(
                        tokenAddress = sp.TAddress,
                        tokenId = sp.TNat
                    )
                )
            ),
            subscribers = sp.big_map(
                tkey = sp.TAddress,
                tvalue = sp.TRecord(
                    subscribedChannels = sp.TSet(sp.TNat),
                    showAdv = sp.TBool
                )
            ),
            notificationId = sp.nat(0),
            notifications = sp.big_map(
                tkey = sp.TNat,
                tvalue = sp.TRecord(
                    channelId = sp.TNat,
                    ipfsHash = sp.TString
                )
            )
        )

    @sp.entry_point
    def setAdmin(self, params):
        sp.set_type(params, sp.TAddress)

        sp.verify(sp.sender == self.data.admin, message="NOT_ADMIN")
        self.data.admin = params

    @sp.entry_point
    def createChannel(self, params):
        sp.set_type(params, sp.TRecord(
            managers = sp.TSet(sp.TAddress),
            ipfsHash = sp.TString,
            token = sp.TRecord(
                tokenAddress = sp.TAddress,
                tokenId = sp.TNat
            )
        ))

        # stake some tokens
        data_type = sp.TList(
            sp.TRecord(
                from_ = sp.TAddress, 
                txs = sp.TList(
                    sp.TRecord(
                        amount = sp.TNat,
                        to_ = sp.TAddress,
                        token_id = sp.TNat
                    ).layout(("to_", ("token_id", "amount")))
                )
            ).layout(("from_", "txs"))
        )

        c = sp.contract(data_type, params.token.tokenAddress, "transfer").open_some()

        data_to_be_sent = sp.list([
            sp.record(
                from_ = sp.sender, 
                txs = sp.list([
                    sp.record(
                        amount = 1000,
                        to_ = sp.self_address, 
                        token_id = params.token.tokenId
                    )
                ])
            )
        ])
        
        sp.transfer(data_to_be_sent, sp.mutez(0), c)

        self.data.channels[self.data.channelId] = sp.record(
            owner = sp.sender,
            managers = params.managers,
            totalSubscribers = sp.nat(0),
            ipfsHash = params.ipfsHash,
            token = params.token
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
    def deleteChannel(self, params):
        sp.set_type(params, sp.TNat)

        sp.verify(sp.sender == self.data.channels[params].owner, message="NOT_OWNER")
        del self.data.channels[params]

    # subscribers = sp.big_map(
    #             tkey = sp.TAddress,
    #             tvalue = sp.TRecord(
    #                 subscribedChannels = sp.TList(
    #                     sp.TRecord(
    #                         channelId = sp.TNat,
    #                         subscribedOrNot = sp.TBool
    #                     )
    #                 ),
    #                 showAdv = sp.TBool
    #             )
    #         ),

    @sp.entry_point
    def subscribe(self, params):
        sp.set_type(params, sp.TList(sp.TRecord(
            channelId = sp.TNat,
            subscribedOrNot = sp.TBool
        )))

        sp.if ~self.data.subscribers.contains(sp.sender):
            self.data.subscribers[sp.sender] = sp.record(
                subscribedChannels = sp.set(),
                showAdv = True
            )

        sp.for query in params:
            sp.if query.subscribedOrNot:
                self.data.subscribers[sp.sender].subscribedChannels.add(query.channelId)
                self.data.channels[query.channelId].totalSubscribers += 1
            sp.else:
                self.data.subscribers[sp.sender].subscribedChannels.remove(query.channelId)
                self.data.channels[query.channelId].totalSubscribers = sp.as_nat(self.data.channels[query.channelId].totalSubscribers - 1)

        
        

    # @sp.entry_point
    # def sendNotifications(self, params):
    #     pass

    # @sp.entry_point
    # def sendAdv(self, params):
    #     pass