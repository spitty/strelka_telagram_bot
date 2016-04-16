#!/usr/bin/python

import logging
import shelve

logger = logging.getLogger(__name__)

class Storer:
    def __init__(self, filename):
        self.filename = filename

    def store(self, key, obj):
        db = shelve.open(self.filename)
        db[key] = obj
        db.close()

    def restore(self, key):
        db = shelve.open(self.filename)
        if db.has_key(key):
            obj = db[key]
            logger.info("Successful load data by key '%s' info from file %s" % (key, self.filename))
        else:
            obj = None
            logger.info("Can't get data by key '%s' info from file %s" % (key, self.filename))
        db.close()
        return obj