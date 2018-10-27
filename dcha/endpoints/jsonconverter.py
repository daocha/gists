# Json serialization
# Date: 23 Jul 2018
# Author: Ray LI

import datetime
from flask.json import JSONEncoder

class JSONEncoderCustom(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, datetime.datetime):
                if obj.utcoffset() is not None:
                    obj = obj - obj.utcoffset()
                return obj.isoformat().__str__()
            elif isinstance(obj, datetime.date):
                return obj.isoformat().__str__()
            else:
                return obj.__dict__
        except TypeError:
            pass
        else:
            iterable = iter(obj)
            return list(iterable)
        return JSONEncoder.default(self, obj)
