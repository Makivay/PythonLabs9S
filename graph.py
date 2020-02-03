import igraph

peakNames = {0: "I", 1: "II", 2: "III", 3: "IV", 4: "V", 5: "VI", 6: "VII"}
#    1  2  3  4  5  6  7
table = [
    [0, 1, 0, 0, 0, 3, 0],
    [0, 0, 0, 0, 0, 4, 0],
    [3, 0, 0, 1, 1, 0, 0],
    [2, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 4, 1, 2, 0, 0]
]


def matrix_to_list(matrix):
    list_array = []
    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
            if matrix[x][y] > 0:
                list_array.append((x, y))
    return list_array


list = matrix_to_list(table)


# G = igraph.Graph(directed=False)  # создание ориентированного графа
# G.add_vertices(range(7))  # добавление вершин в граф
# G.vs["label"] = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']  # подписи вершин
# G.add_edges(list)  # добавление ребер в граф
# # G.es["weight"] = [2,4,5,…]	#задание весов ребрам
# # G.es["label"] = range(m)	#подписи ребер
#
# # Построение графа
# igraph.plot(G, bbox=(300, 300))


class Peak:
    def __init__(self, id, name) -> None:
        super().__init__()
        self.id = id
        self.name = name
        self.neighbours = []
        self.neighboursCount = 0

    def add_neighbour(self, neighbour):
        self.neighbours.append(neighbour)
        self.neighboursCount += 1

    def print(self):
        print("Peak[id: {}, name: {}, neighboursCount: {}, neighbours: {}]".format(self.id, self.name,
                                                                                   self.neighboursCount,
                                                                                   self.neighbours))


def graph_to_peak(input_graph):
    peaksArray = []
    for peakNumber in range(len(input_graph)):
        peakArray = input_graph[peakNumber]
        peak = Peak(peakNumber, peakNames[peakNumber])
        for i in range(len(peakArray)):
            if peakArray[i] > 0:
                peak.add_neighbour(i)
        peaksArray.append(peak)
    return peaksArray


peaks = graph_to_peak(table)
for peak in peaks:
    peak.print()


def search_neighbour_for_table(table, peak_number):
    peak_row = table[peak_number]
    neighbours_count = 0
    for weight in peak_row:
        if weight > 0:
            neighbours_count += 1
    peak_column = [table[x][peak_number] for x in range(len(table))]
    for weight in peak_column:
        if weight > 0:
            neighbours_count += 1
    return neighbours_count


print(search_neighbour_for_table(table, 0))


def search_neighbour_for_list(list, peak_number):
    neighbours_count = 0
    for pair in list:
        if pair[0] == peak_number or pair[1] == peak_number:
            neighbours_count += 1
    return neighbours_count


print(search_neighbour_for_list(list, 0))


def search_neighbour_for_peaks(peaks, peak_number):
    neighbours_count = 0
    for peak in peaks:
        if peak.id == peak_number:
            neighbours_count += peak.neighboursCount
        else:
            for neighbour in peak.neighbours:
                if neighbour == peak_number:
                    neighbours_count += 1
    return neighbours_count


print(search_neighbour_for_peaks(peaks, 0))

chain_true = [0, 1, 5, 3]
chain_false = [0, 2, 1, 5, 3]


def search_chain_in_table(table, chain):
    current = chain[0]
    for i in range(len(chain) - 1):
        new = chain[i + 1]
        if table[current][new] == 0:
            return False
        else:
            current = new
    return True


print(search_chain_in_table(table, chain_true))
print(search_chain_in_table(table, chain_false))


def search_chain_in_list(list, chain):
    i = 1
    first = chain[0]
    second = chain[i]
    while i < len(chain) - 1:
        found = False
        for pair in list:
            if first == pair[0] and second == pair[1]:
                found = True
        if not found:
            return False
        first = second
        i += 1
        second = chain[i]
    return True


print(search_chain_in_list(list, chain_true))
print(search_chain_in_list(list, chain_false))


def search_chain_in_peaks(peaks, chain):
    i = 1
    first = chain[0]
    second = chain[i]
    while i < len(chain) - 1:
        found = False
        for peak in peaks:
            for n in peak.neighbours:
                if first == peak.id and second == n:
                    found = True
        if not found:
            return False
        first = second
        i += 1
        second = chain[i]
    return True


print(search_chain_in_peaks(peaks, chain_true))
print(search_chain_in_peaks(peaks, chain_false))
