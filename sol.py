import requests

def get_solana_balance(address):
    url = f"https://api.mainnet-beta.solana.com"
    headers = {"Content-Type": "application/json"}
    
    # Get balance
    balance_payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBalance",
        "params": [address]
    }
    balance_response = requests.post(url, json=balance_payload, headers=headers).json()
    balance = balance_response['result']['value'] / 10**9  # Convert lamports to SOL

    # Get transaction history
    tx_payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getConfirmedSignaturesForAddress2",
        "params": [address, {"limit": 1000}]
    }
    tx_response = requests.post(url, json=tx_payload, headers=headers).json()
    transactions = tx_response['result']

    received_amount = 0
    sent_amount = 0

    for tx in transactions:
        tx_info_payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getConfirmedTransaction",
            "params": [tx['signature']]
        }
        tx_info_response = requests.post(url, json=tx_info_payload, headers=headers).json()
        tx_info = tx_info_response['result']

        for instruction in tx_info['transaction']['message']['instructions']:
            if 'parsed' in instruction:
                parsed_info = instruction['parsed']['info']
                if parsed_info['destination'] == address:
                    received_amount += parsed_info['lamports']
                elif parsed_info['source'] == address:
                    sent_amount += parsed_info['lamports']

    received_amount /= 10**9  # Convert lamports to SOL
    sent_amount /= 10**9  # Convert lamports to SOL

    return {
        "balance": balance,
        "received_amount": received_amount,
        "sent_amount": sent_amount
    }

# Example usage
solana_address = "your_solana_address_here"
info = get_solana_balance(solana_address)
print(f"Balance: {info['balance']} SOL")
print(f"Received Amount: {info['received_amount']} SOL")
print(f"Sent Amount: {info['sent_amount']} SOL")
