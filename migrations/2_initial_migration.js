const ETHOptionsFactory = artifacts.require("ETHOptionsFactory");

module.exports = function(deployer) {
  deployer.deploy(ETHOptionsFactory);
};
