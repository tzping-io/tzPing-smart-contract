# channel

## create channel
stake some amount of token

## managers
the addresses which can create notifications through channel
(optional) - to add manager pay some token 

## owner
can delete channel, change managers and change admin

## subscribers
big_map. address -> set(subsribed channel ids)

## total subscribers
keep this no. inside channel info

## notification
send by only managers
requires ipfs hash of notification payload
send to everyone in this channel
send to some addresses only while checking that the addres is the subscriber

## advertisement
1 token per adv. per user
(optional) -> disable this

# token
-> add the subscriber to FA2 token ledger when he subscribes for the first time to channel
