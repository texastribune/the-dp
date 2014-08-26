import json
import logging


class JSONFileHandler(logging.FileHandler):
    """
    logging file handler that throws away the message and dump json instead

    You can't do this using a formatter. Looks for json attribute, make sure
    it's passed in as an `extra` kwarg.

    """

    def emit(self, record):
        data = record.json
        data['timestamp'] = int(record.created)  # time.time() in seconds
        record.msg = json.dumps(data)
        super(JSONFileHandler, self).emit(record)
