"""
bffl

A framework for bit fields

Copyright 2020-2024, Ken Seehart
MIT License
https://github.com/kenseehart/bffl
"""


import unittest
from typing import Union, Any, Callable, Sequence, Iterator, Type, Dict, NewType, Generic, TypeVar, Tuple, List, Optional, get_type_hints
from pprint import pprint as std_pprint
import json
import re
from random import randint, seed, choice
from warnings import warn
# pyright: reportInvalidTypeForm=false

from bffl.expressions import CSTNode, cst_expr, cst_source_code, cst_uint, is_identifier
from bffl.numduck import IntDuck, NumDuck

_all_above_excluded = set(locals().keys())

# everything defined below this will be exported to the bffl package unless startswith('_')

r_hex = re.compile(r'^\s*(?:0x|0X)?([0-9a-fA-F]+)(?:[Uu]?[Ll]{1,2}|H|h)?\s*$')
r_bin = re.compile(r'^\s*(?:0b|0B)?([01]+)(?:[Uu]?[Ll]{1,2})?\s*$')

def enum(a: Union[list, str]) -> dict:
    '''return an enum_ dict given an iterable'''
    return {c:i for i, c in enumerate(a)}

def isiter(obj) -> bool:
    '''return `True` if obj is a non-string iterable'''
    return hasattr(obj, '__iter__') and not isinstance(obj, str)


def pprint(v):
    '''
    pretty print customized for bffl usage

    dictionaries keep original order (not sorted)
    bound fields are converted to value
    '''

    if isinstance(v, field):
        v = v.v_

    std_pprint(v, sort_dicts=False)


def field_method(f):
    '''decorator that exposes a metaclass method to an instance of the class'''
    f._is_field_method = True
    return f


class unbound_field(type):
    '''Unbound field implementing propery protocol'''
    btype_: 'btype'
    v_: Any

    def __init__(self, name, bases, dict_):
        super().__init__(name, bases, dict_)
        for k, f in type(self).__dict__.items():
            if getattr(f, '_is_field_method', False):
                setattr(self, k, f)


    def __repr__(self):
        return f'<unbound_field: {self.__name__}>'

    def __bool__(self):
        return True

    @property
    def desc_(self):
        '''description string'''
        return f'{type(self.btype_).__name__} {self.__name__}'

    def __get__(self, instance, owner):
        if instance is None: # unbound field
            return self
        return self(instance) # return the binding of this field to the target

    def __set__(self, instance, value):
        self(instance).v_ = value

    def __getitem__(self, k):
        if isinstance(k, int):
            try:
                return getattr(self, f'_{k}')
            except AttributeError as e:
                if self.btype_.dim_ is not None:
                    raise IndexError(f'{self.desc_} index {k} out of range') from e
                raise TypeError(f'{self.desc_} is not subscriptable') from e

        elif isinstance(k, slice):
            if self.btype_.dim_ is not None:
                fname = f'{k.start}_{k.stop}_{k.step}'
                try:
                    return getattr(self, fname)
                except AttributeError:
                    ft = bslice(self.btype_, k)
                    f = ft.allocate_(f'{self.__name__}.{fname}', self)
                    setattr(self, fname, f)
                    return f
            else:
                raise TypeError(f'{self.desc_} is not subscriptable')
        else:
            try:
                return getattr(self, k)
            except AttributeError as e:
                raise KeyError(f'{self.__name__}:undefined subfield {k}') from e


    def __iter__(self):
        if self.btype_.dim_ is None:
            raise TypeError(f'{self.desc_} is not iterable')

        for i in range(self.btype_.dim_):
            yield self[i]

    def __len__(self):
        if self.btype_.dim_ is None:
            raise TypeError(f'{self.desc_} has no len()')

        return self.btype_.dim_


    @property
    def this_(self):
        'self reference field'
        return self

    @field_method
    def cst_(self, expr: str = '', word_size: int = 0) -> CSTNode:
        '''Return a CSTNode for this field, or an expression
        '''
        if expr == '':
            return cst_uint(self.offset_, self.mask_, word_size)
        else:
            def resolver(s: str, word_size=word_size) -> CSTNode:
                return self[s].cst_('', word_size)

            return cst_expr(expr, resolver, word_size)


    @field_method
    def expr_(self, expr: str = '', word_size: int = 0) -> str:
        'return low-level source code string for this field'
        return cst_source_code(self.cst_(expr, word_size))

    @field_method
    def expr_field_(self, expr: str, word_size: int = 0) -> str:
        ''''return a field that implements the specified expression with this field as the namespace
        Security Warning: do not use unless the source of expr is trusted
        '''

        cst = self.cst_(expr, word_size)
        src = cst_source_code(cst)
        d = {}

        # possibly insecure:
        exec('def fn(n: int):\n    return '+src, d, d) # pylint: disable=exec-used

        fnf = fn_type(d['fn'], src).allocate_('<expr>', self)
        fnf.expr_ = lambda *a: src

        return fnf


