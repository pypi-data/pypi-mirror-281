from pympipool.shared.executor import (
    execute_parallel_tasks,
    execute_separate_tasks,
    ExecutorBroker,
    ExecutorSteps,
)
from pympipool.shared.interface import BaseInterface
from pympipool.shared.thread import RaisingThread
from pympipool.shared.interface import MpiExecInterface


class InteractiveExecutor(ExecutorBroker):
    """
    The pympipool.interactive.executor.InteractiveExecutor leverages the pympipool interfaces to distribute python tasks
    on a workstation or inside a queuing system allocation. In contrast to the mpi4py.futures.MPIPoolExecutor the
    pympipool.interactive.executor.InteractiveExecutor can be executed in a serial python process and does not require
    the python script to be executed with MPI. Consequently, it is primarily an abstraction of its functionality to
    improves the usability in particular when used in combination with Jupyter notebooks.

    Args:
        max_workers (int): defines the number workers which can execute functions in parallel
        executor_kwargs (dict): keyword arguments for the executor
        interface_class (BaseInterface): interface class to initiate python processes

    Examples:

        >>> import numpy as np
        >>> from pympipool.interactive.executor import InteractiveExecutor
        >>>
        >>> def calc(i, j, k):
        >>>     from mpi4py import MPI
        >>>     size = MPI.COMM_WORLD.Get_size()
        >>>     rank = MPI.COMM_WORLD.Get_rank()
        >>>     return np.array([i, j, k]), size, rank
        >>>
        >>> def init_k():
        >>>     return {"k": 3}
        >>>
        >>> with InteractiveExecutor(max_workers=2, executor_kwargs={"init_function": init_k}) as p:
        >>>     fs = p.submit(calc, 2, j=4)
        >>>     print(fs.result())
        [(array([2, 4, 3]), 2, 0), (array([2, 4, 3]), 2, 1)]

    """

    def __init__(
        self,
        max_workers: int = 1,
        executor_kwargs: dict = {},
        interface_class: BaseInterface = MpiExecInterface,
    ):
        super().__init__()
        executor_kwargs["future_queue"] = self._future_queue
        executor_kwargs["interface_class"] = interface_class
        self._set_process(
            process=[
                RaisingThread(
                    target=execute_parallel_tasks,
                    kwargs=executor_kwargs,
                )
                for _ in range(max_workers)
            ],
        )


class InteractiveStepExecutor(ExecutorSteps):
    """
    The pympipool.interactive.executor.InteractiveStepExecutor leverages the pympipool interfaces to distribute python
    tasks. In contrast to the mpi4py.futures.MPIPoolExecutor the pympipool.interactive.executor.InteractiveStepExecutor
    can be executed in a serial python process and does not require the python script to be executed with MPI.
    Consequently, it is primarily an abstraction of its functionality to improve the usability in particular when used
    in combination with Jupyter notebooks.

    Args:
        max_cores (int): defines the number workers which can execute functions in parallel
        executor_kwargs (dict): keyword arguments for the executor
        interface_class (BaseInterface): interface class to initiate python processes

    Examples:

        >>> import numpy as np
        >>> from pympipool.interactive.executor import InteractiveStepExecutor
        >>>
        >>> def calc(i, j, k):
        >>>     from mpi4py import MPI
        >>>     size = MPI.COMM_WORLD.Get_size()
        >>>     rank = MPI.COMM_WORLD.Get_rank()
        >>>     return np.array([i, j, k]), size, rank
        >>>
        >>> with PyFluxStepExecutor(max_cores=2) as p:
        >>>     fs = p.submit(calc, 2, j=4, k=3, resource_dict={"cores": 2})
        >>>     print(fs.result())

        [(array([2, 4, 3]), 2, 0), (array([2, 4, 3]), 2, 1)]

    """

    def __init__(
        self,
        max_cores: int = 1,
        executor_kwargs: dict = {},
        interface_class: BaseInterface = MpiExecInterface,
    ):
        super().__init__()
        executor_kwargs["future_queue"] = self._future_queue
        executor_kwargs["interface_class"] = interface_class
        executor_kwargs["max_cores"] = max_cores
        self._set_process(
            RaisingThread(
                target=execute_separate_tasks,
                kwargs=executor_kwargs,
            )
        )
