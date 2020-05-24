const ETHCallOption = artifacts.require("ETHCallOption");

module.exports = function(deployer) {
  deployer.deploy(ETHCallOption, Date.now() + Date.now()*2, 100, "ETH Call Contract", "ETHCall"); // expiration_timestamp, strike, "ETH Call Contract", "ETHCall"
};
