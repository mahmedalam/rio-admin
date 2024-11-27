from tqdm import tqdm
import httpx


def download_large_file(url: str, destination: str, chunk_size: int = 1024 * 1024) -> None:
    try:
        with httpx.stream("GET", url) as response:
            response.raise_for_status()  # Ensure the request was successful
            total = int(response.headers.get("Content-Length", 0))

            with tqdm(total=total, unit="B", unit_scale=True, desc="Downloading") as pbar:
                with open(destination, "wb") as f:
                    for chunk in response.iter_bytes(chunk_size=chunk_size):
                        f.write(chunk)
                        pbar.update(len(chunk))

        print(f"\nDownload complete: {destination}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # Example Usage
    file_url = "https://xrc.freewebhostmost.com/GeoLite2-City.mmdb"
    destination = "./GeoLite2-City.mmdb"
    download_large_file(file_url, destination)
