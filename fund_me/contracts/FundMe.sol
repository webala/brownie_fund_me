// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <0.9.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;
    address public owner;

    constructor() public {
        //constructor is called automatically when the contract is deployed.
        owner = msg.sender;
    } 

    function fund() public payable {
        uint256 minimumUSD = 50 * 10**18;

        require(
            getConversionRate(msg.value) >= minimumUSD,
            "You need to spend more EHT!"
        );
        //msg.sender -> Sender of funds or caller of function
        //msg.value -> Amount funded
        //Both are key words in solidity
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getVersion() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
        );
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
        );
        (
            uint80 roundId,
            int256 answer,
            uint256 startedAt,
            uint256 updatedAt,
            uint80 answeredInRound
        ) = priceFeed.latestRoundData(); //returns a touple. A list of variables of potentially different types

        //roe unused vaiables can be ignored like so
        //(,int256 answer,,,) = priceFeed.latestRoundData();

        return uint256(answer * 10000000000); // type casting since return value is of uint256
    }

    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethAmount * ethPrice) / 1000000000000000000;
        return ethAmountInUsd;
    }

    //3332.49374413 -> the price has 8 decimals.

    //Modifiers -> Used to change the behaviour of a function in a declarative way.
    modifier onlyOwner() {
        require(msg.sender == owner);
        _; //This means to run the code after the above lines
    }

    function withdraw() public payable onlyOwner {
        uint256 amount = address(this).balance;
        payable(msg.sender).transfer(amount); //transfer all funds to sender of function call

        for (
            uint256 fundersIndex = 0;
            fundersIndex < funders.length;
            fundersIndex++
        ) {
            address funder = funders[fundersIndex];
            addressToAmountFunded[funder] = 0;
        }

        funders = new address[](0);
    }
}
