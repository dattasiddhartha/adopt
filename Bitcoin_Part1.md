## We will:
1. Create a custom Bitcoin script to lock funds with a secret phrase
2. Create a custom P2SH from this script. 
3. Send funds to the P2SH address. 

### Regtest node setup 
Start bitcoind
`$ bitcoind -regtest -daemon`

Generate 101 blocks to make coinbase transaction spendable
`$ bitcoin-cli -regtest generatetoaddress 101 $(bitcoin-cli -regtest getnewaddress)`

### Setting up wallets

Create a new address for alice
```
bitcoin-cli -regtest getnewaddress
2N5Grctt7U7CobTm61bLYAcbLT1N3QsMn76

ALICE_ADDRESS=2N5Grctt7U7CobTm61bLYAcbLT1N3QsMn76
```
Give alice 10 BTC and save the relevant TXID

```
$ bitcoin-cli -regtest sendtoaddress $ALICE_ADDRESS 10.00
6fc3f8becc38a1c445277dc9be6652a10810fd936eabdee61b3ee0a1b6e0492d

$ ALICE_FUNDING_TXID=6fc3f8becc38a1c445277dc9be6652a10810fd936eabdee61b3ee0a1b6e0492d
```
Mine another block to confirm the funding tx 

```
$ bitcoin-cli -regtest generatetoaddress 1 2MwAf8wHdqD4FBSML8SBvGdW42wY8221XqX
[
  "091b09f018547792aa7905c47ddbf08950af94a533e46025c5f4d88711c68a2d"
]
```
Use the txid of the funding tx to get the txhash and save it in a variable 
```
$ bitcoin-cli -regtest gettransaction 6fc3f8becc38a1c445277dc9be6652a10810fd936eabdee61b3ee0a1b6e0492d
{
  "amount": 0.00000000,
  "fee": -0.00003320,
  "confirmations": 1,
  "blockhash": "091b09f018547792aa7905c47ddbf08950af94a533e46025c5f4d88711c68a2d",
  "blockindex": 1,
  "blocktime": 1588503158,
  "txid": "6fc3f8becc38a1c445277dc9be6652a10810fd936eabdee61b3ee0a1b6e0492d",
  "walletconflicts": [
  ],
  "time": 1588501302,
  "timereceived": 1588501302,
  "bip125-replaceable": "no",
  "details": [
    {
      "address": "2N5Grctt7U7CobTm61bLYAcbLT1N3QsMn76",
      "category": "send",
      "amount": -10.00000000,
      "label": "",
      "vout": 1,
      "fee": -0.00003320,
      "abandoned": false
    },
    {
      "address": "2N5Grctt7U7CobTm61bLYAcbLT1N3QsMn76",
      "category": "receive",
      "amount": 10.00000000,
      "label": "",
      "vout": 1
    }
  ],
  "hex": "020000000001019f10ca32e610b8b9de9e0e643fa11171f182c51ee41da207a25a50e2364f58390000000017160014afb598dfef37d4891302e9ecd5feda23160f44eafeffffff02081b6bee0000000017a9142b036ab41308027b620994703ac3eddfe50480c88700ca9a3b0000000017a91483f080ea84030245fccfa93f809eecb2dee36541870247304402207e5bbef9c7d000b8a4d78c1a468a693bdbb44d3a259359092c7a23503fde75d3022016006a1da2ea31e3acb1e958df510e0132d936818d29458e8491a0c5f85901ce01210273c4dbd6930b51529184d076f49b88248a5ec863bbe97cf36a7245f3b96a98b565000000"
}

$ ALICE_FUNDING_TX=020000000001019f10ca32e610b8b9de9e0e643fa11171f182c51ee41da207a25a50e2364f58390000000017160014afb598dfef37d4891302e9ecd5feda23160f44eafeffffff02081b6bee0000000017a9142b036ab41308027b620994703ac3eddfe50480c88700ca9a3b0000000017a91483f080ea84030245fccfa93f809eecb2dee36541870247304402207e5bbef9c7d000b8a4d78c1a468a693bdbb44d3a259359092c7a23503fde75d3022016006a1da2ea31e3acb1e958df510e0132d936818d29458e8491a0c5f85901ce01210273c4dbd6930b51529184d076f49b88248a5ec863bbe97cf36a7245f3b96a98b565000000
```
### Writing Bitcoin Script (smart contract) 

Think of a magic number (secret) and convert it to a little endian hex number. Calculate RIPEMD160(SHA256(secret)). Write the locking script as follows:

`OP_HASH160 <RIPEMD160(SHA256(secret))> OP_EQUALVERIFY`

Use btcc to convert it into hex 

```
$ btcc OP_HASH160 a721871f056154b5d43efa609d63c95aae1facbc OP_EQUALVERIFY
a914a721871f056154b5d43efa609d63c95aae1facbc88
$ LOCKING_SCRIPT=a914a721871f056154b5d43efa609d63c95aae1facbc88
```

### Sending funds to smart contract 

Obtain the P2SH address to which Alice will send her funds

