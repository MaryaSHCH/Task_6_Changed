import csv
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    '''Основываясь на формуле гаверсинуса функция вычисляет расстояние
    между двумя точками на земной поверхности, заданными их широтой и долготой.
    :param lon1(float): долгота первой точки в радианах.
    :param lat1(float): широта первой точки в радианах.
    :param lon2(float): долгота второй точки в радианах.
    :param lat2(float): широта второй точки в радианах.
    :return: расстояние между двумя точками в километрах (float).'''
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2]) # math.radians() – преобразует угол из градусов в радианы.
    # Формула гаверсинуса
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # радиус Земли в километрах
    return c * r # расстояние между двумя точками в километрах

def load_zipcode_database():
    ''' Функция читает файл, содержащий почтовые индексы, их географические координаты,
    а также соответствующие города и штаты. Каждая строка файла преобразуется в словарь,
    который затем добавляется в список, формируя таким образом базу данных в памяти.
    :return: list of dict - cписок словарей, где каждый словарь содержит информацию о почтовом индексе.'''

    with open(r'.\data\zip_codes_states.csv', mode='r') as infile:
    # with - файл будет закрыт после выхода из блока кода, даже если в процессе чтения возникнет ошибка.
    # open(...) - функция для открытия файла с указанием пути к файлу. mode='r' - файл открывается в режиме чтения.
        reader = csv.reader(infile)
    # cоздает объект reader, который позволяет итерировать по строкам CSV-файла.
        next(reader, None)  # пропускает заголовки.
    # None гарантирует, что если файл пуст, то next() не вызовет ошибку.

    # zipcode_database = {...} - Создание нового словаря zipcode_database.
    # {rows[0]: (rows[1], rows[2], rows[3], rows[4]) for rows in reader} -
    # генератор словаря, который итерируется по каждой строке в объекте reader.
    # rows[0] - первый элемент строки (zip_code) - ключ в словаре.
    # (rows[1], rows[2], rows[3], rows[4], rows[5]) - кортеж, содержащий остальные элементы строки:
    # "latitude","longitude","city","state","county".
    # for rows in reader - Цикл, который проходит через все строки в объекте reader.
        zipcode_database = {rows[0]: (rows[1], rows[2], rows[3], rows[4], rows[5]) for rows in reader}
    # return zipcode_database - Возвращает словарь zipcode_database после его заполнения.
    return zipcode_database
zipcode_database = load_zipcode_database()

def find_location_by_zip(zipcode):
    '''Функция находит местоположение по заданному почтовому индексу.
    :param: zipcode (str): почтовый индекс, для которого необходимо найти местоположение.
    :return: tuple: кортеж, содержащий город, штат, широту и долготу для заданного индекса.
    Возвращает None, если индекс не найден.'''

def find_location_by_zip(zipcode):
    if zipcode in zipcode_database:
        location_data = zipcode_database[zipcode]
        return f"ZIP Code {zipcode} is in {location_data[2]}, {location_data[3]}, {location_data[4]} county, coordinates: ({location_data[0]}°N,{location_data[1]}°W)."
    else:
        return "Zipcode not found."

def find_zip_by_city_and_state(city, state, zipcode_database):
    ''' Функция находит почтовый индекс по городу и штату.
    :param city (str): название города.
    :param state (str): название штата.
    :return: str: почтовый индекс, соответствующий указанному городу и штату.
    Если соответствие не найдено, возвращает сообщение об ошибке.'''

    zipcodes = []
    for zipcode, details in zipcode_database.items():
        if details[2].lower() == city.lower() and details[3].lower() == state.lower():
            zipcodes.append(zipcode)
    return zipcodes if zipcodes else "City or state not found."

def calculate_distance_by_zip(zipcode1, zipcode2, unit='km'):
    ''' Функция определяет расстояние между двумя точками, заданными их почтовыми индексами.
    :param zipcode1 (str): Почтовый индекс первой точки.
    :param zipcode2 (str): Почтовый индекс второй точки.
    :return: float: Расстояние между двумя точками.
    Если один или оба индекса не найдены, возвращает сообщение об ошибке.'''

    if zipcode1 in zipcode_database and zipcode2 in zipcode_database:
        lat1, lon1 = map(float, zipcode_database[zipcode1][:2])
        lat2, lon2 = map(float, zipcode_database[zipcode2][:2])
        distance = haversine(lon1, lat1, lon2, lat2)
        if unit == 'miles':
            return distance * 0.621371  # Перевод в мили
        return distance  # в км
    else:
        return f"The distance between {zipcode1} and {zipcode2} cannot be determined."

def main():
    # Функция main() - основная точка входа в программу.
    # Содержит цикл, который обрабатывает команды пользователя в режиме REPL.

    # Запуск бесконечного цикла до момента его прервания пользователем.
    while True:
        # Запрос у пользователя ввести одну из команд: 'loc', 'zip', 'dist', или 'end'.
        # Введеные символы преобразуются в нижний регистр с помощью .lower().
        command = input("Enter command ('loc', 'zip', 'dist', 'end'): ").lower()
        # Если команда 'end', то выводится сообщение "Done" и завершается цикл с помощью break.
        if command == 'end':
            print("Done")
            break

        elif command == 'loc':
            zipcode = input("Enter a ZIP Code to lookup: ")
            print(find_location_by_zip(zipcode))

        elif command == 'zip':
            city = input("Enter a city name to lookup: ")
            state = input("Enter a state name to lookup: ")
            zip_codes_found = find_zip_by_city_and_state(city, state, zipcode_database)
            print(f"The following ZIP Code(s) found for {city}, {state}: {', '.join(zip_codes_found)}")

        elif command == 'dist':
            zipcode1 = input("Enter the first ZIP Code: ")
            zipcode2 = input("Enter the second ZIP Code: ")
            unit = input("Choose the unit of measurement (km/miles): ")
            print(f"Distance between {zipcode1} and {zipcode2}: {calculate_distance_by_zip(zipcode1, zipcode2, unit)}")
    else:
            print(f"Invalid command, ignoring. ")

if __name__ == "__main__":
    main()

import zip_util

zip_codes = zip_util.read_zip_all()
print(zip_codes[0])
print(zip_codes[4108])

