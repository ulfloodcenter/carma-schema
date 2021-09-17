# Copyright (C) 2021-present University of Louisiana at Lafayette.
# All rights reserved. Licensed under the GPLv3 License. See LICENSE.txt in the project root for license information.

from urllib.parse import urlparse

from carma_schema.geoconnex import Entity


class ShortIDComponents:
    def __init__(self, state_fips, county_fips):
        self.state_fips = state_fips
        self.county_fips = county_fips

    def __str__(self):
        return f"{self.state_fips}{self.county_fips}"

    def __repr__(self):
        return f"ShortIDComponents {{ state_fips: {self.state_fips}, county_fips: {self.county_fips} }}"


class County(Entity):
    @classmethod
    def generate_fq_id(cls, short_id: str) -> str:
        """
        Generate Internet of Water county IDs.
        `Example IDs <https://github.com/internetofwater/geoconnex.us/tree/master/namespaces/ref/counties>`_
        :param short_id: Short ID in the form of a county FIPS code, e.g. 08031.
        :return: Fully qualified county ID, e.g. https://geoconnex.us/ref/counties/08031
        """
        return f"https://geoconnex.us/ref/counties/{short_id}"

    @classmethod
    def parse_fq_id(cls, fq_id: str) -> ShortIDComponents:
        short_id = urlparse(fq_id).path.split('/')[-1]
        return ShortIDComponents(state_fips=short_id[:2], county_fips=short_id[2:])

    @classmethod
    def get_short_id(cls, fq_id: str) -> str:
        return urlparse(fq_id).path.split('/')[-1]
