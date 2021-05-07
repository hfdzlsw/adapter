"""
模块工具类

@author sven
@create 2021-05-07
"""
import inspect
import six
from importlib import import_module
from pkgutil import iter_modules


def walk_modules(path):
    """
    Loads a module and all its submodules from the given module path and
    returns them. If *any* module throws an exception while importing, that
    exception is thrown back.
    """
    mods = []
    mod = import_module(path)
    mods.append(mod)
    if hasattr(mod, '__path__'):
        for _, subpath, ispkg in iter_modules(mod.__path__):
            fullpath = path + '.' + subpath
            if ispkg:
                mods += walk_modules(fullpath)
            else:
                submod = import_module(fullpath)
                mods.append(submod)
    return mods


def iter_classes(module, attr_name, base_class):
    for obj in six.itervalues(vars(module)):
        if inspect.isclass(obj) and \
           issubclass(obj, base_class) and \
           obj.__module__ == module.__name__ and \
           getattr(obj, attr_name, None):
            yield obj


def load_classes(mappings, module, attr_name, base_class):
    for cls in iter_classes(module, attr_name, base_class):
        mappings[getattr(cls, attr_name)] = cls


def load_all_classes(module_root_path, attr_name, base_class):
    """
    加载指定目录下所有继承类

    :param module_root_path: 类的顶层路径（列表）
    :param attr_name: 属性名
    :param base_class: 父类
    :return: 字典，{属性名：子类}
    """
    mappings = {}
    for name in module_root_path:
        try:
            for module in walk_modules(name):
                load_classes(mappings, module, attr_name, base_class)
        except ImportError as e:
            print(e)
    return mappings