class field(IntDuck, metaclass=unbound_field):
    '''Bound field'''
    offset_: int
    mask_: int
    name_: str

    def __init__(self, target_field: 'field' = None):
        '''bind a field to a target list consisting of a single integer'''
        if target_field is not None:
            self.target_ = target_field.target_
        else:
            self.target_ = [0]

    def __repr__(self):
        return f'<{repr(self.v_)}>'

    @property
    def n_(self) -> int:
        '''return the raw unsigned integer value'''
        return (self.target_[0] >> self.offset_) & self.mask_

    @n_.setter
    def n_(self, n: int):
        '''set the raw integer value (signed or unsigned)'''
        self.target_[0] = (self.target_[0] & ~(self.mask_ << self.offset_) | ((n&self.mask_) << self.offset_))

    @property
    def v_(self) -> Any:
        '''return value (int|str|list|dict), virtual: overload mixin_field_ to express as a different type (default=int)'''
        return int(self)

    @v_.setter
    def v_(self, n: Any):
        '''set value (int, str, list, or dict), virtual: overload mixin_field_ to receive other data types (default=int)'''
        self.n_ = n

    @property
    def bin_(self) -> str:
        '''return binary string representation (0 padded to correct length, no prefix)'''
        return ('0'*self.size_ + bin(self.n_)[2:])[-self.size_:]

    @bin_.setter
    def bin_(self, s: str):
        '''set binary string, ignore the usual prefixes and suffixes, truncate overflow'''
        m = r_bin.fullmatch(s)
        if m:
            self.n_ = int(m.group(1), 2)
        else:
            raise ValueError(f'Expected binary string, got "{s}"')

    @property
    def hex_(self) -> str:
        '''return hex string representation (0 padded to correct length, no prefix)'''
        hsize = (self.size_+3)//4
        return ('0'*hsize + hex(self.n_)[2:])[-hsize:]

    @hex_.setter
    def hex_(self, s: str):
        '''set hex string, ignore the usual prefixes and suffixes, truncate overflow'''
        m = r_hex.fullmatch(s)
        if m:
            self.n_ = int(m.group(1), 16)
        else:
            raise ValueError(f'Expected hex string, got "{s}"')

    @property
    def json_(self):
        '''return json string representation'''
        return json.dumps(self.v_)

    @json_.setter
    def json_(self, s):
        '''set json string'''
        self.v_ = json.loads(s)

    def __bool__(self):
        return self.n_ != 0

    def __len__(self):
        return self.btype_.dim_

    # comparison
    def __eq__(self, other): # pylint: disable=too-many-return-statements
        if isinstance(other, int):
            return int(self) == other

        if isinstance(other, str):
            return str(self) == other

        if isiter(other):
            if len(self) == len(other):
                for sv, ov in zip(self, other):
                    if sv != ov:
                        return False
                else:
                    return True
            else:
                return False

        if isinstance(other, field):
            return self.n_ == other.n_

        return self.v_ == other

    def __int__(self): # may be overloaded (e.g. sint support for negatives)
        return self.n_

    def __str__(self):
        return str(self.v_)

    def __setitem__(self, k, v):
        if isinstance(k, int):
            k = f'_{k}' # array elements as field property instances

        setattr(self, k, v)

    def __setattr__(self, k, v):
        if k[0]=='_' or k[-1]=='_' or hasattr(self, k):
            super().__setattr__(k, v)
        else:
            msg = f'{type(self)} does not have attribute {k}'
            if hasattr(self, k+'_'):
                msg += ': did you mean {k}_ ?'
            raise AttributeError(msg)

    def __getattr__(self, k):
        try:
            return getattr(self.btype_, k)
        except AttributeError as e:
            raise AttributeError(f"'{self.name_}' field has no attribute '{k}'") from e

