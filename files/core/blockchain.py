# myapp/blockchain.py

import json
import os
from web3 import Web3
from solcx import compile_source, install_solc, set_solc_version

CONTRACT_PATH = 'contract_address.json'
SOLC_VERSION = '0.8.0'
contract_source_code = """
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FileHashStorage {
    mapping(string => bytes32) private fileHashes;
    event HashStored(string indexed fileName, bytes32 fileHash);

    function storeHash(string memory fileName, bytes32 fileHash) public {
        fileHashes[fileName] = fileHash;
        emit HashStored(fileName, fileHash);
    }

    function getHash(string memory fileName) public view returns (bytes32) {
        return fileHashes[fileName];
    }
}
"""

def init_contract():
    install_solc(SOLC_VERSION)
    set_solc_version(SOLC_VERSION)

    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
    if not w3.is_connected():
        raise Exception("Brak połączenia z Ganache")
    w3.eth.default_account = w3.eth.accounts[0]

    compiled_sol = compile_source(contract_source_code, output_values=['abi', 'bin'])
    contract_id, contract_interface = compiled_sol.popitem()
    abi = contract_interface['abi']
    bytecode = contract_interface['bin']

    if os.path.exists(CONTRACT_PATH):
        with open(CONTRACT_PATH, 'r') as f:
            address = json.load(f)['address']
        contract = w3.eth.contract(address=address, abi=abi)
    else:
        contract_instance = w3.eth.contract(abi=abi, bytecode=bytecode)
        tx_hash = contract_instance.constructor().transact()
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        address = tx_receipt.contractAddress
        with open(CONTRACT_PATH, 'w') as f:
            json.dump({'address': address}, f)
        contract = w3.eth.contract(address=address, abi=abi)

    global file_hash_storage
    file_hash_storage = contract


def save_file_hash(file_name, file_hash) :
    tx_hash = file_hash_storage.functions.storeHash(file_name, file_hash).transact()
    return Web3.to_hex(tx_hash)

def get_and_verify_hash(file_name, input_hash):
    stored_hash = file_hash_storage.functions.getHash(file_name).call()
    return stored_hash == input_hash