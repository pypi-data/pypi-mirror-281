from abc import ABC
from functools import wraps
from inspect import signature

from http.client import HTTPConnection as ClientHTTPConnection
from requests import Request
from starlette.requests import HTTPConnection as StarlletteHTTPConnection

from dependency_needle.constants import ANNOTATIONS, RETURN
from dependency_needle.lifetime_enums import LifeTimeEnums
from dependency_needle.dependency_strategy import (
    IDependencyStrategyInterface,
    ScopedDependencyStrategy,
    TransientDependencyStrategy,
    SingeltonDependencyStrategy
)


class Container:
    """Container used to build a class by automating the dependancy injection
    to obtain inversion of control"""

    request_class_types = [
        Request,
        StarlletteHTTPConnection,
        ClientHTTPConnection
    ]

    def __init__(self):
        self.__interface_registery_lookup = {}
        self.__singleton_lookup = {}
        self.__transient_lookup = {}
        self.__lifetime_meta_lookup = {
            LifeTimeEnums.SINGLETON: self.__singleton_lookup,
            LifeTimeEnums.TRANSIENT: self.__transient_lookup,
            # Un-Used dictionary
            LifeTimeEnums.SCOPED: {}
        }
        self.__lifetime_strategy_lookup = {
            LifeTimeEnums.SINGLETON: SingeltonDependencyStrategy,
            LifeTimeEnums.TRANSIENT: TransientDependencyStrategy,
            # Un-Used dictionary
            LifeTimeEnums.SCOPED: ScopedDependencyStrategy
        }

    def __gaurd_build_unregistered_interface(self, interface: ABC):
        """Throw 'KeyError' exception if interface is not registered."""
        if interface not in self.__interface_registery_lookup:
            raise KeyError(f"Interface: {interface} is not registered.")

    def __assert_implementation(self, interface: ABC, concrete_class) -> None:
        """Assert that the concrete class implements the interface
        being registered.

        :param interface: interface needed to be registered.
        :param concrete_class: concrete class implementing the interface.
        :return: None
        """
        if interface not in concrete_class.__bases__:
            raise TypeError(f"Concrete class: {concrete_class}"
                            f" has to implement interface: {interface}.")

    def __assert_abstract_class(self, interface: ABC) -> None:
        """Assert that the interface being registered is an abstract class.

        :param interface: interface needed to be registered.
        :return: None
        """
        if ABC not in interface.__bases__:
            raise TypeError(f"Interface: {interface}"
                            f" has to be an abstract class.")

    def __assert_proper_enum_used(self, enum: LifeTimeEnums) -> None:
        """Assert that the enum being passed is valid.

        :param enum: enum used to register dependency.
        :return: None
        """
        if enum not in LifeTimeEnums.__members__.values():
            raise KeyError(f"Enum: {enum} does not exist in 'LifeTimeEnums'.")

    def register_interface(self, interface: ABC,
                           concrete_class,
                           life_time: LifeTimeEnums) -> None:
        """Register interface with a corresponding concrete class to use.

        :param interface: interface needed to be registered.
        :param concrete_class: concrete class implementing the interface.
        :param life_time: life time enum specifying the lifetime of the class.
        :return: None
        """
        self.__assert_abstract_class(interface)
        self.__assert_implementation(interface, concrete_class)
        self.__assert_proper_enum_used(life_time)
        strategy: IDependencyStrategyInterface = (
            self.__lifetime_strategy_lookup[life_time]
        )

        lookup = self.__lifetime_meta_lookup[life_time]
        self.__interface_registery_lookup[interface] = strategy(
            lookup, interface, concrete_class)

    def build(self, interface: ABC, key_lookup) -> object:
        """Build an interface by utilizing the registery lookup.

        :param interface: interface needed to be built
        :param key_lookup: key_lookup that might be used to lookup\
        registered interfaces.
        :return object: concrete class that implemenets that interface
        """
        self.__gaurd_build_unregistered_interface(interface)
        interface_to_build: IDependencyStrategyInterface = (
            self.__interface_registery_lookup[interface]
        )
        return interface_to_build.build(self.__interface_registery_lookup,
                                        key_lookup)

    def clear(self, key_lookup):
        """Clear created dependencies for specific key

        :param key_lookup: immutable key to delete from\
        transient lookup.
        """
        if key_lookup in self.__transient_lookup:
            del self.__transient_lookup[key_lookup]

    def build_dependencies_decorator(self, fn):
        """Wrap a given function to build its dependencies\
        if they are registered.

        :param fn: function with request/identifier as its\
        first parameter or an annotated parameter of type "Request".
        :return: wrapped function.
        """
        @wraps(fn)
        def wrapper(*args, **kwargs):

            if hasattr(fn, ANNOTATIONS):
                dependencies: dict = getattr(
                    fn,
                    ANNOTATIONS
                )

                # Get request from annotations if it exists.
                request_kwarg_key = ''

                for key, class_type in dependencies.items():
                    if any([
                        issubclass(class_type, request_type)
                        for request_type in Container.request_class_types
                        if key != RETURN
                    ]):
                        request_kwarg_key = key

                built_dependencies = {}

                if request_kwarg_key:
                    request_or_identifier = kwargs.pop(request_kwarg_key)
                    # Assign request to kwargs as it'll be passed as a kwarg
                    # if its annotated.
                    built_dependencies[request_kwarg_key] = (
                        request_or_identifier
                    )
                else:
                    try:
                        request_or_identifier = args[0]
                    except IndexError:
                        raise IndexError(
                            "Request parameter doesn't exist as an annotated"
                            " parameter or first parameter."
                        )

                for key, interface in dependencies.items():
                    try:
                        if key != RETURN:
                            built_dependencies[key] = self.build(
                                interface, request_or_identifier
                            )
                    except (KeyError, TypeError):
                        continue

                kwargs.update(built_dependencies)

            result = fn(*args, **kwargs)
            self.clear(request_or_identifier)

            return result

        func_signature = signature(wrapper)

        wrapper_signature = func_signature.replace(
            parameters=[
                parameter for parameter in func_signature.parameters.values()
                if parameter.annotation
                not in self.__interface_registery_lookup
            ]
        )

        wrapper.__signature__ = wrapper_signature

        return wrapper