class btype(type) :
    '''Base class for field metatypes'''
    repr_: str
    size_: int
    dim_: int = None

    def __new__(cls, *args, name='', **kwargs):
        args, kwargs
        self = super().__new__(cls, name, (), {})
        self.name_ = name
        return self

    def __call__(self, value:int=0) -> field:
        'Create a new bound interface from this btype'
        ufield = self.allocate_(self.name_)
        f = ufield()
        f.v_ = value
        return f

    def allocate_(self, name:str, parent:unbound_field=None, offset:int=0) -> field:
        'allocate a unbound_field of this btype, into the specified parent if specified, else allocate as the interface root'

        if type(self) is btype:
            raise TypeError('btype is a virtual class and can not be allocated')

        ufield = unbound_field(name or self.repr_, (type(self).mixin_field_,), {}) #pylint: disable=no-member
        ufield.parent_ = parent
        ufield.root_ = parent.root_ if parent else ufield
        ufield.size_ = self.size_
        ufield.mask_ = ((1<<self.size_)-1)
        ufield.offset_ = offset
        ufield.btype_ = self
        return ufield

    def __repr__(self):
        return self.repr_

    def __getitem__(self, n):
        return array(self, n)

class uint(btype):
    '''unsigned integer with optional enum'''

    def __init__(self, size:int, enum_:dict=None, name=None):
        super().__init__(name)

        if not isinstance(size, int) or size<=0:
            raise ValueError(f'Expected positive integer size, got {size}')

        self.size_ = size
        self.repr_ = f"{type(self).__name__}[{size}]"
        self.enum_ = enum_ or {}
        self.renum_ = {v:k for k,v in self.enum_.items()}


    @classmethod
    def __class_getitem__(cls, *args):
        if len(args) == 1 and isinstance(args[0], tuple):
            args = args[0]

        # if the last argument is a dict, it is an enum
        if isinstance(args[-1], dict):
            enum_ = args[-1]
            args = args[:-1]
        else:
            enum_ = None

        # Create the base uint instance
        result = cls(args[-1], enum_)

        # Apply dimensions in reverse order
        for dim in reversed(args[:-1]):
            result = result[dim]

        return result

    class mixin_field_(field):
        '''inherited by bound field instance'''
        @property
        def v_(self) -> Union[int, str]:
            v = int(self)
            try:
                v = self.btype_.renum_[v] # defaults to raw int if enum is not defined
            except KeyError:
                pass
            return v

        @v_.setter
        def v_(self, v:Union[int, str]):

            if isinstance(v, str):
                try:
                    v = self.btype_.enum_[v]
                except KeyError:
                    try:
                        v = int(v)
                    except ValueError:
                        raise ValueError(f'{self}: undefined enum {v}')

            self.n_ = v

class svreg(uint):
    '''uint with system verilog slice semantics'''

    class mixin_field_(field):
        '''inherited by bound field instance'''

        def __getitem__(self, k:slice):
            'return a bound field using SV slice semantics'
            if not(isinstance(k, slice)):
                return super().__getitem__(k)

            sz = 1 + k.start - k.stop
            offset = self.size_ - k.start - 1
            bt:btype = type(self.btype_)(sz)
            uf = bt.allocate_(f'{self.name_}[{k.start}:{k.stop}]', self, offset)
            f = uf(self)
            return f

        def __setitem__(self, k:slice, v:Any):
            'set subfield value using SV slice semantics'
            f = self.__getitem__(k)
            f.v_ = v


