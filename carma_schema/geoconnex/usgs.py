# Copyright (C) 2021-present University of Louisiana at Lafayette.
# All rights reserved. Licensed under the GPLv3 License. See LICENSE.txt in the project root for license information.

from urllib.parse import urlparse

from carma_schema.geoconnex import Entity


class HydrologicUnit(Entity):
    @classmethod
    def generate_fq_id(cls, short_id: str) -> str:
        """
        Generate Internet of Water hydrologic unit IDs.
        `Example IDs <https://github.com/internetofwater/geoconnex.us/tree/master/namespaces/usgs>`_
        :param short_id: Short ID in the form of a HUC code, e.g. 07070005.
        :return: Fully qualified hydrologic unit ID, e.g. https://geoconnex.us/usgs/hydrologic-unit/07070005
        """
        return f"https://geoconnex.us/usgs/hydrologic-unit/{short_id}"

    @classmethod
    def parse_fq_id(cls, fq_id: str) -> str:
        short_id = urlparse(fq_id).path.split('/')[-1]
        return short_id
