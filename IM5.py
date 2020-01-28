import numpy.random as random

# Вариант: 5
# Равномерный
# Эрланговский 6 порядка
# 5

# Интенсивность потока обработки
miu = 5


def value_by_erlang_distribution_6(rate):
    return sum(random.exponential([rate], 6))


def value_by_uniform_distribution(rate):
    return random.uniform(rate - 0.1 * rate, rate + 0.1 * rate)


def new_request_time(system_time, rate):
    return system_time + value_by_uniform_distribution(rate)


def new_free_time(system_time):
    return system_time + value_by_uniform_distribution(miu)


# Интенсивность входного потока
inputRates = [a / 10 * miu for a in range(1, 11)]

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

    while done < 1_000_000:
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
        if done % 1_000 == 0:
            print(done + ": " + bufferSize)
print("I'm done! =)")
