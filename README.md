# runes-farming
This is a script that creates and funds wallets, etches a rune and moves on. 
You might need to put ```--cookie-file E:\synced\signet\.cookie``` after ord in all of these commands, plus in subprocess commands in rune-farming.py

Prerequisites:
1. Have a running signet node with ord installed https://docs.ordinals.com/guides/wallet.html, there's a good guide by victorbs in tfm.
2. Have some signet btc. https://signetfaucet.com/ is the go to faucet but not sure if it works.
3. VSCode or other compiler + python installed. Tutorial: https://www.youtube.com/watch?v=cUAK4x_7thA

Steps:
1. Clone this repostory to your local machine.
2. In command line cd into your ord directory and create a vault wallet with ```ord -s wallet --name vault create```, write down a mnemonic it gives you, then do ```ord -s wallet --name vault recieve```, also write down the address it gives. We need a completely new wallet with no runes or inscriptions in it.
3. Transfer your signet btc to this address with ```ord -s wallet --name YOURWALLETNAME send --fee-rate 1 VAULTADDRESS XXsats``` and put how many sats you have, can check with ```wallet balance```.
4. Come up or generate rune names. They should be unique, get as many as you like. I used this prompt in chatgpt ```come up with 50 1-4 word combinations, all caps with no spaces between. each combination should be 10-25 letters long. Put it as an array called "runeNames" in json file```. Rune names should be unique so you can specify some niche topic in your prompt so yours are really unique. Put your array of rune names into rune_names.json.
5. Configure ```ordPath``` on the 7th line of rune-farming.py to your directory.
6. Run rune-farming.py, it will run until your vault is empty or there are no more rune names.
7. After the script is done there is a checker that shows you which wallets didn't etch a rune, you can etch them by hand.
8. Create a copy of wallets.json and put it somethere safe.

In general, etching a rune is 10200 sats and transering is 400, so to do 100 wallets you'll need 1100000 sats or 0.011 sbtc

Goof luck farming!
