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
  def __init__(self, col=None):
    self.col = col

  @classmethod
  def python_type(cls):
    return None
  @classmethod
  def sqlite_type(cls):
    return "NULL"
  @classmethod
  def to_sqlite(cls):
    return None
  @classmethod
  def to_python(cls, v):
    return cls.python_type()(v)


class KeyCol(PropertyBase):
  @classmethod
  def python_type(cls):
    return int
  @classmethod
  def sqlite_type(cls):
    return "INTEGER"


class StringCol(PropertyBase):
  @classmethod
  def python_type(cls):
    return str
  @classmethod
  def sqlite_type(cls):
    return "TEXT"

  
class ReferenceCol(PropertyBase):
  def __init__(self, source, *args, **kw):
    PropertyBase.__init__(self, *args, **kw)
    self.ref = source

  @classmethod
  def python_type(cls):
    #UGH!  Lazy bind this.
    return self.ref

  @classmethod
  def sqlite_type(cls):
    return "INTEGER"


def write(conn=None, *objs):
  for o in objs:
    o.save(conn)



class MappingMeta(type):
  def __new__(cls, name, bases, dct):
    return type.__new__(cls, name, bases, dct)

  def __init__(cls, name, bases, dct):
    super(MappingMeta, cls).__init__(name, bases, dct)
    sqlite3.register_converter(name, cls)


class Mapping:
  __metaclass__ = MappingMeta
  def __init__(self, *args, **kws):
    for key, prop in self.__class__.__dict__.items():
      if isinstance(prop, PropertyBase):
        if key in kws:
          print key, prop, 'with', kws[key]
          self.__dict__[key] = prop.python_type()(kws[key])

  @classmethod
  def table(cls):
    return cls.__name__

  @classmethod
  def columns(cls):
    return [(prop.col or key, prop.sqlite_type() ) for key, prop in cls.__dict__.items() if isinstance(prop, PropertyBase)]

  @classmethod
  def new_schema(cls, connection):
    c = connection.cursor()
    vs = ', '.join(['%s %s'%(k, t) for k, t in cls.columns()])
    q = "create table %s(%s)"%(cls.table(), vs)
    print q
    c.execute(q)

  def save(self, connection):
    c = connection.cursor()
    cs = self.columns()
    ks = ', '.join(['%s'%(k,) for k, t in cs])
    q = "insert into %s(%s) values (%s)"%(self.table(), ks, ', '.join('?'*len(cs)))
    print q
    c.execute(q, [getattr(self, k) for k, t in cs])

  @classmethod
  def load(cls, connection, key):
    c = connection.cursor()
    cs = cls.columns()
    ks = ', '.join(['%s'%(k,) for k, t in cs])
    q = "select %s from %s"%(ks, cls.table())
    print q
    c.execute(q)

    r = cls()
    for i, v in  enumerate(c.fetchone()):
      k, t = cs[i]
      p = getattr(cls, k)
      setattr(r, k, p.to_python(v))
    return r




class WebSite(Mapping):
  key = KeyCol()
  name = StringCol()

class Domain(Mapping):
  key = KeyCol()
  domain = StringCol()
  website = ReferenceCol(WebSite)

class URL(Mapping):
  key = KeyCol()
  url = StringCol()
  domain = ReferenceCol(Domain)

#conn = sqlite3.connect(os.path.join(dir, site['name']))

if __name__ == "__main__":
    print WebSite.table()
    print WebSite.columns()
    conn = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)

    WebSite.new_schema(conn)
    w = WebSite(key=1, name="hoge")
    w.save(conn)
    x = WebSite.load(conn, key=1)
    print x
    print x.key
    print x.name

    conn.close()


