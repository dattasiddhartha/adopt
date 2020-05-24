//pragma solidity >=0.6.0 <0.7.0;
pragma solidity ^0.5.0;

import "../node_modules/openzeppelin-solidity/contracts/token/ERC20/ERC20.sol";
import "../node_modules/openzeppelin-solidity/contracts/token/ERC20/ERC20Detailed.sol";
import "../node_modules/openzeppelin-solidity/contracts/math/SafeMath.sol";

import "../node_modules/openzeppelin-solidity/contracts/token/ERC777/ERC777.sol";
import "../node_modules/openzeppelin-solidity/contracts/token/ERC777/IERC777.sol";
import "../node_modules/openzeppelin-solidity/contracts/introspection/IERC1820Registry.sol";
import "../node_modules/openzeppelin-solidity/contracts/token/ERC777/IERC777Recipient.sol";
//import "@nomiclabs/buidler/console.sol";

contract ETHCallOption is ERC20, ERC20Detailed, IERC777Recipient {
    using SafeMath for uint256;
    
    uint256 private _expiration_timestamp;
    uint256 private _strike;
    
    mapping(address => uint) private _contributions;
    uint256 private _total_contribution;
    
    ERC20 constant private DAI_CONTRACT = ERC20(0x00D811B7d33cECCFcb7435F14cCC274a31CE7F5d);
    ERC777 constant private PBTC_CONTRACT = ERC777(0xEB770B1883Dcce11781649E8c4F1ac5F4B40C978);
    
    event OptionExercised(address indexed owner, uint256 amount);
    event OptionWrote(address indexed writer, uint256 amount);
    //event ReceivedPBTC(address indexed writer, uint256 amount);
    //event ReceivedPBTC(operator, from, to, amount, userData, operatorData);

    IERC1820Registry private _erc1820 = IERC1820Registry(0x1820a4B7618BdE71Dce8cdc73aAB6C95905faD24);
    bytes32 constant private TOKENS_RECIPIENT_INTERFACE_HASH = keccak256("ERC777TokensRecipient");

    constructor(uint256 expiration_timestamp, uint256 strike, string memory name, string memory symbol)
        ERC20Detailed(name, symbol, 18)
        public
        payable
    {
        _expiration_timestamp = expiration_timestamp;
        _strike = strike;
        _erc1820.setInterfaceImplementer(address(this), TOKENS_RECIPIENT_INTERFACE_HASH, address(this));
    }

function tokensReceived(
        address operator,
        address from,
        address to,
        uint256 amount,
        bytes calldata userData,
        bytes calldata operatorData
    ) external {
        require(msg.sender == address(PBTC_CONTRACT), "Invalid token");

        // do stuff
        //emit ReceivedPBTC(operator, from, to, amount, userData, operatorData);
    }
    
    function contribution(address contributor) public view returns (uint256) {
        return _contributions[contributor];
    }
    
    modifier beforeExpiration() {
        require(block.timestamp <= _expiration_timestamp, "Option contract has expired."); // <=
        _;
    }

    function exerciseOption(address payable exercisor, uint256 amount) public beforeExpiration returns (bool success) {
        if(exercisor != msg.sender){
            require(allowance(exercisor, msg.sender) >= amount, "Unauthorized exercise");
        }
        require(balanceOf(exercisor) >= amount, "Not enough option tokens owned");
        _burn(exercisor, amount);
        require(DAI_CONTRACT.transferFrom(exercisor, address(this), amount * _strike), "DAI transfer unsuccessful");
        exercisor.transfer(amount);
        emit OptionExercised(exercisor, amount);
        return true;
    }
    
    //Just realized msg.sender is going to be the pBTC contract address and not the actual sender address...Oops!
    function writeOption(uint256 amount) public payable returns (bool success) {
        require(PBTC_CONTRACT.transferFrom(msg.sender, address(this), amount), "pBTC transfer unsuccessful");
        _contributions[msg.sender] = amount;
        _total_contribution.add(amount);
        _mint(msg.sender, amount);
        emit OptionWrote(msg.sender, msg.value);
        return true;
    }
    
    // ETH as collateral version: 
    // function writeOption() public payable beforeExpiration returns (bool success) {
    //     require(msg.value > 0, "Must send eth to write option");
    //     _contributions[msg.sender] = msg.value;
    //     _total_contribution.add(msg.value);
    //     _mint(msg.sender, msg.value);
    //     emit OptionWrote(msg.sender, msg.value);
    //     //console.log(msg.value, msg.sender);
    //     return true;
    // }
    
    modifier afterExpiration() {
        require(block.timestamp > _expiration_timestamp, "Option contract has not expired."); // >
        _;
    }
    
    function claimContribution() public afterExpiration returns (bool success) {

        require(_contributions[msg.sender] > 0, "No contribution found");
        
        uint256 total_balance_wei = address(this).balance;
        uint256 claimer_proportion_wei_num = total_balance_wei.mul(_contributions[msg.sender]);
        uint256 claimer_proportion_wei = claimer_proportion_wei_num.div(_total_contribution);

        uint256 total_balance_dai = DAI_CONTRACT.balanceOf(address(this));
        uint256 claimer_proportion_dai_num = total_balance_dai.mul(_contributions[msg.sender]);
        uint256 claimer_proportion_dai = claimer_proportion_dai_num.div(_total_contribution);

        _total_contribution.sub(_contributions[msg.sender]);
        _contributions[msg.sender] = 0;

        if(claimer_proportion_dai > 0){
            DAI_CONTRACT.transfer(msg.sender, claimer_proportion_dai);
        }
        
        if(claimer_proportion_wei > 0){
            msg.sender.transfer(claimer_proportion_wei);
        }
        
        return true;
    }
    
    function deleteContract() public afterExpiration {

        uint256 total_balance_eth = address(this).balance;
        uint256 total_balance_dai = DAI_CONTRACT.balanceOf(address(this));
        
        if(total_balance_eth == 0 && total_balance_dai == 0){
            selfdestruct(msg.sender);
        }
    }

}
