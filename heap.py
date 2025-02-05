import heapq

heap = []
heapq.heappush(heap, 10)
heapq.heappush(heap, 1)
heapq.heappush(heap, 2)

print(heap)
heap.append(3)
print(heap)
heapq.heapify(heap)
print(heap)