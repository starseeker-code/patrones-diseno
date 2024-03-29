import abc
from numbers import Number
from typing import Sequence
import heapq

# 1 - Create the interface for the strategies 

class IStrategy(abc.ABC):
    @abc.abstractmethod
    def sorting_algorithm(self):
        ...
        
# 2 - Create the strategies

class SelectionSort(IStrategy):
    def sorting_algorithm(self, data: Sequence[Number]) -> list[Number]:
        data = list(data)
        result = []
        while data:  # xrange() is also a good option
            pivot_number = min(data)
            result.append(pivot_number)
            data.pop(data.index(pivot_number))
        return result
    
class HeapSort(IStrategy):
    def sorting_algorithm(self, data: Sequence[Number]) -> list[Number]:
        data = list(data)
        heapq.heapify(data)  # It's inplace
        return data
    
class QuickSort(IStrategy):
    def sorting_algorithm(self, data: Sequence[Number]) -> list[Number]:
        if len(data) <= 1:  # Check for extreme case empty sequence or single item one
            return data
        pivot = data[len(data) // 2]  # Divides in half the sequence
        left = [number for number in data if number < pivot]  # Groups numbers that are LESS than the pivot
        mid = [number for number in data if number == pivot]  # Groups numbers the pivot itself
        right = [number for number in data if number > pivot]  # Groups numbers that are MORE than the pivot
        return self.sorting_algorithm(left) + mid + self.sorting_algorithm(right)  # Recursively does the same until it adds 1-item ordered lists
    
class MergeSort(IStrategy):
    @staticmethod
    def merge(left: Sequence[Number], right: Sequence[Number]) -> list[Number]:
        order = lambda x, y: x < y  # Compares 1-sized sequences two elements at a time, and orders them
        result = []  # Stores the ordered results
        index_left = index_right = 0  # References to the index position of the sequence elements
        while index_left < len(left) and index_right < len(right):
            if order(left[index_left], right[index_right]):  # If x < y appends x and shifts to next number to the left
                result.append(left[index_left])
                index_left += 1
            else:  # If x > y appends y and shifts to next number to the right
                result.append(right[index_right])
                index_right += 1
        result.extend(left[index_left:])
        result.extend(right[index_right:])
        return result
    
    def sorting_algorithm(self, data: Sequence[Number]) -> list[Number]:
        if len(data) <= 1:
            return list(data)  # Trivial return
        middle = len(data) // 2  # Divides in half the sequence
        left = data[:middle]
        right = data[middle:]
        left = self.sorting_algorithm(left)  # Starts sorting the two halfs, recursively
        right = self.sorting_algorithm(right)
        return self.merge(left, right)  # Joins the (sorted) pieces of the sequence

# 3 - Create the context

class Sorter:
    def __init__(self, strategy: IStrategy = SelectionSort(), data: Sequence[Number] = None):
        self._strategy = strategy
        self._data = data
    
    @property
    def strategy(self) -> IStrategy:
        return self._strategy
    
    @strategy.setter
    def strategy(self, strategy: IStrategy):
        self._strategy = strategy
        
    def sort(self, data: Sequence[Number] = None) -> Sequence[Number]:
        if data:
            self._data = data
        result = self._strategy.sorting_algorithm(self._data)
        self._data = result  # Not needed, but I like to keep the sorted data since it's already sorted
        return result
    
    def __str__(self) -> str:
        return f"Sorter -> Strategy: {self._strategy.__class__.__name__}  Data: {self._data}"

# 4 - Use the pattern

unsorted_list = [2, 5, 1, 3, 1, -2, 4]  # Sample data

sorter_instance = Sorter()  # Instantiation of a Sorter
sorter_instance.sort(unsorted_list)  # Use of the strategy pattern
sorter_instance.strategy = QuickSort()  # Change of algorithm during runtime
other_instance = Sorter(MergeSort(), unsorted_list)  # Sorter can be instantiated as many times as needed
other_instance.sort()  # It's a good practice to have default behaviour


# Code for tests
if __name__ == "__main__":
    test_data = (0, -11, 3.2, 60, 29, 96, -19, 8, 19, 7.1, 48, 58, 2.8, -81, 24, 84, 5.0, 9, 29, 103.462, 8,
                   60, 8.2, 34, 85, 100, -5.2, 28, 60, 88, 76, 8, 30.42, 79, -22, 40, 54, 0, 18, 89, -43.0031,
                   59, 71, 70.49, 45, 63, 63, 51, 71, 38, 48, 58, 24, 87, 79, 26, 51, 43, 22, 11, 14, 19, 85)
    # Instantiation test
    test = Sorter(data=test_data)
    test.sort()
    print(test)
    # Algorithm test
    print(Sorter(HeapSort(), test_data).sort())
    print(Sorter(QuickSort(), test_data).sort())
    print(Sorter(MergeSort(), test_data).sort())
