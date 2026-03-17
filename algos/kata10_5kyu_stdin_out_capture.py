# old-fashioned argument parsing https://www.codewars.com/kata/67fbe9b877ff79c2f311d440
import sys, io

def unfool(fun):
    """Inserts args into sys.stdin, resets pointer to start of stream,
    runs the function and captures the output as the last line, returning it."""
    def wrapper(*args):
        old_stdin = sys.stdin
        old_stdout = sys.stdout
        capture = io.StringIO()
        sys.stdin = sys.stdout = capture
        capture.write('\n'.join(map(str, args)) + '\n') # inputs
        capture.seek(0)
        
        try:
            fun() # run base function
            res = capture.getvalue().strip() # last line is the output
            capture.close()
            res = res.split('\n')
            return int(res.pop())
        finally: # runs even if there is a return before it!
            sys.stdin = old_stdin
            sys.stdout = old_stdout
    return wrapper

@unfool
def example_fun():
    n = int(input())
    if n == 0:
        print(42)
    elif n == 1:
        print(2, file=sys.stdout)
    else:
        sys.stdout.write("7")

assert 42 == example_fun(0)
assert 2 == example_fun(1)
assert 7 == example_fun(2)
