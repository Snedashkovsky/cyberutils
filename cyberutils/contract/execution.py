from jsonschema import validate
from typing import Optional, Union

from cyber_sdk.client.lcd import LCDClient
from cyber_sdk.client.lcd.api.tx import CreateTxOptions, BlockTxBroadcastResult, SignerOptions
from cyber_sdk.client.lcd.wallet import Wallet
from cyber_sdk.core import Coin, Coins, AccAddress
from cyber_sdk.core.fee import Fee
from cyber_sdk.core.tx import Tx
from cyber_sdk.core.wasm import MsgExecuteContract
from cyber_sdk.exceptions import LCDResponseError


def execute_contract(execute_msgs: list[dict],
                     contract_address: str,
                     lcd_client: LCDClient,
                     fee_denom: str,
                     fee_amount: int = 0,
                     gas: int = 300_000,
                     wallet: Optional[Wallet] = None,
                     sender: Optional[Union[str, AccAddress]] = None,
                     sign_and_broadcast_tx: bool = True,
                     contract_execute_schema: Optional[dict] = None,
                     memo: Optional[str] = None) -> Optional[Union[BlockTxBroadcastResult, Tx]]:
    """
    Execute contract list of messages for a contract in a transaction or get an unsigned transaction
    :param execute_msgs: list of execute messages
    :param contract_address: contract address
    :param lcd_client: network LCD client
    :param gas: amount of gas
    :param fee_amount: fee amount
    :param fee_denom: fee denom
    :param wallet: executable wallet
    :param sender: transaction sender address
    :param sign_and_broadcast_tx: sign and broadcast a transaction if true, otherwise return an unsigned transaction
    :param contract_execute_schema: schema of contract execute messages for message validation
    :param memo: note(memo) of a transaction
    :return: a transaction result or an unsigned transaction
    """
    assert ((wallet or sender) and not sign_and_broadcast_tx) or (wallet and sign_and_broadcast_tx)
    if contract_execute_schema:
        for _execute_msg in execute_msgs:
            validate(_execute_msg, contract_execute_schema)

    _sender = wallet.key.acc_address if sender is None else AccAddress(sender)
    _msgs = \
        [MsgExecuteContract(
            sender=_sender,
            contract=AccAddress(contract_address),
            execute_msg=execute_msg) for execute_msg in execute_msgs]

    if sign_and_broadcast_tx is False:
        return lcd_client.tx.create(
            signers=[SignerOptions(address=_sender)],
            options=CreateTxOptions(
                msgs=_msgs,
                memo=memo,
                fee=Fee(gas, Coins([Coin(amount=fee_amount, denom=fee_denom)]))
            )
        )

    _tx_signed = wallet.create_and_sign_tx(
        CreateTxOptions(
            msgs=_msgs,
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
