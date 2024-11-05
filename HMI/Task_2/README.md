# Реализация графоф и алгоритма дейкстры

## Задание

Необходимо написать универсальную основу для представления ненаправленных связных графов и поиска в них кратчайших маршрутов. Далее, этот алгоритм предполагается применять для прокладки маршрутов: на картах, в метро и так далее.

## Листинг программы
```python
from __future__ import annotations
import heapq
from typing import List, Tuple

class Vertex:
    """Класс для представления вершины в графе."""

    def __init__(self):
        """Инициализирует вершину с пустым списком связей."""
        self._links: List[Link] = []

    @property
    def links(self) -> List[Link]:
        """Возвращает список связей, подключенных к этой вершине."""
        return self._links


class Link:
    """Класс для представления связи между двумя вершинами в графе."""

    def __init__(self, v1: Vertex, v2: Vertex):
        """Инициализирует связь между двумя вершинами с расстоянием по умолчанию 1.

        Args:
            v1 (Vertex): Первая вершина.
            v2 (Vertex): Вторая вершина.
        """
        self._v1 = v1
        self._v2 = v2
        self._dist = 1  # Расстояние по умолчанию

    @property
    def v1(self) -> Vertex:
        """Возвращает первую вершину связи."""
        return self._v1

    @property
    def v2(self) -> Vertex:
        """Возвращает вторую вершину связи."""
        return self._v2

    @property
    def dist(self) -> float:
        """Получает или устанавливает расстояние связи."""
        return self._dist

    @dist.setter
    def dist(self, value: float):
        self._dist = value  # Устанавливает новое расстояние


class LinkedGraph:
    """Класс для представления связного неориентированного графа."""

    def __init__(self):
        """Инициализирует граф с пустыми списками связей и вершин."""
        self._links: List[Link] = []
        self._vertex: List[Vertex] = []

    def add_vertex(self, v: Vertex):
        """Добавляет новую вершину в граф, если она еще не присутствует.

        Args:
            v (Vertex): Вершина для добавления.
        """
        if v not in self._vertex:
            self._vertex.append(v)

    def add_link(self, link: Link):
        """Добавляет новую связь в граф, если она еще не присутствует.

        Также добавляет вершины связи в граф, если они еще не присутствуют.

        Args:
            link (Link): Связь для добавления.
        """
        # Добавляем вершины в граф, если их еще нет
        self.add_vertex(link.v1)
        self.add_vertex(link.v2)

        # Проверяем, существует ли уже связь между этими вершинами
        # Так как граф неориентированный, (v1,v2) и (v2,v1) считаются одинаковыми
        for existing_link in self._links:
            if ({existing_link.v1, existing_link.v2} == {link.v1, link.v2}):
                # Связь уже существует
                return

        # Добавляем связь в граф
        self._links.append(link)
        # Также добавляем связь в список связей каждой вершины
        link.v1._links.append(link)
        link.v2._links.append(link)

    def find_path(self, start_v: Vertex, stop_v: Vertex) -> Tuple[List[Vertex], List[Link]]:
        """Находит кратчайший путь между двумя вершинами, используя алгоритм Дейкстры.

        Args:
            start_v (Vertex): Начальная вершина.
            stop_v (Vertex): Конечная вершина.

        Returns:
            tuple: Кортеж, содержащий список вершин кратчайшего пути и список связей между ними.
        """
        # Инициализируем расстояния и предыдущие вершины
        distances = {vertex: float('inf') for vertex in self._vertex}
        previous = {vertex: None for vertex in self._vertex}
        distances[start_v] = 0  # Расстояние до начальной вершины равно 0

        # Очередь приоритетов: (расстояние, счетчик, вершина)
        queue = []
        counter = 0  # Уникальный счетчик последовательности
        heapq.heappush(queue, (0, counter, start_v))
        visited = set()  # Множество посещенных вершин

        while queue:
            current_distance, _, current_vertex = heapq.heappop(queue)

            if current_vertex in visited:
                continue
            visited.add(current_vertex)

            if current_vertex == stop_v:
                break  # Достигли конечной вершины

            for link in current_vertex.links:
                # Определяем соседнюю вершину
                neighbor = link.v1 if link.v2 == current_vertex else link.v2
                if neighbor in visited:
                    continue
                distance = current_distance + link.dist  # Вычисляем новое расстояние

                if distances[neighbor] > distance:
                    distances[neighbor] = distance  # Обновляем минимальное расстояние
                    previous[neighbor] = (current_vertex, link)  # Сохраняем путь
                    counter += 1
                    heapq.heappush(queue, (distance, counter, neighbor))

        # Проверяем, была ли достигнута конечная вершина
        if distances[stop_v] == float('inf'):
            # Путь не существует
            return ([], [])

        # Восстанавливаем путь
        path_vertices = []
        path_links = []
        current_vertex = stop_v

        while previous[current_vertex] is not None:
            path_vertices.append(current_vertex)
            prev_vertex, link = previous[current_vertex]
            path_links.append(link)
            current_vertex = prev_vertex

        path_vertices.append(start_v)
        path_vertices.reverse()
        path_links.reverse()

        return (path_vertices, path_links)


class Station(Vertex):
    """Класс для представления станции метро."""

    def __init__(self, name: str):
        """Инициализирует станцию с заданным именем.

        Args:
            name (str): Название станции.
        """
        super().__init__()
        self.name = name

    def __str__(self) -> str:
        """Возвращает название станции."""
        return self.name

    def __repr__(self) -> str:
        """Возвращает строковое представление станции."""
        return self.name


class LinkMetro(Link):
    """Класс для представления связи между двумя станциями метро."""

    def __init__(self, v1: Vertex, v2: Vertex, dist: float):
        """Инициализирует связь между двумя станциями с заданным расстоянием.

        Args:
            v1 (Vertex): Первая станция.
            v2 (Vertex): Вторая станция.
            dist (float): Расстояние между станциями.
        """
        super().__init__(v1, v2)
        self.dist = dist  # Устанавливаем расстояние связи

def check():
    map2 = LinkedGraph()
    v1 = Vertex()
    v2 = Vertex()
    v3 = Vertex()
    v4 = Vertex()
    v5 = Vertex()
    map2.add_link(Link(v1, v2))
    map2.add_link(Link(v2, v3))
    map2.add_link(Link(v2, v4))
    map2.add_link(Link(v3, v4))
    map2.add_link(Link(v4, v5))
    assert len(map2._links) == 5, "неверное число связей в списке _links класса LinkedGraph"
    assert len(map2._vertex) == 5, "неверное число вершин в списке _vertex класса LinkedGraph"
    map2.add_link(Link(v2, v1))
    assert len(map2._links) == 5, "метод add_link() добавил связь Link(v2, v1), хотя уже имеется связь Link(v1, v2)"
    path = map2.find_path(v1, v5)
    s = sum([x.dist for x in path[1]])
    assert s == 3, "неверная суммарная длина маршрута, возможно, некорректно работает объект-свойство dist"
    assert issubclass(Station, Vertex) and issubclass(LinkMetro, Link), "класс Station должен наследоваться от класса Vertex, а класс LinkMetro от класса Link"
    map2 = LinkedGraph()
    v1 = Station("1")
    v2 = Station("2")
    v3 = Station("3")
    v4 = Station("4")
    v5 = Station("5")
    map2.add_link(LinkMetro(v1, v2, 1))
    map2.add_link(LinkMetro(v2, v3, 2))
    map2.add_link(LinkMetro(v2, v4, 7))
    map2.add_link(LinkMetro(v3, v4, 3))
    map2.add_link(LinkMetro(v4, v5, 1))
    assert len(map2._links) == 5, "неверное число связей в списке _links класса LinkedGraph"
    assert len(map2._vertex) == 5, "неверное число вершин в списке _vertex класса LinkedGraph"
    path = map2.find_path(v1, v5)
    assert str(path[0]) == '[1, 2, 3, 4, 5]', path[0]
    s = sum([x.dist for x in path[1]])
    assert s == 7, "неверная суммарная длина маршрута для карты метро"
if __name__ == "__main__":
    check()
    print("Тестирование прошло успешно")
```

