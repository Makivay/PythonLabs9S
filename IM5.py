from matplotlib import pyplot as plt

import numpy
import numpy.random as random

# Вариант: 5
# Равномерный
# Эрланговский 6 порядка
# 5

# Интенсивность потока обработки
K = 6
miu = 5

receivedRequestTimes = []
doneRequestTimes = []

averageTimes = []


def value_by_erlang_distribution_k(rate):
    l = 1 / (rate * K)
    return sum(random.exponential([l], K))


def value_by_uniform_distribution(rate):
    # by design
    return random.exponential(1 / rate)
    # return random.exp(1 / rate - 0.05 * miu, 1 / rate + 0.05 * miu)


def new_request_time(system_time, rate):
    request_time = system_time + value_by_uniform_distribution(rate)
    receivedRequestTimes.append(request_time)
    return request_time


def new_free_time(system_time):
    free_time = system_time + value_by_erlang_distribution_k(miu)
    doneRequestTimes.append(free_time)
    return free_time


# Интенсивность входного потока
inputRates = [a / 10 * miu for a in range(1, 10)]


for inputRate in inputRates:
    bufferSize = 0
    received = 0
    done = 0
    systemTime = 0
    loadedFlag = False
    requestTime = 0
    freeTime = 0

    # Вермя новой заявки
    requestTime = new_request_time(requestTime, inputRate)
    freeTime = requestTime

    while done < 1_000_0:
        if requestTime <= freeTime:
            # Мы заняты
            systemTime = requestTime
            received += 1
            if not loadedFlag:
                loadedFlag = True
                freeTime = new_free_time(systemTime)
            else:
                bufferSize += 1
            requestTime = new_request_time(systemTime, inputRate)
        else:
            # Мы свободны
            systemTime = freeTime
            done += 1
            if bufferSize > 0:
                bufferSize -= 1
                freeTime = new_free_time(systemTime)
            else:
                loadedFlag = False
                freeTime = requestTime
    i = min(len(receivedRequestTimes), len(doneRequestTimes))
    deltaTimes = [doneRequestTimes[a] - receivedRequestTimes[a] for a in range(i)]
    averageTimes.append(sum(deltaTimes) / len(deltaTimes))
    receivedRequestTimes.clear()
    doneRequestTimes.clear()


def calcTeorT():
    averageTimes = []
    for inputRate in inputRates:
        #
        p = inputRate / miu
        # коэфициент вариации
        v = 1 / numpy.sqrt(K)
        # Среднее число запросов в системе
        L = (p ** 2 * (1 + v ** 2)) / (2 * (1 - p)) + p
        # Среднее время прабывания
        T = L / inputRate
        averageTimes.append(T)
    return averageTimes


plt.plot(inputRates, averageTimes, label='Практичесское', lw=4, color='black', alpha=0.5)
plt.plot(inputRates, calcTeorT(), label='Теоритичесское', lw=4, color='red', alpha=0.5)
plt.xlabel('Инт. входного потока')
plt.ylabel('Ср. t в системе')
plt.grid()
plt.legend()
plt.show()
