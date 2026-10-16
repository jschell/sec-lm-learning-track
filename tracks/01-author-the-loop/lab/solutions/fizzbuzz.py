def fizzbuzz(n):
    values = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            values.append("FizzBuzz")
        elif i % 3 == 0:
            values.append("Fizz")
        elif i % 5 == 0:
            values.append("Buzz")
        else:
            values.append(str(i))
    return values
