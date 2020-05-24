//Test functionality
//1. Initialize an option

const ETHOptionsFactory = artifacts.require('./contracts/ETHOptionsFactory.sol') // Create option contracts
const ETHPutOption = artifacts.require('./contracts/ETHPutOption.sol') // Manipulate option contracts
const assert = require('assert')

let contractInstance_creation
let contractInstance

contract('ETHPutOption', (accounts) => {
    // static variables kept constant
    before(async () => {
        expiration_ts = Date.now() + Date.now() * 2
        strike_price = 1
    })

    beforeEach(async () => {
        contractInstance_creation = await ETHOptionsFactory.deployed()
        contractInstance = await ETHPutOption.deployed()
    })

    //Test 1
    // Assume only 1 contract of specific ts & strike can exist concurrently
    it('Initialize put option contract', async () => {
        const contract_status = await contractInstance_creation.createPutOptionContract(expiration_ts, strike_price)
        console.log("Expiration time: ", expiration_ts)
        console.log(contract_status)
        //assert.equal(contract_status, true)
    })

    // Test 2
    //  address of the specific contract created
    //it('View outstanding put option contract', async () => {
    //    const contract_status = await contractInstance_creation.putOptionContract(expiration_ts, strike_price)
    //    console.log(contract_status)
        //console.log(expiration_ts)
        //assert.equal(todoContent, 'this is a short text', 'The content of the new added todo is not correct')
    //})

    // Test 3
    //  write option, send contribution
    //it('Write option', async () => {
    //    console.log(Date.now())
        //const contract_status = await contractInstance.writeOption(1)
    //    const contract_status = await contractInstance.writeOption({ value: web3.utils.toWei('1', 'ether') })
    //    console.log(contract_status)
    //})

    // Test 3
    //  exercise option
    it('Exercise option', async () => {
        //console.log(balanceOf(accounts[0]))
        const contract_status = await contractInstance.exerciseOption(accounts[1], 1)
        console.log(contract_status)
    })

    // Test n
    // Contributor of the contract
    //it('contribution', async () => {
    //    await contractInstance.contribution(accounts[0])
    //    const acc_contributor = await contractInstance.contribution(accounts[0])
    //    console.log("Contribution: ", acc_contributor)
    //})

    // Test n
    // Contributor of the contract
    it('claim contribution', async () => {
        await contractInstance.claimContribution()
        const acc_contributor = await contractInstance.claimContribution()
        //console.log(acc_contributor)
    })

    // Test n
    // Deletion can only occur after contract is expired
    //it('deleteContract', async () => {
    //    await contractInstance.deleteContract()
    //})

})