class sint(uint):
    '''signed integer with optional enum'''

    class mixin_field_(uint.mixin_field_):
        '''inherited by bound field instance'''
        def __int__(self):
            v = self.n_
            if v&(1<<(self.size_-1)):
                v = v - (1<<(self.size_))
            return v

class fixed(sint):
    '''fixed point encoded as signed integer with const divisor

    A divisor is sufficient to generalize fixed point.
    For clarity, we specify precision and base, where divisor = base**precision

    size = total number of bits
    precision = number of fractional digits
    base = base of digits
    '''

    def __init__(self, size:int, precision: int, base:int, name=None):
        super().__init__(size, name)
        self.precision_ = precision
        self.base_ = base
        self.divisor_ = base**precision
        self.size_ = size
        self.max_ = ((1<<size)-1)/self.divisor_
        self.min_ = -self.max_

    class mixin_field_(NumDuck, sint.mixin_field_):
        '''inherited by bound field instance'''
        def __int__(self):
            return int(float(self))

        def __float__(self):
            v = self.n_
            if v&(1<<(self.size_-1)):
                v = v - (1<<(self.size_))
            return v/self.divisor_

        @property
        def v_(self) -> float:
            return float(self)

        @v_.setter
        def v_(self, v:float):
            try:
                if v<self.min_ or v>self.max_:
                    raise ValueError(f'{type(self).desc_}: value {v} out of range {self.min_} <= value <= {self.max_}')
            except TypeError as e:
                raise TypeError(f"{type(self).desc_} doesn't support assignment of {type(v)}")
            self.n_ = int(v*self.divisor_)



class decimal(fixed):
    '''fixed point decimal encoded as signed integer

    decimal(16, 2) = 16 bits, 2 decimal places (-655.35 <= v <= 655.36)
    decoded values (self.v_) are float
    '''

    def __init__(self, size:int, precision:int, name=None):
        super().__init__(size, precision, 10, name=name)
        self.repr_ = f"decimal({size}, {precision})"


class struct(btype):
    def __init__(self, *args):
        match args:
            case (type() as klass,):
                # Decorator usage
                name = klass.__name__
                annotations = getattr(klass, '__annotations__', {})
                self.fields_ = [(key, value) for key, value in annotations.items()]

            case (str() as name, list() as fields):
                # Regular instantiation with fields
                self.fields_ = fields

            case _:
                raise ValueError(f'{type(self).__name__} requires a name and fields list')

        self.name_ = name
        self.size_ = sum(ft.size_ for _, ft in self.fields_)
        self.repr_ = f"{type(self).__name__}('{self.name_}', {self.fields_})"

    def allocate_(self, name:str='_root', parent:unbound_field=None, offset:int=0) -> unbound_field:
        '''allocate a field recursively'''
        ftype = super().allocate_(name, parent, offset)
        z = offset

        for fname, ft in reversed(self.fields_):
            if fname.endswith('_'):
                raise ValueError(f'Field names must not end with _: {fname}')

            setattr(ftype, fname, ft.allocate_(f'{name}.{fname}', ftype, z))
            z += ft.size_

        return ftype

    @property
    def classdef_(self):
        'return class definition source code for this btype'
        lines = ['@struct', f'class {self.name_}:']
        for name, typ in self.fields_:
            lines.append(f'    {name}: {typ.name_ or typ.repr_}')

        return '\n'.join(lines)+'\n\n'


    class mixin_field_(field):
        '''inherited by bound field instance'''
        @property
        def v_(self) -> dict:
            d = {}
            for k, _ in self.btype_.fields_:
                d[k] = getattr(self, k).v_
            return d

        @v_.setter
        def v_(self, v:Union[int, dict]):
            if isinstance(v, dict):
                for k, fv in v.items():
                    setattr(self, k, fv)
            else:
                self.n_ = v

        def __iter__(self):
            for k, t in self.btype_.fields_:
                yield k

        def __getitem__(self, k):
            if isinstance(k, str):
                try:
                    return getattr(self, k)
                except AttributeError as e:
                    if is_identifier(k):
                        raise KeyError(f'{type(self)} does not have field "{k}"') from e

                f=self.expr_field_(k)(self)
                return f
            else:
                raise TypeError(f'{k.btype_.__name__} fields do not support {type(k).__name__} indices')



