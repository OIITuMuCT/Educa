squares_odds = [x**2 for x in range(10) if x % 2 != 0]   # Фильтрация элементов иф в конце
squares_cubes = [(x**2 if x % 2 != 0 else x**3) for x in range(10)] # Выбор элемента иф в начале в
print(squares_odds)
print(squares_cubes)