from matplotlib import pyplot as plt
import numpy as np
import numpy.random as rd

status = False  # True - Пауссоновский поток, False - Экспериментальный поток
# Условия варианта
shape = 3
mu0 = 2
# Инт. входного потока
lamb = np.linspace(0.1, 1, 10) * mu0
# Подсчет границ для равномер.
a = 1 / mu0 - 0.1 * mu0 / 2
b = a + 0.1 * mu0

if status:
    # Теор значения
    # Подсчет теор. значения коэффициента вариации обработки
    v = np.sqrt(((b - a) ** 2) / 12) / ((a + b) / 2)
    # Подсчет теор. значения коэффициента загрузки системы
    p = lamb[lamb != mu0] / mu0
    # Подсчет теор. значения среднего числа запросов в системе
    L = (p ** 2 * (1 + v ** 2)) / (2 * (1 - p)) + p
    # Подсчет теор. значения среднего времени пребывания запроса в системе
    tTheor = L / lamb[lamb != mu0]

# Массив для записи оценочных значений среднего времени пребывания запроса в системе
tAnal = np.array([])

# Проход по всем значениям интен. потока
for i in lamb:
    # Занятость ОУ и число запросов в очереди,число итераций
    busy = m = count = 0
    # Старое значение среднего времени пребывания запроса в системе
    tOld = 2 ** 32
    # значения времен прихода запроса,время обработки запроса,работы запроса
    dataRequest = np.array([])
    tRequest = rd.exponential(1 / i, 1) if status else rd.gamma(shape, 1 / (i * shape), 1)
    workT = np.array([])
    # Массив значений времен обработки запросов
    workData = np.array([])
    # Массив значений систм времени.
    systemT = np.array([])
    print(tRequest)
    while True:
        count += 1
        if tRequest <= workT:
            systemT = tRequest
            if not busy:
                # ОУ в положение занято
                busy = True
                # Генерация время обработки запроса
                workT = systemT + rd.uniform(a, b)
            else:
                # Увел. кол. заявок
                m += 1
            # Генерируем время прихода запроса, если ch = True, то генерируем для тестового потока
            tRequest = systemT + (rd.exponential(1 / i, 1) if status else rd.gamma(shape, 1 / (i * shape), 1))
            dataRequest = np.append(dataRequest, systemT)
        else:
            systemT = workT
            if m > 0:  # Если буфер не пустой
                m -= 1  # Забераем запрос из буфера
                workT = systemT + rd.uniform(a, b)  # Генерируем время обработки запроса
            else:
                busy = False  # Освобождаем ОУ
                workT = tRequest  # Время обслуживания = время прихода запроса
            workData = np.append(workData, systemT)
        # Оценка параметров каждые 1000 итераций
        if count % 1000 == 0:
            # Расчет оценки ср. времени
            tNew = np.mean(workData - dataRequest[:len(workData)])
            # tNew = np.mean(workData - dataRequest[:len(workData)])
            if (np.abs((tNew - tOld) / tOld)) > 0.01:
                # Сохранение нового значения оцениваемого параметра как старого
                tOld = tNew
            else:
                break
    # Сохранение оценки среднего времени пребывания запроса в системе
    tAnal = np.append(tAnal, tNew)

print(tAnal)
# Вывод графиков
if status:
    plt.plot(lamb[:len(tTheor)], tTheor, label='Теор.', lw=4, color='black', alpha=0.5)
    plt.plot(lamb[:9], tAnal[:9], label='Оценка', lw=4, color='red', alpha=0.5)
    plt.ylabel('Ср. t в системе')
    plt.xlabel('Инт. входного потока')
else:
    plt.plot(lamb[:9], tAnal[:9], lw=4, color='red', )
    plt.ylabel('Ср. t в системе')
    plt.xlabel('Инт. входного потока')
plt.grid()
plt.legend()
plt.show()
