import subprocess
import json
import os
import time
import random

ordPath = 'E:\\Bitcoin\\ord-0.15.0\\ord' #put your path here

def load_data_from_json(file_path, key):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data.get(key, [])

def createWallet(i):
    result = subprocess.run([ordPath, '-s', 'wallet', '--name', str(i), 'create'], capture_output=True, text=True)
    if result.returncode == 0:
        output_data = json.loads(result.stdout)
        mnemonic = output_data.get("mnemonic")
        print('Creating wallet # ' + str(i))
        print('Mnemonic: ' + mnemonic)
        result = subprocess.run([ordPath, '-s', 'wallet', '--name', str(i), 'receive'], capture_output=True, text=True)
        if result.returncode == 0:
            output_data = json.loads(result.stdout)
            address = output_data.get("address")
            print('Address' + address)
            if mnemonic is not None:
                # Read existing data from the JSON file if it exists
                wallets = []
                if os.path.exists('wallets.json') and os.path.getsize('wallets.json') > 0:
                    try:
                        with open('wallets.json', 'r') as f:
                            wallets = json.load(f)
                    except json.decoder.JSONDecodeError:
                        # Handle the case when the file is empty
                        print("Empty or invalid JSON file. Starting with an empty list of wallets.")
               
                wallets.append({'index': i, 'mnemonic': mnemonic, 'address': address})
  
                with open('wallets.json', 'w') as f:
                    json.dump(wallets, f, indent=4)
                
                if checkBalance('vault') > 10500:
                    #fund this wallet from the vault
                    subprocess.run([ordPath, '-s',  'wallet', '--name', 'vault', 'send', '--fee-rate', '1', address, '10400sats'])
                else:
                    print("Not enough sats in the vault!")              

                while True:
                    if checkBalance(i) > 0:
                        break
                    else:
                        print("Txn hasn't gone through yet! Waiting for funds...")
                        time.sleep(10)  # Wait for 10 seconds before checking again                 
            else:
                print("Error creating a wallet.")
        else:
            print("Error:", result.stderr)
    else:
        # Print an error message if the subprocess failed
        print("Error:", result.stderr)

def createRune(i):
    if checkBalance(i) > 10200:
        
        result = subprocess.run([ordPath, '--index-runes', '-s', 'wallet', '--name', str(i), 'etch', '--divisibility', '4', '--fee-rate', '1', '--rune', runeNames[i], '--supply', str(random.randint(1,50)*1000000), '--symbol', runeNames[i][0]], capture_output=True, text=True)
        if result.returncode == 0:
            print('Rune ' + runeNames[i] + ' is being etched...')
            
        else:
            print("Error:", result.stderr)


def checkBalance(quary):

    result = subprocess.run([ordPath, '-s',  'wallet', '--name', str(quary), 'balance'], capture_output=True, text=True)

    if result.returncode == 0:
        output_data = json.loads(result.stdout)
        # Extract and print the number of cardinals
        cardinals = output_data.get("cardinal")
        if cardinals is not None:
            print("Number of cardinals:", cardinals)
            return cardinals
        else:
            print("Cardinals not found in the output.")
    else:
        print("Error:", result.stderr)


rune_names_file = 'rune_names.json'
runeNames = load_data_from_json(rune_names_file, 'runeNames')


# Check if the JSON file exists, if not, create an empty dictionary
if os.path.exists('wallets.json') and os.path.getsize('wallets.json') > 0:
    with open('wallets.json', 'r') as f:
        # Load the JSON data
        wallets = json.load(f)
        
        last_index = 0
        
        if wallets:
            for wallet in wallets:
                index = wallet.get('index', 0)
                
                if index > last_index:
                    last_index = index
            
            print("Last index:", last_index)
else:
    print("wallets.json is empty")
    last_index = -1  # Start from -1 to include wallet with index 0

for i in range(last_index + 1, len(runeNames) - 1):  # Start from last_index + 1 to include wallet with index 0
    createWallet(i)
    time.sleep(10)
    createRune(i)

def checkRunes(i):
    result = subprocess.run([ordPath, '-s',  'wallet', '--name', str(i), 'balance'], capture_output=True, text=True)

    if result.returncode == 0:
        # Parse the output as JSON
        output_data = json.loads(result.stdout)
        runic = output_data.get("runic")
        if runic <10000:
            print("No runes in wallet ", i)
    else:
        print("Error:", result.stderr)

print("Ran out of Rune names, checking rune-less wallets...")
for i in range(0, len(runeNames) - 1):
    checkRunes(i)
