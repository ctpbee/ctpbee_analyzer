from functools import wraps
import time
import sys
import psutil
import os


class HowMany:
    def __init__(self):
        self.cost_queue = {}
        self.enable_count = 0
        self._original_trace_function = None

    def trace_memory(self, frame, event, arg):
        if event == 'return':
            p = psutil.Process(os.getpid())
            self.cost_queue['memory'] = p.memory_info()[0] / _TWO_20
        if self._original_trace_function is not None:
            self._original_trace_function(frame, event, arg)
        return self.trace_memory

    def __call__(self, func):
        self.cost_queue['name'] = func.__name__
        f = self.wrap_function(func)
        f.__module__ = func.__module__
        f.__name__ = func.__name__
        f.__doc__ = func.__doc__
        f.__dict__.update(getattr(func, '__dict__', {}))
        return f

    def wrap_function(self, func):
        def f(*args, **kwds):
            self.enable_by_count()
            try:
                return func(*args, **kwds)
            finally:
                self.disable_by_count()

        return f

    def enable(self):
        self._original_trace_function = sys.gettrace()
        sys.settrace(self.trace_memory)

    def disable(self):
        sys.settrace(self._original_trace_function)

    def enable_by_count(self):
        """ Enable the profiler if it hasn't been enabled before.
        """
        if self.enable_count == 0:
            self.enable()
        self.enable_count += 1

    def disable_by_count(self):
        """ Disable the profiler if the number of disable requests matches the
        number of enable requests.
        """
        if self.enable_count > 0:
            self.enable_count -= 1
            if self.enable_count == 0:
                self.disable()


template = '{0:<15} {1:<15} {2:<15} {3:<15}'
temp_time = '{:.3f} ms'
temp_cpu = '{} %'
temp_memory = '{:.3f} MB'
_TWO_20 = float(2 ** 20)

header = template.format('Function', 'Spend', 'CPU', 'Memory')


def show(h, time, cpu):
    stream = sys.stdout
    stream.write(header + '\n')
    stream.write(u'=' * len(header) + '\n')
    result = template.format(h.cost_queue['name'],
                             temp_time.format(time),
                             temp_cpu.format(cpu),
                             temp_memory.format(h.cost_queue['memory'])
                             )
    stream.write('\r' + result + '\n')


def cost(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        h = HowMany()
        p = psutil.Process(os.getpid())
        start_time = time.time()
        start_cpu = p.cpu_percent()
        val = h(func)(*args, **kwargs)
        end_time = time.time()
        end_cpu = p.cpu_percent()
        show(h, end_time - start_time, end_cpu - start_cpu)
        return val

    return wrap
