from typing import Optional

from cyber_sdk.client.lcd.api.tx import CreateTxOptions, BlockTxBroadcastResult
from cyber_sdk.client.lcd import LCDClient
from cyber_sdk.core.fee import Fee
from cyber_sdk.core import Coin, Coins, AccAddress
from cyber_sdk.exceptions import LCDResponseError
from cyber_sdk.core.wasm import MsgExecuteContract
from cyber_sdk.client.lcd.wallet import Wallet


def execute_contract(execute_msgs: list[dict], wallet: Wallet, contract_address: str, lcd_client: LCDClient, gas: int,
                     fee_amount: int, fee_denom: str, memo: Optional[str] = None) -> Optional[BlockTxBroadcastResult]:
    """
    Execute contract list of messages for a contract in a transaction
    :param execute_msgs: list of execute messages
    :param wallet: executable wallet
    :param contract_address: contract address
    :param lcd_client: network LCD client
    :param gas: amount of gas
    :param fee_amount: fee amount
    :param fee_denom: fee denom
    :param memo: note(memo) of a transaction
    :return: transaction result
    """

    _msgs = \
        [MsgExecuteContract(
            sender=wallet.key.acc_address,
            contract=AccAddress(contract_address),
            execute_msg=execute_msg) for execute_msg in execute_msgs]

    _tx_signed = wallet.create_and_sign_tx(
        CreateTxOptions(
            msgs=_msgs,
            memo=memo,
            fee=Fee(gas, Coins([Coin(amount=fee_amount, denom=fee_denom)]))
        ))

    try:
        _tx_broadcasted = lcd_client.tx.broadcast(_tx_signed)
        return _tx_broadcasted
    except LCDResponseError as _e:
        print(f'LCDResponseError: {_e}')
        return None
