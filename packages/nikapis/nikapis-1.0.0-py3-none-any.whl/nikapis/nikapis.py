def crypto(name):
    import requests, json
    res = requests.get(f'https://NikAPIs.site/apis/crypto/?name={name}') # the our api crypto
    a, z = res.text.find('<pre>') + len('<pre>'), res.text.find('</pre>')
    all = json.loads(res.text[a:z].strip())['crypto']
    info = {
        'name': all['name'],
        'symbol': all['symbol'],
        'price': all['price'],
        'change': all['change'],
        'toman': all['toman'],
        'ir_change': all['ir_change']
    }

    return info

status = False # soon
class Apis:
    def __init__(self, key):
        self.key = key
        if str(self.key).lower() == '@nikapischannel': # the ad password, you can edit it ;)
            # notcoin
            self.notcoin = crypto('notcoin')
            # toncoin
            self.toncoin = crypto('toncoin')
            # tether
            self.tether = crypto('tether')
            # bnb
            self.bnb = crypto('bnb')
            # solana
            self.solana = crypto('solana')
            # dogecoin
            self.dogecoin = crypto('dogecoin')
            # tron
            self.tron = crypto('tron')
            # polygon
            self.polygon = crypto('polygon')
            # ethereum
            self.ethereum = crypto('ethereum')
            # bitcoin
            self.bitcoin = crypto('bitcoin')

        # the result is json
        

