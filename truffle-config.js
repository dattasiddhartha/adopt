/**
 * Use this file to configure your truffle project. It's seeded with some
 * common settings for different networks and features like migrations,
 * compilation and testing. Uncomment the ones you need or modify
 * them to suit your project as necessary.
 *
 * More information about configuration can be found at:
 *
 * truffleframework.com/docs/advanced/configuration
 *
 * To deploy via Infura you'll need a wallet provider (like truffle-hdwallet-provider)
 * to sign your transactions before they're sent to a remote public node. Infura accounts
 * are available for free at: infura.io/register.
 *
 * You'll also need a mnemonic - the twelve word phrase the wallet uses to generate
 * public/private key pairs. If you're publishing your code to GitHub make sure you load this
 * phrase from a file you've .gitignored so it doesn't accidentally become public.
 *
 */

// const HDWalletProvider = require('truffle-hdwallet-provider');
// const infuraKey = "fj4jll3k.....";
//
// const fs = require('fs');
// const mnemonic = fs.readFileSync(".secret").toString().trim();

var HDWalletProvider = require("truffle-hdwallet-provider");
var mnemonic = "return pen damp farm this milk length seven outside corn decorate bike";

module.exports = {
 networks: {
  development: {
      host: "127.0.0.1",     // Localhost (default: none)
          port: 7545,            // Standard Ethereum port (default: none)
      network_id: "5777",       // Any network (default: none)
     },
  ropsten: {
      provider: function() { 
       return new HDWalletProvider(mnemonic, "https://ropsten.infura.io/v3/864becafff9e424aa2ff8b65bb4337ec");
      },
      network_id: 3,
      gas: 2197, // 21975
      gasPrice: 4000000, // 20000000000
  }
    },
    compilers: {
        solc: {
            version: "0.5.0",    // Fetch exact version from solc-bin (default: truffle's version)
            // docker: true,        // Use "0.5.1" you've installed locally with docker (default: false)
            // settings: {          // See the solidity docs for advice about optimization and evmVersion
            //  optimizer: {
            //    enabled: false,
            //    runs: 200
            //  },
            //  evmVersion: "byzantium"
            // }
        }
    }
};
