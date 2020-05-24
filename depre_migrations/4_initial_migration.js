const ETHPutOption = artifacts.require("ETHPutOption");

module.exports = function(deployer) {
    deployer.deploy(ETHPutOption, Date.now() + Date.now() * 2, 100, "ETH Put Contract", "ETHPut");
};
