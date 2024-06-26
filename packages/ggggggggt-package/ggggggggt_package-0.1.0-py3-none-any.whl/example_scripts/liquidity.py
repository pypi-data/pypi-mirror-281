from utils import get_env_json
from gemnify_sdk.scripts.gemnify import Gemnify
from gemnify_sdk.scripts.config import Config
from gemnify_sdk.scripts.utils import expand_number

env_json = get_env_json()

config = Config("arbitrum-sepolia")
config.set_rpc(env_json['url'])
config.set_private_key(env_json['private_key'])

gemify = Gemnify(config)
liquidity = gemify.liquidity()

liquidity.add_liquidity(
    "0x254b40Ce47F7DA1867e594613D08a23E198d7FE7",
    expand_number(11.1, 18),
    0,
    0
)

liquidity.remove_liquidity(
    expand_number(0.8, 18),
    0,
    "0xcd665A9ED5e75961649a73e26b13A869F0c45200"
)