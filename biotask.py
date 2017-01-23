import sys


class Feature:
    def __init__(self, species, feature_name, value):
        self.species = species
        self.featureName = feature_name
        self.value = value

# Подзадача 1. Чтение из файла.
with open('spec_dt.txt') as readFile:
    print("Please wait...")
    print("Reading...")
    featuresArray = []  # массив, в котором хранятся все признаки
    next(readFile)  # пропускаем первую строку(заголовок таблицы)
    for line in readFile:
        try:
            fileLine = line.strip().split('\t')
            # загоняем созданные объекты признаков в массив
            featuresArray.append(Feature(fileLine[0], fileLine[1], fileLine[2]))
        except Exception:
            continue
amountOfFeatures = len(featuresArray)  # количество признаков в таблице
# если таблица пуста, выполнение программы прерывается, выбрасывая исключение со статусом "Таблица пуста."
if amountOfFeatures == 0:
    sys.exit("Таблица пуста.")

# Подзадача 2. Сортировка массива по названию вида.
#  В итоге получим отсортированный массив, где сначала идут все признаки первого вида,
#  потом все признаки второго и т.д.
print("Sorting...")
featuresArray.sort(key=lambda x: x.species)

# Подзадача 3. Сортировка внутри блоков признаков(объединенных общим названием вида).
# Последовательно спускаясь сверху вниз по таблице и сранивая значения поля "Вид", определяем границы блоков.
# Как только понимаем, что блок окончен(другое значение поля "Вид"), сортируем этот блок,
# начиная с позиции начала блока до текущего номера строки.

currentLineNum = 0  # текущая позиция
startBlockLineNum = currentLineNum  # позиция начала блока, который сейчас сортируется
blockName = featuresArray[startBlockLineNum].species  # имя вида в блоке, который сейчас сортируется
while True:
    if currentLineNum == amountOfFeatures:  # если true - здесь окончание последнего блока
        featuresArray[startBlockLineNum:currentLineNum] = sorted(featuresArray[startBlockLineNum:currentLineNum],
                                                                 key=lambda x: float(x.value), reverse=True)
        break 
    currentLineName = featuresArray[currentLineNum].species
    if blockName != currentLineName:  # если true - здесь начинается новый блок
        # ниже происходит сортировка только что завершившегося блока
        featuresArray[startBlockLineNum:currentLineNum] = sorted(featuresArray[startBlockLineNum:currentLineNum],
                                                                 key=lambda x: float(x.value), reverse=True)
        blockName = currentLineName  # имя вида в новом блоке
        startBlockLineNum = currentLineNum  # номер строки - начала нового блока
    currentLineNum += 1

# Подзадача 4. Запись в файл.
# Последовательно спускаясь сверху вниз по таблице, пишем в файл значения признаков в отсортированном порядке.
# В конец строки добавляем, каждый раз увеличивающееся на единицу значение rank(добавляем rank в таблицу динамически,
# а не сохраняем их в объекты класса Feature, чтобы не тратить лишнюю память на хранение).
# Как только понимаем, что начинается блок с новым значением "Вид" присваиваем rank значение 1 и повторяем
# вышеописанные действия до конца нового блока. Повторяем это до конца массива.

with open('sorted_spec_dt.txt', 'w') as writeFile:
    print("Writing...")
    currentLineNum = 0
    rank = 1
    writeFile.write('species' + '\t' + 'feature' + '\t' + 'value' + '\t' + 'rank' + '\n')
    while currentLineNum < amountOfFeatures:
        currentLineName = featuresArray[currentLineNum].species
        if blockName != currentLineName:
            blockName = currentLineName
            rank = 1
        writeFile.write(featuresArray[currentLineNum].species+'\t'+featuresArray[currentLineNum].featureName+'\t'
                        + featuresArray[currentLineNum].value + '\t' + str(rank) + '\n')
        rank += 1
        currentLineNum += 1
print('Your file is successfully done.')