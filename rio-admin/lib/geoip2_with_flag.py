import flag
import geoip2.database

# Path to the GeoLite2-City.mmdb file
DATABASE_PATH = "GeoLite2-City.mmdb"


def get_country_from_ip(ip_address) -> tuple[str, str, str] | None:
    """
    Get the country and flag for an IP address using GeoIP2.
    Returns a tuple with country, city, and flag.
    """
    try:
        with geoip2.database.Reader(DATABASE_PATH) as reader:
            response = reader.city(ip_address)
            return (
                response.country.names["en"],
                response.city.names["en"],
                flag.flag(response.country.iso_code),
            )
    except:
        return None
