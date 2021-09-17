# Copyright (C) 2021-present University of Louisiana at Lafayette.
# All rights reserved. Licensed under the GPLv3 License. See LICENSE.txt in the project root for license information.

class Entity:
    @classmethod
    def generate_fq_id(cls, short_id: str) -> str:
        """
        Generate a fully qualified `Internet of Water <https://internetofwater.org>`_/geoconnex ID for an
        entity from a short_id
        :param short_id: Short ID for an entity
        :return:
        """
        raise NotImplementedError
