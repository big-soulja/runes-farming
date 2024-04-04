import random
# create a batch file to create runes
# also create an SVG with the rune name

def createBatch(i, words):
    
    fname = 'r1b.yaml'
    rdiv = random.randint(0,5)
    rsup = random.randint(1,50)*1000000 + 1
    rmine = 1
    w1 = words[i*3]
    w2 = words[i*3+1]
    w3 = words[i*3+2]
    rsym = w1[0] # first letter of first word
    Nr = 1000
    rcap = int((rsup-1)/Nr)
    # fpath = '/home/monkey/'

    svgname = 'r1.svg'
    cback = 'black'
    ctext = 'red'
    cdot = '.'
    rname = w1 + cdot + w2 + cdot + w3


    with open(fname, 'w') as file:
        # Write some text to the file
        file.write('mode: separate-outputs\n')
        file.write('\n')
        file.write('# rune to etch\n')
        file.write('etching:\n')
        file.write('  # rune name\n')
        file.write(f'  rune: {rname}\n')
        file.write('  # allow subdividing super-unit into `10^divisibility` sub-units\n')
        file.write(f'  divisibility: {rdiv}\n')
        file.write('  # premine\n')
        file.write(f'  premine: {rmine}\n')
        file.write('  # total supply, must be equal to `premine + terms.cap * terms.amount`\n')
        file.write(f'  supply: {rsup}\n')
        file.write('  # currency symbol\n')
        file.write(f'  symbol: {rsym}\n')
        file.write('  # mint terms\n')
        file.write('  terms:\n')
        file.write('    # amount per mint\n')
        file.write(f'    amount: {Nr}\n')
        file.write('    # maximum number of mints\n')
        file.write(f'    cap: {rcap}\n')
        file.write('\n')
        file.write('inscriptions:\n')
        file.write('  # path\n')
        file.write(f'  - file: {fname}\n')


    # write the svg file
    with open(svgname, 'w') as file:
        # Write some text to the file
        file.write('<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">\n')
        file.write(f'  <rect width="100%" height="100%" fill="{cback}"></rect>\n')
        file.write(f'  <g font-family="Arial" font-size="20" fill="{ctext}">\n')
        file.write(f'    <text x="10" y="30">{w1}</text>\n')
        file.write(f'    <text x="10" y="60">{w2}</text>\n')
        file.write(f'    <text x="10" y="90">{w3}</text>\n')
        file.write(f'  </g>\n')
        file.write(f'</svg>\n')

