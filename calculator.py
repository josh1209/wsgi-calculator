"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""

import re
import traceback

def main():
    body = ['<h1>The Calculator</h1>', '<ul>']
    body.append("<html>Here's how to use this page...</html>")
    body.append('<li>To add, use the "add" page, followed by the two numbers you want to add. Ex: /add/2/4 will yield "6".</li>')
    body.append('<li>For subtraction, use the "subtract" page. Ex: /subtract/10/5 will yield "5".</li>')
    body.append('<li>For multiplication, use the "multiply" page. Ex: /multiply/3/5 will yield "15".</li>')
    body.append('<li>For division, use the "divide" page. Ex: /divide/20/2 will yield "10".</li>')
    
    return '\n'.join(body)

def add(*args):
    """ Returns a STRING with the sum of the arguments """

    # TODO: Fill sum with the correct value, based on the
    # args provided.
    digit1, digit2 = args
    sum = int(digit1) + int(digit2)

    page = ['<h1>Summation</h1>']
    page.append(f'<html>{digit1} plus {digit2} equals {sum}')

    return '\n'.join(page)

# TODO: Add functions for handling more arithmetic operations.

def subtract(*args):
    """ Returns a STRING with the difference of the arguments """
    
    digit1, digit2 = args
    difference = int(digit1) - int(digit2)

    page = ['<h1>Subtraction</h1>']
    page.append(f'<html>{digit1} minus {digit2} equals {difference}')

    return '\n'.join(page)
    
def multiply(*args):
    """ Returns a STRING with the arguments multiplied together """
    
    digit1, digit2 = args
    multiplied = int(digit1) * int(digit2)

    page = ['<h1>Multiplication</h1>']
    page.append(f'<html>{digit1} times {digit2} equals {multiplied}')

    return '\n'.join(page)
    
def divide(*args):
    """ Returns a STRING with the arguments divided by each other """
    
    digit1, digit2 = args
    divided = int(digit1) / int(digit2)

    page = ['<h1>Division</h1>']
    page.append(f'<html>{digit1} divided by {digit2} equals {divided}')

    return '\n'.join(page)

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    
    funcs = {
        '': main,
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide
    }

    path = path.strip('/').split('/')
    
    func_name = path[0]
    args = path[1:]
    
    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

#    func = add
#    args = ['25', '32']

    return func, args

def application(environ, start_response):
    # TODO: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    #
    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = '200 OK'
    except NameError:
        status = '500 Internal Server Error'
        body = '<h1> Not Found</h1>'
    except ZeroDivisionError:
        status = '500 Internal Server Error'
        body = '<h1> Cannot Divide by Zero</h1>'
    except Exception:
        status = '500 Internal Server Error'
        body = '<h1> Internal Server Error</h1>'
        print(traceback.format_exc())
    finally:
        headers.append(("Content-length", str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    # TODO: Insert the same boilerplate wsgiref simple
    # server creation that you used in the book database.
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
