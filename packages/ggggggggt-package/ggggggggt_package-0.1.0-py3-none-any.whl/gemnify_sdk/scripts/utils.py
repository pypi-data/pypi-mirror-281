import json
import os
from decimal import Decimal
from eth_account import Account

# Get the absolute path of the current script
current_script_path = os.path.abspath(__file__)
base_dir = os.path.abspath(
    os.path.join(current_script_path, '..', '..', '..', '..')
)
package_dir = os.path.join(base_dir, 'gemnify-sdk-python')
contract_abis_dir = os.path.join(package_dir, "gemnify_sdk", "contracts", "abis")
contract_addresses_dir = os.path.join(package_dir, "gemnify_sdk", "contracts", "addresses")
print('base_dir', base_dir)

def get_contract_abi(contract_name):
    abi_file = os.path.join(contract_abis_dir, contract_name + ".json")
    return json.load(
        open(
            abi_file
        )
    )

def get_contract_address(contract_name, chain):
    addresses_file = os.path.join(contract_addresses_dir, chain + ".json")
    print(addresses_file)
    with open(addresses_file, 'r') as f:
        addresses_json = json.load(f)
        return addresses_json[contract_name]

def expand_number(number, decimals):
    multiplier = 10 ** decimals
    result = number * multiplier
    uint256_max_value = 2 ** 256 - 1
    if result > uint256_max_value:
        raise OverflowError("Result exceeds uint256 maximum value")
    return int(result)

def get_address_from_private_key(private_key):
    account = Account.from_key(private_key)
    address = account.address
    return address
