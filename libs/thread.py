from typing import Any, Dict, Union, Callable

from PyQt5 import QtCore, QtWidgets


class THREAD_STATE:
    start = 0
    running = 1
    finish = 2
    error = 3

    __str: Dict[int, str] = {
        start: "start",
        running: "running..",
        finish: "finished",
        error: "error!"
    }

    @classmethod
    def str(cls, value: int) -> str:
        return cls.__str[value]

# class FuncWorker(QtCore.QRunnable):
#     def __init__(self, func: Union, *args: Tuple[Any], **kwargs: Dict[Any, Any]) -> None:
#         super(FuncWorker, self).__init__()
#         self.__func = func
#         self.__args = args
#         self.__kwargs = kwargs

#         self.setAutoDelete(True)

#     @QtCore.pyqtSlot()
#     def run(self) -> None:
#         self.__func(*self.__args, **self.__kwargs)

# def run_in_thread(*func) -> Callable[[Any], Any]:
#
#     def _run_in_thread(fn) -> None:
#         print(func, fn)
#
#     return _run_in_thread


class FuncWorker(QtCore.QRunnable):
    def __init__(self, *funcs: Callable[[Any], Any]) -> None:
        super(FuncWorker, self).__init__()
        self.__funcs = funcs

        self.setAutoDelete(True)

    @QtCore.pyqtSlot()
    def run(self) -> Any:
        for func in self.__funcs:
            result: Callable[[Any], Any] = None
            try:
                result = func()
            except Exception as ex:
                print(ex)
                pass
            else:
                pass
            finally:
                if result:
                    print(result)


class ThreadPool(QtCore.QThreadPool):
    def __init__(self, parent: QtWidgets.QWidget = None, max_thread_count: int = 1, **kwargs: Dict[Any, Any]) -> None:
        super(ThreadPool, self).__init__(parent)
        self.__parent: QtWidgets.QWidget = parent
        self.__max_thread_count: int = max_thread_count
        self.__kwargs: Dict[Any, Any] = kwargs

        self.setMaxThreadCount(self.__max_thread_count)
        self.setExpiryTimeout(10)

    def run_functions(self, *funcs) -> None:
        worker = FuncWorker(*funcs)
        self.start(worker)
