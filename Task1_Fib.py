def caching_fibonacci():
    # пустой словарь для кэша
    cache = {}
    
    def fibonacci(n):
        # Базовые случаи
        if n <= 0:
            return 0
        if n == 1:
            return 1
        
        # Если уже в кэше - возвращаем его
        if n in cache:
            
            # debug print
            # print(f"   - Retrieving from cache: fib({n}) = {cache[n]}")
            
            return cache[n]
        
        # рекурсия и кэш
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        
        #debug print
        #print(f"Calculating and caching: fib({n}) = {cache[n]}")
        
        return cache[n]
    
    # Возвращаем внутреннюю функцию
    return fibonacci

# Пример использования:
fib = caching_fibonacci()
print(fib(10))  # 55
print(fib(15))  # 610

# Проверка кэша
print(fib(10))  # Должно извлечь из кэша, если раскоментировать debug print, будет видно
print(fib(14))  # Должно извлечь из кэша
print(fib(11))  # Должно извлечь из кэша