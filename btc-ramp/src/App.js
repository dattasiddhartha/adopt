import React, { Component } from 'react'
import ReactDOM from 'react-dom'
import Web3 from 'web3'
import './App.css'
import { pBTC } from 'ptokens-pbtc'

//Figure how to make web3 and ptokens-pbtc instances shared among Deposit and Redeem instances

class App extends Component {

  constructor(props) {
    super(props);
    this.state = { account: '', pbtc_instance: '', btcRedeemAddress:'', btcRedeemAmount: ''};
    this.onRedeemFieldUpdate = this.onRedeemFieldUpdate.bind(this);
    this.onAmountFieldUpdate = this.onAmountFieldUpdate.bind(this);
  }

  componentWillMount() {
    this.loadBlockchainData()
  }

  async loadBlockchainData() {
    const web3 = new Web3(Web3.givenProvider || "http://localhost:8545")
    const accounts = await web3.eth.getAccounts()
    const pbtc = new pBTC({
      ethProvider: window.web3.currentProvider,
      btcNetwork: 'testnet'
    })
    this.setState({ account: accounts[0], pbtc_instance: pbtc })
  }

  generateDepositAddress = async () => {
    const pbtc = this.state.pbtc_instance;
    const account = this.state.account;
    const depositAddress = await pbtc.getDepositAddress(account);
    console.log(depositAddress.toString());
    const tBTCaddress = (
      <div className="address">
        <h2>Deposit Address: </h2> 
        {depositAddress.toString()}
      </div>
    )
    ReactDOM.render(tBTCaddress, document.getElementById('depositAddress'));
  }

  generateWithdrawalPrompt() { 
    console.log("testing");
    const redeemAmount = this.state.btcRedeemAmount;
    const redeemAddress = this.state.btcRedeemAddress;
    const withdrawPrompt = (
      <div className="address">
        <h3>Confirm withdrawal of {redeemAmount} to {redeemAddress} </h3> 
        <button onClick={this.redeemPBTCtoBTC}> Confirm </button> 
      </div>
    )
    ReactDOM.render(withdrawPrompt, document.getElementById('withdrawPrompt'));
  }

  onRedeemFieldUpdate(event) {
    this.setState({btcRedeemAddress: event.target.value})
    console.log(this.state.btcRedeemAddress)
  }

  onAmountFieldUpdate(event) {
    this.setState({btcRedeemAmount: event.target.value})
    console.log(this.state.btcRedeemAmount)
  }

  redeemPBTCtoBTC = async () => {
    const pbtc = this.state.pbtc_instance;
    //TODO: check user account balance to make sure they have enough funds 
    const amountToRedeem = this.state.btcRedeemAmount
    const redeemAddress = this.state.btcRedeemAddress

    let ethTxIsConfirmed = false
    let nodeHasReceivedTx = false
    let nodeHasBroadcastedTx = false
    let btcTxIsConfirmed = false
    const start = () =>
      new Promise(resolve => {
        pbtc
          .redeem(amountToRedeem, this.state.btcRedeemAddress)
          .once('onEthTxConfirmed', () => {
            ethTxIsConfirmed = true
          })
          .once('onNodeReceivedTx', () => {
            nodeHasReceivedTx = true
          })
          .once('onNodeBroadcastedTx', () => {
            nodeHasBroadcastedTx = true
          })
          .once('onBtcTxConfirmed', () => {
            btcTxIsConfirmed = true
          })
          .then(() => resolve())
      })
    await start()
  }

  render() {
    return (
      <div className="container">
        <h1>BTC ↔ pBTC (testnet)</h1>
        <p>Your ETH address: {this.state.account}</p>
        <button onClick={this.generateDepositAddress}> Deposit BTC </button>
        <div id="depositAddress">
        </div>
        <div id="redeemAddress">
        <h2>Withdraw BTC: </h2> 
        <h3> Withdrawal Address:</h3>
        <input type="text" value={this.state.redeemAddress} onChange={this.onRedeemFieldUpdate}/>
        <h3> Withdrawal Amount:</h3>
        <input type="number" step='0.00000001' value={this.state.redeemAddress} onChange={this.onAmountFieldUpdate}/>
        <button onClick={() => this.generateWithdrawalPrompt()}> Withdraw BTC to this Address </button>
        <div id="withdrawPrompt"> 
        </div> 
        </div>
      </div>
    );
  }
}

export default App;