class array(struct):
    '''array'''

    def __init__(self, etype: btype, dim:int, name:str=None):
        self.etype_ = etype
        self.dim_ = dim
        self.size_ = etype.size_*dim
        self.repr_ = f"{etype.name_ or etype.repr_}[{dim}]"
        self.fields_ = tuple((f'_{i}',  etype) for i in range(dim))
        self.name_ = name

    class mixin_field_(struct.mixin_field_):
        '''inherited by bound field instance'''
        @property
        def v_(self) -> list:
            return [self[i].v_ for i in range(self.btype_.dim_)]

        @v_.setter
        def v_(self, v:Union[int, list, tuple]):
            if isinstance(v, int):
                self.n_ = v
            elif isiter(v):
                for i, fv in enumerate(v):
                    setattr(self, f'_{i}', fv)
            else:
                raise TypeError('assignment to array must be int or iterable')

        def __getitem__(self, k):
            if isinstance(k, int):
                try:
                    k = f'_{k}' # array elements as field property instances
                    return getattr(self, k)
                except AttributeError as e:
                    raise IndexError(f'array index {k[1:]} out of range') from e
            elif(isinstance(k, slice)):
                ftype = type(self)[k]
                return ftype(self)
            else:
                return super().__getitem__(k)

        def __iter__(self):
            for f in iter(type(self)):
                yield f(self)


class bslice(array):
    '''array slice'''

    def __init__(self, atype: array, aslice: slice): #pylint: disable=super-init-not-called
        self.atype_ = atype
        self.etype_ = atype.etype_
        self.slice_ = aslice
        self.islice_ = list(range(*aslice.indices(atype.dim_)))
        self.dim_ = len(self.islice_)
        self.size_ = self.etype_.size_*self.dim_
        self.repr_ = f"{atype}[{aslice}]"
        self.name_ = type(self).__name__

    def allocate_(self, name:str, parent:unbound_field, offset:int=0) -> unbound_field:
        '''allocate a field recursively'''
        ftype = btype.allocate_(self, name, parent, offset)

        for i,j in enumerate(self.islice_):
            setattr(ftype, f'_{i}', parent[j])

        return ftype


class utf8(array):
    '''unicode utf8 string, optionally null terminated'''
    # TODO: Low hanging performance fruit, if anyone needs this to be fast

    def __init__(self, length:int, nult:bool=True, name_:str = None):
        super().__init__(uint(8), length)
        self.repr_ = f"utf8({length})"
        self.nult_ = nult

    class mixin_field_(array.mixin_field_):
        '''inherited by bound field instance'''
        @property
        def v_(self) -> str:
            b = bytes(self[i] for i in range(self.dim_))
            if self.nult_:
                n = b.find(0)
                if n>-1:
                    b = b[:n]
            return b.decode('utf8')

        @v_.setter
        def v_(self, v:str):
            if isinstance(v, int):
                self.n_ = v
            else:
                if isinstance(v, str):
                    s = v.encode('utf8')
                elif isinstance(v, bytes):
                    s = v
                else:
                    raise TypeError(f'Expected str|bytes|int, got {v}')

                s = (s + b'\0'*self.dim_)[:self.dim_] # null pad to length

                for i, c in enumerate(s):
                    self[i] = c


class fn_type(btype):
    def __init__(self, fn: Callable[[int], Any], expr: str):
        self.fn_ = fn
        self.size_ = 0
        self.repr_ = f"fn_type({fn})"
        self.name_ = type(self).__name__


    class mixin_field_(field):
        @property
        def v_(self) -> Any:
            return self.fn_(self.target_[0])

        @property
        def n_(self) -> int:
            return int(self.v_)



__all__ = list(set([x for x in locals().keys() if not x.startswith('_')]) - _all_above_excluded)
