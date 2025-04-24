# original snippet is from https://knazarov.com/posts/purity_delimited_continuations_and_io/


# Creates a specific IO operation and yields it, to
# be catched by the outside IO loop
def IO(io_type, *params):
    res = yield {"io_type": io_type, "params": params}
    return res

def count(x, n=None):
    if n is None:
        # If "n" is not specified, read if from stdin
        n = yield from IO("read")
        n = int(n)

    if (x <= n):
        yield from IO("print", x)
        yield from count(x+1, n)

computation = count(0)

while True:
    try:
        io = next(computation)
    except StopIteration:
        break

    # Pick a specific IO action to execute
    if io["io_type"] == "print":
        print(io["params"][0])
    elif io["io_type"] == "read":
        computation.send(input("Specify n:"))
