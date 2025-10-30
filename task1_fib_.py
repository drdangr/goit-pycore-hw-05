def caching_fibonacci():
    # inside function cache
    cache = {}
    
    def fibonacci(n):
        # base cases
        if n <= 0:
            return 0
        if n == 1:
            return 1
        
        # if already in cache, return it
        if n in cache:
            
            # debug print
            # print(f"   - Retrieving from cache: fib({n}) = {cache[n]}")
            
            return cache[n]
        
        # recursive calculation with caching
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        
        #debug print
        #print(f"Calculating and caching: fib({n}) = {cache[n]}")
        
        return cache[n]
    
    # return the inner function
    return fibonacci

# example usage
fib = caching_fibonacci()
print(fib(10))  # 55
print(fib(15))  # 610

# check caching by calling again
print(fib(10))  # may retrieve from cache
