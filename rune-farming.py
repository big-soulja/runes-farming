import subprocess
import json
import os
import time
import random
import create_batch_svg
from data.wordList import words

#path to your ord
ordPath = 'ord'
#bitcoin network
network = '-r'
# datadir = '--datadir=E:\env'
# 3 words are combined into 1 rune name, pt here as many as you'd like but has to be divisible by 3
words = words
print(words)

def createWallet(i):
    result = subprocess.run([ordPath, network, 'wallet', '--name', str(i), 'create'], capture_output=True, text=True)
    if result.returncode == 0:
        output_data = json.loads(result.stdout)
        mnemonic = output_data.get("mnemonic")
        print('Creating wallet # ' + str(i))
        print('Mnemonic: ' + mnemonic)
        result = subprocess.run([ordPath, network, 'wallet', '--name', str(i), 'receive'], capture_output=True, text=True)
        print(result)
        if result.returncode == 0:
            output_data = json.loads(result.stdout)
            address = output_data.get("addresses")[0]
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
                
                if checkBalance('vault') > 21000:
                    #fund this wallet from the ord
                    subprocess.run([ordPath, network, 'wallet', '--name', 'vault', 'send', '--fee-rate', '1', address, '21000sats'])
                else:
                    print("Not enough sats in the vault!")              

                while True:
                    if checkBalance(i) > 0:
                        break
                    else:
                        print("Txn hasn't gone through yet! Waiting for funds...")
                        time.sleep(30)  # Wait for 30 seconds before checking again                 
            else:
                print("Error creating a wallet.")
        else:
            print("Error:", result.stderr)
    else:
        # Print an error message if the subprocess failed
        print("Error:", result.stderr)

def createRune(last_index, i):
    if checkBalance(i) >= 21000:
        runeNumber = i - last_index
        print('Rune number ' + str(runeNumber) + ' is being etched...')
        create_batch_svg.createBatch(runeNumber, words)
        result = subprocess.run([ordPath, '--index-runes', network, 'wallet', '--name', str(i), 'batch', '--fee-rate', '1', '--batch', '/r1b.yaml'], capture_output=True, text=True)
        print(result)
        if result.returncode == 0:
            output_data = json.loads(result.stdout)
            print(output_data)
            print('Rune number ' + str(runeNumber) + ' has been etched...')
            
        else:
            print("Error:", result.stderr)


def checkBalance(quary):

    result = subprocess.run([ordPath, network, 'wallet', '--name', str(quary), 'balance'], capture_output=True, text=True)

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



def main():
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

    print("Last index = " + str(last_index))

    for i in range(last_index + 1, last_index + int(len(words)/3) - 1):  # Start from last_index + 1 to include wallet with index 0
        print(last_index + 1)
        print(last_index + int(len(words)/3) - 1)
        if checkBalance('vault') < 21000:
            print("No enough sats in the vault...")
            break
        createWallet(i)
        time.sleep(10)
        createRune(last_index, i)


if __name__=='__main__':
    main()
