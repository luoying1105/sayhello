#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/22 14:51
# @Author  : LUO YING
# @Site    : 
# @File    : _tools.py
# @Detail    :
import contextlib
import inspect
from datetime import date
from datetime import datetime
from typing import Iterable, Any

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from grpc_server.tool._setting import DB_URI

engine = create_engine(DB_URI, convert_unicode=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


@contextlib.contextmanager
def session_ctx(throw_ex=True):
    """
    Session上下文管理器
    :return: Session
    """
    # logging.debug("session_ctx open session")
    try:
        session = Session()
        yield session
    except Exception as e:
        tb = e.__traceback__
        if tb.tb_next is not None:
            tb = tb.tb_next
        es = "{}:{}:{}".format(tb.tb_frame.f_code.co_filename, e.__class__.__name__, tb.tb_lineno)
        # logging.warning("db context error %s %s", es, e)
        if throw_ex:
            raise e
    finally:
        if locals().get('session', None):
            # logging.debug('session_ctx close session')
            locals()['session'].close()


class Singleton(type):
    """
    单例工具metaclass
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class BaseHandler(metaclass=Singleton):
    def __init__(self):
        # self.logger = logging.getLogger(self.__class__.__name__)
        self.obj_converter = ObjConverter()


class ObjConverter(metaclass=Singleton):
    """
    将对象转换为dict
    """
    __reflect_cache__ = {}
    __support_types__ = (Base,)
    __time_format__ = '%Y-%m-%d %H:%M:%S'
    __date_format__ = '%Y-%m-%d'
    _instance = None

    def __init__(self, parse_func=None):
        """
        初始化
        :param  parse_func: callable
            转换字段时调用
        """
        if callable(parse_func):
            self.__execute__ = parse_func

    @classmethod
    def instance(cls):
        """
        获取单例实例
        :rtype: ObjConverter
        """
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def convert(self, obj: Base, exclude: Iterable = None, cache: bool = True) -> dict:
        """
        转换对象
        :param obj:
        :param exclude:
        :param cache:
        :return:dict
        """
        assert isinstance(obj, self.__support_types__), u'不支持的类型!'
        if type(obj) in self.__reflect_cache__:
            return self._convert_with_cache(obj, ex=set() if not exclude else set(exclude))
        r = {}

        def _ex_all(_):
            return False

        def _ex(x):
            return x in exclude

        ex = _ex if exclude else _ex_all
        # ex = lambda x: x in exclude if exclude else lambda _: False
        for key in obj.__dict__:
            if key.startswith('_') or ex(key):
                continue
            v = getattr(obj, key)
            r[key] = self.convert(v) if isinstance(v, self.__support_types__) else self.__execute__(v)
        if cache:
            self.__reflect_cache__[type(obj)] = r.keys()
        return r

    def convert_list(self, ol, exclude=None, cache=True) -> list:
        assert hasattr(ol, '__iter__'), 'TypeError: ol must be iterable'
        return [self.convert(o, exclude, cache) for o in ol]

    def _convert_with_cache(self, obj, ex: set = None):
        key_map = self.__reflect_cache__[type(obj)]
        return {key: self.__execute__(getattr(obj, key)) for key in key_map if key not in ex}

    def __execute__(self, v):
        """
        默认的转换函数
        :param v:
        :return:
        """
        if isinstance(v, self.__support_types__):
            return self.convert(v)
        if isinstance(v, (date, datetime)):
            return self.__time__convert__(v)
        return v

    def __time__convert__(self, v):
        """
        转换日期相关类型数据
        :param v:
        :return:
        """
        t = type(v)
        tc = {date: self.__date_format__, datetime: self.__time_format__}
        assert t in tc, 'not a date or datetime value'
        return v.strftime(tc[t])

    def register(self, ct, fields):
        """
        注册要转换的类型
        :param ct:
        :param fields:
        :return:
        """
        assert inspect.isclass(ct) and hasattr(fields, '__iter__'), 'type error'
        self.__reflect_cache__[ct] = tuple(fields)

    def fields_to_dict(self, obj, fields) -> dict:
        """
        将对象的指定字段转换为dict
        :param obj:
        :param fields:
        :return:
        """
        assert isinstance(fields, (list, tuple)), 'fields must be instance of tuple or list'
        return {field: self.__execute__(getattr(obj, field)) for field in fields if hasattr(obj, field)}

    @staticmethod
    def make_np_obj(src: dict, cls: type) -> Any:
        """
        生成namedtuple类对象
        :param src:
        :param cls:
        :return:
        """
        fields = getattr(cls, "_fields")
        params = {key: src.get(key) for key in fields}
        return cls(**params)

    def make_dict(self, keys, values) -> dict:
        return dict(zip(keys, map(self.__execute__, values)))

    def make_dict_list(self, keys, values) -> Iterable[dict]:
        return tuple(map(lambda row: self.make_dict(keys, row), values))