```
$ bitcoin-cli -regtest decodescript $LOCKING_SCRIPT
{
  "asm": "OP_HASH160 a721871f056154b5d43efa609d63c95aae1facbc OP_EQUALVERIFY",
  "type": "nonstandard",
  "p2sh": "2N4GMhsfZE7xg88JHLQK42FexSaRRKTnpao",
  "segwit": {
    "asm": "0 ee3a5c33a08b5a01bb7199e6163dfc37a237caf1f5895beff58919e0809cb9f3",
    "hex": "0020ee3a5c33a08b5a01bb7199e6163dfc37a237caf1f5895beff58919e0809cb9f3",
    "reqSigs": 1,
    "type": "witness_v0_scripthash",
    "addresses": [
      "bcrt1qaca9cvaq3ddqrwm3n8npv00ux73r0jh37ky4hml43yv7pqyuh8esfyrk3y"
    ],
    "p2sh-segwit": "2N3VaeXZrUQ6J89Jhf2dqUGJNjvtXumQBeS"
  }
}

$ LOCKING_SCRIPT_ADDRESS=bcrt1qaca9cvaq3ddqrwm3n8npv00ux73r0jh37ky4hml43yv7pqyuh8esfyrk3y
```

Create the transaction using the funding TXID as the input (make sure vout corresponds to the UTXO within the transaction you select)

```
$ bitcoin-cli -regtest createrawtransaction '''
→     [
→       {
→         "txid": "'$ALICE_FUNDING_TX_ID'",
→         "vout": '1'
→       }
→     ]
→     ''' '''
→     {
→       "'$LOCKING_SCRIPT_ADDRESS'": 9.9999
→     }'''
02000000012d49e0b6a1e03e1be6deab6e93fd1008a15266bec97d2745c4a138ccbef8c36f0100000000ffffffff01f0a29a3b00000000220020ee3a5c33a08b5a01bb7199e6163dfc37a237caf1f5895beff58919e0809cb9f300000000

$ RAW_TX=02000000012d49e0b6a1e03e1be6deab6e93fd1008a15266bec97d2745c4a138ccbef8c36f0100000000ffffffff01f0a29a3b00000000220020ee3a5c33a08b5a01bb7199e6163dfc37a237caf1f5895beff58919e0809cb9f300000000
```

Get Alice's private key so that we can sign the tx

```
$ bitcoin-cli -regtest dumpprivkey $ALICE_ADDRESS
cRUdv17UgDYZ5nhUazWFQLTRayXjbBpPUuGzAHfeC5xrm5xWND1n

$ ALICE_PRIVATE_KEY=cRUdv17UgDYZ5nhUazWFQLTRayXjbBpPUuGzAHfeC5xrm5xWND1n
```
Now sign the raw transaction with Alice's private key 

```
$ bitcoin-cli -regtest signrawtransactionwithkey $RAW_TX "[\"$ALICE_PRIVATE_KEY\"]"
{
  "hex": "020000000001012d49e0b6a1e03e1be6deab6e93fd1008a15266bec97d2745c4a138ccbef8c36f01000000171600144627657b1b2b14efcd5122dd0ed7ece91fd1a86affffffff01f0a29a3b00000000220020ee3a5c33a08b5a01bb7199e6163dfc37a237caf1f5895beff58919e0809cb9f30247304402203629beb38ce4df4a2da5873d14a8da0008438c6d510513e87171046b43d53f3002201c9729869050d49fbc83aea64ccbf5308de6ae144b4c16388599e6c7df39e152012103e0e812acc69a7476ba433a0a84682c195dda8018652ed76328208f5e40da06a700000000",
  "complete": true
}

$ SIGNED_RAW_TX=020000000001012d49e0b6a1e03e1be6deab6e93fd1008a15266bec97d2745c4a138ccbef8c36f01000000171600144627657b1b2b14efcd5122dd0ed7ece91fd1a86affffffff01f0a29a3b00000000220020ee3a5c33a08b5a01bb7199e6163dfc37a237caf1f5895beff58919e0809cb9f30247304402203629beb38ce4df4a2da5873d14a8da0008438c6d510513e87171046b43d53f3002201c9729869050d49fbc83aea64ccbf5308de6ae144b4c16388599e6c7df39e152012103e0e812acc69a7476ba433a0a84682c195dda8018652ed76328208f5e40da06a700000000
```

Broadcast the transaction to the network and mine another block to confirm it 

```
bitcoin-cli -regtest sendrawtransaction $SIGNED_RAW_TX
89a632ea89333364c6513fd219e4a032e56f343b912d908f613fadeca93b9f8a

$ bitcoin-cli -regtest generatetoaddress 1 2MwAf8wHdqD4FBSML8SBvGdW42wY8221XqX
[
  "005d87ac28168bf56ea6d4c456504e093bc6a513af1f91b7d40e81bcde97209d"
]
```

TODO: 

-describe how to unlock and spend funds (Need to create tx from scratch as Bitcoin core doesn't support spending custom P2SH funds")

-add OP_CHECKLOCKTIMEVERIFY to locking script to enable custom expiry dates 

for discussion: should we enable the option seller to spend the funds with their private key at expiry if the option buyer does not exercise? or should we only allow spending of the funds via use of the magic number? my concern with allowing seller private key to be used is potential double spend risk

Notes: 
The address used when mining new blocks (2MwAf8wHdqD4FBSML8SBvGdW42wY8221XqX) is unimportant. This can just be thought of as the miner's address. 

To spend the funds, an unlocking script must be provided, which after execution, leaves elements on the stack that will cause the locking script (which runs on the same stack) to finish execution with either 0x1 at the top of the stack or an empty stack. Execution can be visualized using command line tools such as [btcdeb](https://github.com/kallewoof/btcdeb) or online tools such as [Bitcoin IDE](https://siminchen.github.io/bitcoinIDE/build/editor.html). NB btcdev also contains btcc, the script compiler used above. 

Potential issues with custom redeem script: https://bitcoin.stackexchange.com/questions/88661/bitcoin-raw-transaction-with-manually-created-redeem-script

