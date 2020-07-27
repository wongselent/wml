from typing import Any, Dict, Callable

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


class FuncWorker(QtCore.QRunnable):
    def __init__(self, *funcs: Callable[[Any], Any]) -> None:
        super(FuncWorker, self).__init__()
        self.__funcs = funcs
        self.setAutoDelete(True)

    @QtCore.pyqtSlot()
    def run(self) -> None:
        for func in self.__funcs:
            result: Callable = None
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
    def __init__(self, parent: QtWidgets.QWidget = None, max_thread_count: int = 1) -> None:
        super(ThreadPool, self).__init__(parent)
        self.__parent: QtWidgets.QWidget = parent
        self.__max_thread_count: int = max_thread_count

        self.setMaxThreadCount(self.__max_thread_count)
        # self.setStackSize(1)
        self.setExpiryTimeout(5000)

    def run_functions(self, *funcs) -> None:
        worker = FuncWorker(*funcs)
        self.start(worker)
