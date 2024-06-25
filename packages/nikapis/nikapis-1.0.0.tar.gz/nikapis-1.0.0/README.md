<p align="center">
    <a href="https://t.me/NikAPIsChannel">
        <img src="https://www.taxpayeradvocate.irs.gov/wp-content/uploads/2023/04/Crypto.png" alt="NikAPIs" width="128">
    </a>
    <br>
    <b>A library with different capabilities for you</b>
    <br>
    <a href="https://t.me/NikAPIsChannel">
        telegram channel
    </a>
    •
    <a href="https://t.me/YeStalker">
        admin
    </a>
    •
    <a href="https://NikAPis.site">
        web
    </a>
</p>

## Nik APIs

> A library with features that your bot and sites need, for example Crypto

``` python
from nikapis import Apis

nik = Apis('@nikapischannel')

# information of Notcoin (NOT)
notcoin = nik.notcoin

# the JSON result
print(notcoin)
```

**Crypto** In the code above, which is related to the digital currency section, you can get the price in dollars or tomans, and you can also get the currency change percentage in the last 24 hours.
### Support

If you need to contact support, use the following ways:

- [Go to Telegram Account](https://t.me/YeStalker).
- [Go to Telegram Group](https://t.me/RoleAi).
- nikpy.dev@gmail.com

### Documentation / Methods

- **crypto** notcoin/toncoin/tether/bnb/solana/dogecoin/tron/polygon/ethereum/bitcoin
- - **coin name**: nik.notcoin['name']
- - **coin symbol**: nik.notcoin['symbol']
- - **usa price**: nik.notcoin['price']
- - **percent change**: nik.notcoin['change']
- - **iran price**: nik.notcoin['toman']
- - **toman change**: nik.notcoin['ir_change']

### Installing

``` bash
pip install requests
pip install nikapis
```

### next update

- Hamster Kombat
- other new crypto
