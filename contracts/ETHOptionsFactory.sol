pragma solidity ^0.5.0;

import "./ETHCallOption.sol";
import "./ETHPutOption.sol";

contract ETHOptionsFactory {
    
    mapping(uint256 => mapping(uint256 => address)) private _call_option_contracts;
    mapping(uint256 => mapping(uint256 => address)) private _put_option_contracts;

    event CallOptionContractCreated(address indexed contract_address, uint256 expiration_timestamp, uint256 strike);
    event PutOptionContractCreated(address indexed contract_address, uint256 expiration_timestamp, uint256 strike);
    
    function callOptionContract(uint256 expiration_timestamp, uint256 strike) public view returns (address) {
        return _call_option_contracts[expiration_timestamp][strike];
    }
    
    function putOptionContract(uint256 expiration_timestamp, uint256 strike) public view returns (address) {
        return _put_option_contracts[expiration_timestamp][strike];
    }
    
    function createCallOptionContract(uint256 expiration_timestamp, uint256 strike) public returns (bool success) {
        
        // check valid expiration
        require(expiration_timestamp >= now, "Invalid expiration.");
        
        // check the contract was not already created
        require(_call_option_contracts[expiration_timestamp][strike] == address(0), "Contract already created.");
        
        // create new call option contract with the given parameters
        ETHCallOption call_option_contract = new ETHCallOption(expiration_timestamp, strike, "ETH Call Contract", "ETHCall");

        address call_option_contract_address = address(call_option_contract);

        _call_option_contracts[expiration_timestamp][strike] = call_option_contract_address;

        emit CallOptionContractCreated(call_option_contract_address, expiration_timestamp, strike);
        
        return true;
    }
    
    function createPutOptionContract(uint256 expiration_timestamp, uint256 strike) public returns (bool success) {

        // check valid expiration
        require(expiration_timestamp >= now, "Invalid expiration.");
        
        // check the contract was not already created
        require(_put_option_contracts[expiration_timestamp][strike] == address(0), "Contract already created.");
        
        // create new put option contract with the given parameters
        ETHPutOption put_option_contract = new ETHPutOption(expiration_timestamp, strike, "ETH Put Contract", "ETHPut");

        address put_option_contract_address = address(put_option_contract);

        _put_option_contracts[expiration_timestamp][strike] = put_option_contract_address;

        emit PutOptionContractCreated(put_option_contract_address, expiration_timestamp, strike);
        
        return true;
    }
}