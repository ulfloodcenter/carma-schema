
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
