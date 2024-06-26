from utils import get_env_json
from gemnify_sdk.scripts.gemnify import Gemnify
from gemnify_sdk.scripts.config import Config
from gemnify_sdk.scripts.utils import expand_number

env_json = get_env_json()

config = Config("arbitrum-sepolia")
config.set_rpc(env_json['url'])
config.set_private_key(env_json['private_key'])

gemify = Gemnify(config)
position = gemify.position()

position.create_increase_position(
    "0x254b40Ce47F7DA1867e594613D08a23E198d7FE7",
    expand_number(15, 18),
    expand_number(150, 30),
    True,
    expand_number(1.1, 30),
    expand_number(0.000215, 18),
    "0x0000000000000000000000000000000000000000",
    value = expand_number(0.000215, 18)
)

