#!/usr/bin/env python

# dumb simple active record like stuff.

import sqlite3


# PARSE_DECLTYPES

#typing place holder.



class PropertyMeta(type):
  def __new__(cls, name, bases, dct):
    klass = type.__new__(cls, name, bases, dct)
    return klass

  def __init__(cls, name, bases, dct):
    super(PropertyMeta, cls).__init__(name, bases, dct)
    def adapter(self): 
      return self.to_sqlite()
    sqlite3.register_adapter(name, adapter)


class PropertyBase(object):
  __metaclass__ = PropertyMeta
  def __init__(self, p):
    self.table, self.col = p
  @classmethod
  def python_type(cls):
    return None
  @classmethod
  def sqlite_type(cls):
    return "NULL"
  def to_sqlite(self):
    return None


class KeyCol(PropertyBase):
  @classmethod
  def python_type(cls):
    return int
  @classmethod
  def sqlite_type(cls):
    return "INTEGER"
  def to_sqlite(self):
    return None


class StringCol(PropertyBase):
  @classmethod
  def python_type(cls):
    return str
  @classmethod
  def sqlite_type(cls):
    return "TEXT"
  def to_sqlite(self):
    return None

  
class ReferenceCol(PropertyBase):
  def __init__(self, p, source):
    PropertyBase.__init__(self, p)
    self.src_table, self.src_col = source
  @classmethod
  def python_type(cls):
    return int
  @classmethod
  def sqlite_type(cls):
    return "INTEGER"
  def to_sqlite(self):
    return None

def write(*objs, conn):
  for o in objs:
    o.save(conn)



class MappingMeta(type):
  def __new__(cls, name, bases, dct):
    klass = type.__new__(cls, name, bases, dct)
    def init(self, *args, **kws):
      print 'init', cls, name
      for key, prop in dct.items():
        if isinstance(prop, PropertyBase):
          if key in kws:
            print key, prop, 'with', kws[key]
            self.__dict__[key] = prop.python_type()(kws[key])
    klass.__init__ = init
    return klass

  def __init__(cls, name, bases, dct):
    super(MappingMeta, cls).__init__(name, bases, dct)
    sqlite3.register_converter(name, cls)


class Mapping:
  __metaclass__ = MappingMeta
  def save(self, connection):
    c = connection.cursor()
    for key, prop in self.__class__.__dict__.items():
      if isinstance(prop, PropertyBase):
        c.execute("insert into %s(%s) values (?)"%(prop.table, prop.col),
                  (getattr(self, key),))
  def load(self, connection):
    pass

class WebSite(Mapping):
  key = KeyCol(('website', 'id'))
  name = StringCol(('website', 'name'))

class Domain(Mapping):
  key = KeyCol(('domain','id'))
  domain = StringCol(('domain', 'name'))
  website = ReferenceCol(('domain', 'website'), ('website', 'id'))

class URL(Mapping):
  key = KeyCol(('url', 'id'))
  url = StringCol(('url', 'data'))
  domain = ReferenceCol(('url', 'domain'), ('domain', 'id'))

#conn = sqlite3.connect(os.path.join(dir, site['name']))

if __name__ == "__main__":
    conn = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
    cur = conn.cursor()
    cur.execute("create table website(id INTEGER, name TEXT)")
    w = WebSite(key=1, name="hoge")
    w.save(conn)
    cur.execute("select name from website")
    obj = cur.fetchone()[0]
    print obj
    print type(obj)

    '''
    cur.execute("create table domain(X Domain)")
    cur.execute("insert into domain(X) values (?)", (Domain("hoge"),))
    cur.execute("select X from domain")
    obj = cur.fetchone()[0]
    print obj
    print type(obj)

    cur.execute("create table url(X URL)")
    cur.execute("insert into url(X) values (?)", (URL("hoge"),))
    cur.execute("select X from url")
    obj = cur.fetchone()[0]
    print obj
    print type(obj)
    '''
    cur.close()
    conn.close()


