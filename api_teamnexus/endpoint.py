import yaml
from pathlib import Path

class Endpoint:
    ROOT = str(Path(__file__).parent.parent)
    with open(ROOT + "/docs/config.yml", "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)

    endpoint = cfg["api_teamnexus"]["endpoint"]
    TokenApi = cfg["api_teamnexus"]["token"]
    BL_endpoint = cfg["api_teamnexus"]["blacklist"]["endpoint"]
    BL_User = cfg["api_teamnexus"]["blacklist"]["user"]
    BL_Password = cfg["api_teamnexus"]["blacklist"]["password"]
    api_url = endpoint+"{action}"+"?token={token_api}".format(token_api=TokenApi)
    
    BOOKING = api_url.format(action="booking.php")
    GET_ASIN_BY_CODE = api_url.format(action="getasinbycode.php")
    INSERT_ORDER = api_url.format(action="insertorder.php")
    INSERT_REVIEW = api_url.format(action="insertreview.php")
    CHECK_REFUND = api_url.format(action="checkrimborso.php")
    DELETE_BOOKING = api_url.format(action="deletebooking.php")
    GET_PRODUCTS = api_url.format(action="getproducts.php")
    UPLOAD_SCREEN = api_url.format(action="uploadscreen.php")
    CHECK_BLACKLIST = "{BL_endpoint}?username={user}&password={password}&action=checkblacklist".format(BL_endpoint=BL_endpoint, user=BL_User, password=BL_Password)