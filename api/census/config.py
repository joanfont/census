import decouple


class Config:

    @property
    def DEBUG(self):
        return decouple.config('DEBUG', default=False, cast=bool)

config = Config()
