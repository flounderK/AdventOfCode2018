import sys


class Node:
    METADATA_SUM = 0

    def __init__(self, data):
        self.child_node_quantity = 0
        self.metadata_quantity = 0
        self.metadata = list()
        self.child_nodes_processed = 0
        self.data = data
        self.value = 0
        self.metadata_sum = 0
        self.child_nodes = list()
        self.process_list()

    def add_metadata(self, metadata_item):
        Node.METADATA_SUM += metadata_item
        self.metadata_sum += metadata_item
        self.metadata.append(metadata_item)

    def process_list(self):
        self.child_node_quantity = self.data.pop()
        self.metadata_quantity = self.data.pop()

        while self.child_nodes_processed != self.child_node_quantity:
            self.child_nodes.append(Node(self.data))
            self.child_nodes_processed += 1

        for i in range(0, self.metadata_quantity):
            self.add_metadata(self.data.pop())

        if self.child_node_quantity == 0:
            self.value = self.metadata_sum

        else:
            node_index = 0
            for metadata_item in self.metadata:
                node_index = metadata_item - 1
                if node_index < len(self.child_nodes) and node_index != -1:
                    self.value += self.child_nodes[node_index].value


sys.setrecursionlimit(9999)
print("Recursion limit changed to 9999")

with open("Day8In.txt", "r") as f:
    content = [int(i) for i in f.readline().split(" ")]

content.reverse()
node = Node(content)
print(f"Part 1: {Node.METADATA_SUM}")
print(f"Part 2: {node.value}")

