from typing import Optional, Union

from cyber_sdk.client.lcd import LCDClient
from cyber_sdk.client.lcd.api.tx import CreateTxOptions, BlockTxBroadcastResult, SignerOptions
from cyber_sdk.client.lcd.wallet import Wallet
from cyber_sdk.core import Coin, Coins, AccAddress
from cyber_sdk.core.fee import Fee
from cyber_sdk.core.tx import Tx
from cyber_sdk.core.wasm import MsgInstantiateContract
from cyber_sdk.exceptions import LCDResponseError


def instantiate_contract(
        init_msg: dict,
        code_id: int,
        label: str,
        lcd_client: LCDClient,
        fee_denom: str,
        fee_amount: int = 0,
        gas: int = 300_000,
        init_coins: Optional[Coins] = None,
        wallet: Optional[Wallet] = None,
        sender: Optional[Union[str, AccAddress]] = None,
        admin: Optional[Union[str, AccAddress]] = None,
        sign_and_broadcast_tx: bool = True,
        memo: Optional[str] = None) -> Optional[Union[BlockTxBroadcastResult, Tx]]:
    """
    Execute a contract instantiations or get an unsigned transaction
    :param init_msg: list of instantiate messages
    :param init_coins: coins for a contract instantiation
    :param code_id: code id
    :param label: contract label
    :param lcd_client: network LCD client
    :param gas: amount of gas
    :param fee_amount: fee amount
    :param fee_denom: fee denom
    :param wallet: executable wallet
    :param sender: transaction sender address
    :param admin: contract admin
    :param sign_and_broadcast_tx: sign and broadcast a transaction if true, otherwise return an unsigned transaction
    :param memo: note(memo) of a transaction
    :return: a transaction result or an unsigned transaction
    """
    assert ((wallet or sender) and not sign_and_broadcast_tx) or (wallet and sign_and_broadcast_tx)
    _sender = wallet.key.acc_address if sender is None else AccAddress(sender)
    _init_coins = Coins() if init_coins is None else init_coins

    # TODO test after cyber_sdk upgrade (need to add the `label` parameter)

    _msg = \
        MsgInstantiateContract(
            sender=_sender,
            admin=admin,
            code_id=code_id,
            init_msg=init_msg,
            init_coins=_init_coins,
            label=label)

    if sign_and_broadcast_tx is False:
        return lcd_client.tx.create(
            signers=[SignerOptions(address=_sender)],
            options=CreateTxOptions(
                msgs=[_msg],
                memo=memo,
                fee=Fee(gas, Coins([Coin(amount=fee_amount, denom=fee_denom)]))
            )
        )

    _tx_signed = wallet.create_and_sign_tx(
        CreateTxOptions(
            msgs=[_msg],
            memo=memo,
            fee=Fee(gas, Coins([Coin(amount=fee_amount, denom=fee_denom)]))
        )
    )

    try:
        _tx_broadcasted = lcd_client.tx.broadcast(_tx_signed)
        return _tx_broadcasted
    except LCDResponseError as _e:
        print(f'LCDResponseError: {_e}')
        return None
