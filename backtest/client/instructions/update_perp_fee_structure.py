from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class UpdatePerpFeeStructureArgs(typing.TypedDict):
    fee_structure: types.fee_structure.FeeStructure


layout = borsh.CStruct("fee_structure" / types.fee_structure.FeeStructure.layout)


class UpdatePerpFeeStructureAccounts(typing.TypedDict):
    admin: PublicKey
    state: PublicKey


def update_perp_fee_structure(
    args: UpdatePerpFeeStructureArgs,
    accounts: UpdatePerpFeeStructureAccounts,
    program_id: PublicKey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=True),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x17\xb2o\xcbI\x16\x8cK"
    encoded_args = layout.build(
        {
            "fee_structure": args["fee_structure"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, program_id, data)
