import time


def log_calls(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        res = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time

        if args and kwargs:
            args_str = ", ".join(map(str, args)) + ", " + ", ".join(f"{k}={v}" for k, v in kwargs.items())
        elif args:
            args_str = ", ".join(map(str, args))
        elif kwargs:
            args_str = ", ".join(f"{k}={v}" for k, v in kwargs.items())
        else:
            args_str = ""

        print(f"[LOG] {func.__name__}(args=({args_str})) -> {res} за {execution_time:.6f} сек")

        return res
    return wrapper


@log_calls
def calc_delivery(distance_km, weight_kg, is_express):
    cost = 100 + (20 * distance_km) + (15 * weight_kg)
    if is_express:
        cost *= 1.5

    return cost

calc_delivery(5, 2, False)
calc_delivery(12, 5, True)
calc_delivery(3, 1, False)