## Пояснение
## Классы Vertex и Link:

* Vertex — это вершина графа, содержащая связи (Link), которые её соединяют с другими вершинами.
* Link — это связь между двумя вершинами с заданным расстоянием (dist). Она неориентированная, то есть соединение между вершинами может быть в обоих направлениях.
## Класс LinkedGraph:

Представляет связный неориентированный граф.
### Методы:
* add_vertex(v: Vertex) добавляет вершину в граф, если она ещё не добавлена.
* add_link(link: Link) добавляет связь между вершинами и обновляет списки связей каждой из связанных вершин.
* find_path(start_v: Vertex, stop_v: Vertex) реализует алгоритм Дейкстры для нахождения кратчайшего пути между двумя вершинами.
### Алгоритм Дейкстры (find_path метод):

* Инициализирует начальные расстояния до всех вершин как бесконечные, кроме стартовой вершины, для которой расстояние равно нулю.
* Использует приоритетную очередь (heapq) для обработки вершин, начиная с начальной вершины. В очереди хранятся вершины с расстояниями, отсортированные по возрастанию.
* Каждый раз извлекает вершину с наименьшим расстоянием и обновляет расстояния до её соседей, если путь через текущую вершину короче.
* Если найдена конечная вершина, алгоритм завершается.
* В конце восстанавливается путь, начиная от конечной вершины и идя по предыдущим вершинам, которые были сохранены при обновлении расстояний.
## Классы Station и LinkMetro:
* Station наследует Vertex и добавляет имя станции, что полезно для представления реальных объектов, таких как станции метро.
* LinkMetro наследует Link и устанавливает расстояние, представляя связь между станциями метро с определённой длиной.
