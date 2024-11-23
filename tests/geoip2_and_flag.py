import flag
import geoip2.database

# Path to the GeoLite2-City.mmdb file
database_path = "../GeoLite2-City.mmdb"


def get_country_from_ip(ip_address):
    try:
        with geoip2.database.Reader(database_path) as reader:
            response = reader.city(ip_address)
            return {
                "country": response.country.names["en"],
                "city": response.city.names["en"],
                "flag": flag.flag(response.country.iso_code),
            }
    except Exception as e:
        return f"Error: {e}"


# Test with an IP address
ip = "170.171.1.9"  # Example IP (US, New York)
response = get_country_from_ip(ip)
print(f"The country for IP {ip} is: {response}")
