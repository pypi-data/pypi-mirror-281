from utils import get_env_json
from gemnify_sdk.scripts.gemnify import Gemnify
from gemnify_sdk.scripts.config import Config
from gemnify_sdk.scripts.utils import expand_number

env_json = get_env_json()

config = Config("arbitrum-sepolia")
config.set_rpc(env_json['url'])
config.set_private_key(env_json['private_key'])

gemify = Gemnify(config)
order = gemify.order()

order.create_increase_order(
    expand_number(10, 18),
    "0x254b40Ce47F7DA1867e594613D08a23E198d7FE7",
    expand_number(20, 30),
    "0x2f2F7Aa330Ef17019A9cB086da0970470fFe5a8c",
    True,
    expand_number(0.98, 30),
    False,
    expand_number(0.000215, 18),
    value = expand_number(0.000215, 18))

print(order.get_increase_order("0xcd665A9ED5e75961649a73e26b13A869F0c45200", 10))

