from abc import ABC, abstractmethod

from dependency_needle.container import Container
from dependency_needle.lifetime_enums import LifeTimeEnums


def main():
    class MockInterfaceOne(ABC):
        """Mock interface class."""
        @abstractmethod
        def mock_method(self):
            """Mock interface method."""
            pass

    class MockInterfaceTwo(ABC):
        """Mock interface class."""

        @abstractmethod
        def mock_method(self):
            """Mock interface method."""
            pass

    class MockInterfaceThree(ABC):
        """Mock interface class."""

        @abstractmethod
        def mock_method(self):
            """Mock interface method."""
            pass

    class ConcreteOne(MockInterfaceOne):
        def mock_method(self):
            pass

    class ConcreteTwo(MockInterfaceTwo):
        def __init__(self, dependency_one: MockInterfaceOne):
            pass

        def mock_method(self):
            pass

    class ConcreteThree(MockInterfaceThree):
        def __init__(self, dependency_one: MockInterfaceOne,
                     dependency_two: MockInterfaceTwo):
            pass

        def mock_method(self):
            pass

    container = Container()

    container.register_interface(
        MockInterfaceOne, ConcreteOne, LifeTimeEnums.SINGLETON)
    container.register_interface(
        MockInterfaceTwo, ConcreteTwo, LifeTimeEnums.SINGLETON)
    container.register_interface(
        MockInterfaceThree, ConcreteThree, LifeTimeEnums.TRANSIENT)

    built_object = container.build(
        MockInterfaceThree, "REQUEST_OBJECT_OR_UNIQUE_KEY")

    return built_object


if __name__ == "__main__":
    main()
