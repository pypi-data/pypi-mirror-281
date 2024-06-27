### Background

This tool was created to help decrypt certain fields from RealPage's API. 
There are some specific bits of code that will only work for their specific encryption settings. 
Feel free to implement additional more generic methods and submit pull requests. We have noticed
there will occasionally be HTML escaped characters returned from their API 
so we unescape it in the example just to be safe.


### Installation
```pip install capicom```

### Usage

```py
import html

from Crypto.Cipher import DES3

from capicom.decrypt import Capicom3DESCipher


encryption_key = 'your encryption password'
encrypted_field = html.unescape('encrypted string')
decrypted_field = Capicom3DESCipher.decrypt_3des_realpage(encrypted_field, encryption_key)
print(decrypted_field)
```
