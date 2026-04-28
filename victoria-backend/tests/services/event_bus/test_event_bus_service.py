from app.services.event_bus import EventBusService, Event
from unittest import mock


class MyEvent(Event):
    def __init__(self, a: int, b: int):
        self.a: int = a
        self.b: int = b


class MySubEvent(MyEvent):
    def __init__(self, a: int):
        self.a = a


class MyMegaEvent(Event):
    def __init__(self, msg: str):
        self.msg: str = msg


def test_event_bus_dispatches_to_one_subscriber():
    # Arrange
    serv = EventBusService()
    event = MyEvent(42, 67)
    test_method = mock.MagicMock()

    def handler(event: MyEvent):
        test_method(event.a, event.b)

    # Act
    serv.subscribe(MyEvent, handler)
    serv.publish(event)

    # Assert
    test_method.assert_called_once_with(42, 67)


def test_event_bus_dispatches_to_two_subscribers_of_same_event():
    # Arrange
    serv = EventBusService()
    event = MyEvent(42, 67)
    test_method1 = mock.MagicMock()
    test_method2 = mock.MagicMock()

    def handler1(event: MyEvent):
        test_method1(event.a, event.b)

    def handler2(event: MyEvent):
        test_method2(event.a, event.b)

    # Act
    serv.subscribe(MyEvent, handler1)
    serv.subscribe(MyEvent, handler2)
    serv.publish(event)

    # Assert
    test_method1.assert_called_once_with(42, 67)
    test_method2.assert_called_once_with(42, 67)


def test_event_bus_routes_to_multiple_subscribers_properly():
    # Arrange
    serv = EventBusService()
    event = MyEvent(42, 67)
    mega_event = MyMegaEvent("lol")

    test_method1 = mock.MagicMock()
    test_method2 = mock.MagicMock()
    test_method3 = mock.MagicMock()

    def handler1(event: MyEvent):
        test_method1(event.a, event.b)

    def handler2(event: MyEvent):
        test_method2(event.b, event.a)

    def handler3(event: MyMegaEvent):
        test_method3(event.msg)

    # Act
    serv.subscribe(MyEvent, handler1)
    serv.subscribe(MyEvent, handler2)
    serv.subscribe(MyMegaEvent, handler3)

    serv.publish(event)

    # Assert
    test_method1.assert_called_once_with(42, 67)
    test_method2.assert_called_once_with(67, 42)
    test_method3.assert_not_called()

    # Act
    serv.publish(mega_event)

    # Assert
    test_method1.assert_called_once_with(42, 67)
    test_method2.assert_called_once_with(67, 42)
    test_method3.assert_called_once_with("lol")


def test_event_bus_not_dispatches_to_not_yet_subscribed_handler():
    # Arrange
    serv = EventBusService()
    event = MyEvent(42, 67)
    mega_event = MyMegaEvent("lol")
    test_method1 = mock.MagicMock()
    test_method2 = mock.MagicMock()

    def handler1(event: MyEvent):
        test_method1(event.a, event.b)

    def _(event: MyMegaEvent):
        test_method2(event.msg)

    # Act
    serv.subscribe(MyEvent, handler1)

    serv.publish(event)
    serv.publish(mega_event)

    # Assert
    test_method1.assert_called_once_with(42, 67)
    test_method2.assert_not_called()


def test_event_bus_not_dispatches_to_supertype_event():
    # Arrange
    serv = EventBusService()
    sub_event = MySubEvent(20)

    super_method = mock.MagicMock()
    sub_method = mock.MagicMock()

    def super_handler(event: MyEvent):
        super_method(event.a, event.b)

    def sub_handler(event: MySubEvent):
        sub_method(event.a)

    # Act
    serv.subscribe(MyEvent, super_handler)
    serv.subscribe(MySubEvent, sub_handler)

    serv.publish(sub_event)

    # Assert
    super_method.assert_not_called()
    sub_method.assert_called_once_with(20)


def test_event_bus_not_dispatches_to_already_unsubscribed_handler():
    # Arrange
    serv = EventBusService()
    event = MyEvent(42, 67)

    test_method1 = mock.MagicMock()
    test_method2 = mock.MagicMock()

    def handler1(event: MyEvent):
        test_method1(event.a, event.b)

    def handler2(event: MyEvent):
        test_method2(event.b, event.a)

    # Act
    serv.subscribe(MyEvent, handler1)
    unsub_handle = serv.subscribe(MyEvent, handler2)

    serv.publish(event)

    # Assert
    assert test_method1.call_count == 1
    assert test_method2.call_count == 1

    # Act
    unsub_handle()
    serv.publish(event)

    # Assert
    assert test_method1.call_count == 2
    assert test_method2.call_count == 1
