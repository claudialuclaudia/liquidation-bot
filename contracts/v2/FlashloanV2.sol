pragma solidity ^0.6.6;
pragma experimental ABIEncoderV2;

import "./aave/FlashLoanReceiverBaseV2.sol";
import "../../interfaces/v2/ILendingPoolAddressesProviderV2.sol";
import "../../interfaces/v2/ILendingPoolV2.sol";

contract FlashloanV2 is FlashLoanReceiverBaseV2, Withdrawable {
    struct LiquidationParams {
        address collateralAsset;
        address borrowedAsset;
        address user;
        uint256 debtToCover;
        bool useEthPath;
    }

    constructor(address _addressProvider) FlashLoanReceiverBaseV2(_addressProvider) public {}

    /**
     * @dev This function must be called only be the LENDING_POOL and takes care of repaying
     * active debt positions, migrating collateral and incurring new V2 debt token debt.
     *
     * @param assets The array of flash loaned assets used to repay debts.
     * @param amounts The array of flash loaned asset amounts used to repay debts.
     * @param premiums The array of premiums incurred as additional debts.
     * @param initiator The address that initiated the flash loan, unused.
     * @param params The byte array containing, in this case, the arrays of aTokens and aTokenAmounts.
     */
    //  lending pool calls this; only gives us flash loan if this goes through
    function executeOperation(
        address[] calldata assets,
        uint256[] calldata amounts,
        uint256[] calldata premiums,
        address initiator,
        bytes calldata params
    )
        external
        override
        returns (bool)
    {
        //
        // This contract now has the funds requested.
        // Your logic goes here.
        //
        require(msg.sender == address(LENDING_POOL), 'CALLER_MUST_BE_LENDING_POOL');
        LiquidationParams memory decodedParams = _decodeParams(params);
        require(assets.length == 1 && assets[0] == decodedParams.borrowedAsset, 'INCONSISTENT_PARAMS');

        _liquidateOnCompound(
            decodedParams.collateralAsset,
            decodedParams.borrowedAsset,
            decodedParams.user,
            decodedParams.debtToCover,
            decodedParams.useEthPath,
            amounts[0],
            premiums[0],
            initiator
        );

        // At the end of your logic above, this contract owes
        // the flashloaned amounts + premiums.
        // Therefore ensure your contract has enough to repay
        // these amounts.
        
        // Approve the LendingPool contract allowance to *pull* the owed amount
        for (uint i = 0; i < assets.length; i++) {
            uint amountOwing = amounts[i].add(premiums[i]);
            IERC20(assets[i]).approve(address(LENDING_POOL), amountOwing);
        }
        
        return true;
    }

    function _liquidateOnCompound(

    ) internal {
        //call liquidate on compound
        //CEther: function liquidateBorrow(address borrower, address cTokenCollateral) payable
        CEther cToken = CEther(0x3FDB...);
        CErc20 cTokenCollateral = CErc20(0x3FDA...);
        require(cToken.liquidateBorrow.value(100)(0xBorrower, cTokenCollateral) == 0, "borrower underwater??");
    }

    /**
        * @dev Decodes the information encoded in the flash loan params
        * @param params Additional variadic field to include extra params. Expected parameters:
        *   address collateralAsset The collateral asset to claim
        *   address borrowedAsset The asset that must be covered and will be exchanged to pay the flash loan premium
        *   address user The user address with a Health Factor below 1
        *   uint256 debtToCover The amount of debt to cover
        *   bool useEthPath Use WETH as connector path between the collateralAsset and borrowedAsset at Uniswap
        * @return LiquidationParams struct containing decoded params
    */
    function _decodeParams(bytes memory params) internal pure returns (LiquidationParams memory) {
        (
        address collateralAsset,
        address borrowedAsset,
        address user,
        uint256 debtToCover,
        bool useEthPath
        ) = abi.decode(params, (address, address, address, uint256, bool));

        return LiquidationParams(collateralAsset, borrowedAsset, user, debtToCover, useEthPath);
    }

    function _flashloan(address[] memory assets, uint256[] memory amounts) internal {
        address receiverAddress = address(this);

        address onBehalfOf = address(this);
        bytes memory params = "";
        uint16 referralCode = 0;

        uint256[] memory modes = new uint256[](assets.length);

        // 0 = no debt (flash), 1 = stable, 2 = variable
        for (uint256 i = 0; i < assets.length; i++) {
            modes[i] = 0;
        }

        //this is what's actually making the flash loan
        LENDING_POOL.flashLoan(
            receiverAddress,
            assets,
            amounts,
            modes,
            onBehalfOf,
            params,
            referralCode
        );
    }

    /*
     *  Flash multiple assets 
     */
    function flashloan(address[] memory assets, uint256[] memory amounts) public onlyOwner {
        _flashloan(assets, amounts);
    }

    /*
     *  Flash loan 1000000000000000000 wei (1 ether) worth of `_asset`
     */
    function flashloan(address _asset) public onlyOwner {
        bytes memory data = "";
        uint amount = 1 ether;

        address[] memory assets = new address[](1);
        assets[0] = _asset;

        uint256[] memory amounts = new uint256[](1);
        amounts[0] = amount;

        _flashloan(assets, amounts);
    }
}