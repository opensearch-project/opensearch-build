import logging
import urllib.request
from typing import List


class DistributionNotFound(Exception):
    def __init__(self, urls: List[str]):
        self.urls = urls
        super().__init__(f"Unable to find a distribution under urls {self.urls}")


def find_build_root(base_url: str, platform: str, architecture: str, product_name: str) -> str:
    possible_urls = [
        f"{base_url}/{platform}/{architecture}/builds/{product_name}",
        f"{base_url}/{platform}/{architecture}/builds"
    ]

    for distribution_url in possible_urls:
        manifest_url = f"{distribution_url}/manifest.yml"
        try:
            with urllib.request.urlopen(manifest_url):
                # OK we could access the manifest, return the url
                return distribution_url
        except:
            logging.info(f"No build manifest found at {manifest_url}")
    raise DistributionNotFound(possible_urls)
