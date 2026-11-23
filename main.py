"""
=============================================================================
Project Title : Student Records & Result Manager (FDS Capstone Project)
Course        : Fundamentals of Data Structures & Algorithms (FDS / DSA)
Language      : Python 3 (Pure DSA Implementation from First Principles)
=============================================================================
Data Structures & Algorithms Implemented:
  1. ARRAY               : Fixed subject marks array & contiguous memory buffer
  2. DOUBLY LINKED LIST  : Dynamic student records repository (O(1) insert/delete)
  3. STACK (LIFO)        : Undo system for transactional record modifications
  4. QUEUE (FIFO)        : Circular request queue for result verification/clearance
  5. TREE (BST)          : Binary Search Tree index for O(log n) roll number lookups
  6. GRAPH               : Prerequisite dependency & peer network (BFS, DFS, TopoSort)
  7. SEARCHING           : Binary Search (O(log n)) & Linear Search (O(n))
  8. SORTING             : Merge Sort (O(n log n)) & Quick Sort (O(n log n))
=============================================================================
"""

import sys
from typing import List, Optional, Tuple, Any

# =============================================================================
# 1. ARRAY: Fixed-Size Subject Marks Array Abstraction
# =============================================================================
SUBJECT_NAMES = ["Data Structures", "Digital Logic", "Discrete Math", "OOPs in C++", "Computer Org"]
NUM_SUBJECTS = 5

class MarksArray:
    """Represents a fixed-size contiguous array of subject marks."""
    def __init__(self, marks_list: Optional[List[float]] = None):
        self._data = [0.0] * NUM_SUBJECTS
        if marks_list:
            for i in range(min(len(marks_list), NUM_SUBJECTS)):
                self._data[i] = float(marks_list[i])

    def get(self, index: int) -> float:
        if 0 <= index < NUM_SUBJECTS:
            return self._data[index]
        raise IndexError("MarksArray index out of bounds")

    def set(self, index: int, value: float) -> None:
        if 0 <= index < NUM_SUBJECTS:
            if 0.0 <= value <= 100.0:
                self._data[index] = float(value)
            else:
                raise ValueError("Marks must be between 0 and 100")
        else:
            raise IndexError("MarksArray index out of bounds")

    def total(self) -> float:
        tot = 0.0
        for i in range(NUM_SUBJECTS):
            tot += self._data[i]
        return tot

    def percentage(self) -> float:
        return self.total() / NUM_SUBJECTS

    def to_list(self) -> List[float]:
        return [self._data[i] for i in range(NUM_SUBJECTS)]

    def __str__(self) -> str:
        return ", ".join(f"{SUBJECT_NAMES[i]}: {self._data[i]:.1f}" for i in range(NUM_SUBJECTS))


# =============================================================================
# STUDENT ENTITY
# =============================================================================
class Student:
    """Core student model containing academic credentials."""
    def __init__(self, roll_no: int, name: str, marks_list: List[float]):
        self.roll_no: int = roll_no
        self.name: str = name
        self.marks: MarksArray = MarksArray(marks_list)
        self.total: float = self.marks.total()
        self.percentage: float = self.marks.percentage()
        self.grade: str = self._calculate_grade()

    def update_marks(self, marks_list: List[float]) -> None:
        self.marks = MarksArray(marks_list)
        self.total = self.marks.total()
        self.percentage = self.marks.percentage()
        self.grade = self._calculate_grade()

    def _calculate_grade(self) -> str:
        p = self.percentage
        if p >= 90.0: return "O (Outstanding)"
        elif p >= 80.0: return "A+ (Excellent)"
        elif p >= 70.0: return "A (Very Good)"
        elif p >= 60.0: return "B+ (Good)"
        elif p >= 50.0: return "B (Above Average)"
        elif p >= 40.0: return "P (Pass)"
        else: return "F (Fail)"

    def clone(self) -> 'Student':
        return Student(self.roll_no, self.name, self.marks.to_list())

    def __repr__(self) -> str:
        return f"Student(Roll={self.roll_no}, Name='{self.name}', Total={self.total:.1f}, %={self.percentage:.1f}%, Grade={self.grade})"


# =============================================================================
# 2. DOUBLY LINKED LIST: Primary Dynamic Storage for Student Records
# =============================================================================
class DLLNode:
    """Node for Doubly Linked List."""
    def __init__(self, student: Student):
        self.student: Student = student
        self.prev: Optional['DLLNode'] = None
        self.next: Optional['DLLNode'] = None

class StudentDoublyLinkedList:
    """
    Doubly Linked List allowing O(1) head/tail insertions,
    bidirectional iteration, and linear-time updates/deletions.
    """
    def __init__(self):
        self.head: Optional[DLLNode] = None
        self.tail: Optional[DLLNode] = None
        self.size: int = 0

    def insert_at_end(self, student: Student) -> bool:
        """Appends a new student record to the linked list."""
        if self.find_by_roll(student.roll_no) is not None:
            return False  # Duplicate roll number
        new_node = DLLNode(student)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.size += 1
        return True

    def find_by_roll(self, roll_no: int) -> Optional[Student]:
        curr = self.head
        while curr:
            if curr.student.roll_no == roll_no:
                return curr.student
            curr = curr.next
        return None

    def delete_by_roll(self, roll_no: int) -> Optional[Student]:
        """Removes a student node and returns the deleted student record."""
        curr = self.head
        while curr:
            if curr.student.roll_no == roll_no:
                removed_student = curr.student
                if curr.prev:
                    curr.prev.next = curr.next
                else:
                    self.head = curr.next

                if curr.next:
                    curr.next.prev = curr.prev
                else:
                    self.tail = curr.prev

                self.size -= 1
                return removed_student
            curr = curr.next
        return None

    def to_array(self) -> List[Student]:
        """Converts linked list nodes to contiguous array buffer."""
        result = []
        curr = self.head
        while curr:
            result.append(curr.student)
            curr = curr.next
        return result

    def is_empty(self) -> bool:
        return self.size == 0


# =============================================================================
# 3. STACK: LIFO Undo Operation System
# =============================================================================
class ActionSnapshot:
    """Represents a state change to enable Undo."""
    def __init__(self, action_type: str, student_before: Optional[Student], student_after: Optional[Student]):
        # action_type in ['INSERT', 'DELETE', 'UPDATE']
        self.action_type: str = action_type
        self.student_before: Optional[Student] = student_before.clone() if student_before else None
        self.student_after: Optional[Student] = student_after.clone() if student_after else None

class UndoStack:
    """
    Fixed-capacity/dynamic stack implementing LIFO order.
    Pushes recent mutations and pops to revert state.
    """
    def __init__(self, capacity: int = 50):
        self._stack: List[ActionSnapshot] = []
        self.capacity: int = capacity

    def push(self, action: ActionSnapshot) -> bool:
        if len(self._stack) >= self.capacity:
            self._stack.pop(0)  # Evict oldest snapshot
        self._stack.append(action)
        return True

    def pop(self) -> Optional[ActionSnapshot]:
        if self.is_empty():
            return None
        return self._stack.pop()

    def peek(self) -> Optional[ActionSnapshot]:
        if self.is_empty():
            return None
        return self._stack[-1]

    def is_empty(self) -> bool:
        return len(self._stack) == 0

    def size(self) -> int:
        return len(self._stack)


# =============================================================================
# 4. QUEUE: Circular Queue for Result Clearance / Verification Requests
# =============================================================================
class ClearanceRequest:
    def __init__(self, request_id: int, roll_no: int, request_type: str):
        self.request_id = request_id
        self.roll_no = roll_no
        self.request_type = request_type  # e.g., 'Grade Revaluation', 'Transcript', 'Bonafide'

    def __repr__(self):
        return f"[Req #{self.request_id}] Roll: {self.roll_no} | Purpose: {self.request_type}"

class CircularQueue:
    """
    Fixed-size Circular Queue implementation from first principles.
    Handles FIFO request queues efficiently without memory shifting.
    """
    def __init__(self, capacity: int = 20):
        self.capacity: int = capacity
        self._queue: List[Optional[ClearanceRequest]] = [None] * capacity
        self.front: int = -1
        self.rear: int = -1
        self._count: int = 0

    def is_full(self) -> bool:
        return self._count == self.capacity

    def is_empty(self) -> bool:
        return self._count == 0

    def enqueue(self, item: ClearanceRequest) -> bool:
        if self.is_full():
            return False
        if self.front == -1:
            self.front = 0
            self.rear = 0
        else:
            self.rear = (self.rear + 1) % self.capacity
        self._queue[self.rear] = item
        self._count += 1
        return True

    def dequeue(self) -> Optional[ClearanceRequest]:
        if self.is_empty():
            return None
        item = self._queue[self.front]
        self._queue[self.front] = None
        if self.front == self.rear:
            self.front = -1
            self.rear = -1
        else:
            self.front = (self.front + 1) % self.capacity
        self._count -= 1
        return item

    def get_all(self) -> List[ClearanceRequest]:
        items = []
        if self.is_empty():
            return items
        idx = self.front
        for _ in range(self._count):
            if self._queue[idx] is not None:
                items.append(self._queue[idx])
            idx = (idx + 1) % self.capacity
        return items


# =============================================================================
# 5. TREE: Binary Search Tree (BST) for Fast O(log n) Searching & In-order
# =============================================================================
class BSTNode:
    def __init__(self, student: Student):
        self.student: Student = student
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None

class StudentBST:
    """
    Binary Search Tree indexed on student Roll Number.
    Provides logarithmic average search time O(log n) and
    in-order sorted traversal.
    """
    def __init__(self):
        self.root: Optional[BSTNode] = None

    def insert(self, student: Student) -> None:
        self.root = self._insert_recursive(self.root, student)

    def _insert_recursive(self, node: Optional[BSTNode], student: Student) -> BSTNode:
        if node is None:
            return BSTNode(student)
        if student.roll_no < node.student.roll_no:
            node.left = self._insert_recursive(node.left, student)
        elif student.roll_no > node.student.roll_no:
            node.right = self._insert_recursive(node.right, student)
        else:
            node.student = student  # Update existing
        return node

    def search_by_roll(self, roll_no: int) -> Tuple[Optional[Student], int]:
        """Returns (Student, steps_taken) to demonstrate binary search efficiency."""
        curr = self.root
        steps = 0
        while curr:
            steps += 1
            if roll_no == curr.student.roll_no:
                return curr.student, steps
            elif roll_no < curr.student.roll_no:
                curr = curr.left
            else:
                curr = curr.right
        return None, steps

    def inorder_traversal(self) -> List[Student]:
        result: List[Student] = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node: Optional[BSTNode], result: List[Student]) -> None:
        if node:
            self._inorder(node.left, result)
            result.append(node.student)
            self._inorder(node.right, result)

    def search_by_name(self, name_query: str) -> List[Student]:
        """Searches students whose name matches or contains the query."""
        matches: List[Student] = []
        all_students = self.inorder_traversal()
        q = name_query.lower()
        for s in all_students:
            if q in s.name.lower():
                matches.append(s)
        return matches

    def rebuild_from_list(self, students: List[Student]) -> None:
        self.root = None
        for s in students:
            self.insert(s)


# =============================================================================
# 6. GRAPH: Prerequisite Dependency & Peer Mentorship Network
# =============================================================================
class AcademicGraph:
    """
    Directed & Undirected Graph using Adjacency List.
    Features:
      - Subject Prerequisite DAG: Topological Sort (Kahn's Algorithm)
      - Peer Mentorship Network: BFS for shortest connection & DFS for study clusters
    """
    def __init__(self):
        self.adj_list: dict[str, List[str]] = {}
        self.in_degree: dict[str, int] = {}

    def add_vertex(self, vertex: str) -> None:
        if vertex not in self.adj_list:
            self.adj_list[vertex] = []
            self.in_degree[vertex] = 0

    def add_directed_edge(self, u: str, v: str) -> None:
        """u -> v means u is a prerequisite for v."""
        self.add_vertex(u)
        self.add_vertex(v)
        self.adj_list[u].append(v)
        self.in_degree[v] = self.in_degree.get(v, 0) + 1

    def add_undirected_edge(self, u: str, v: str) -> None:
        """Represents peer mentorship / study group connection between u and v."""
        self.add_vertex(u)
        self.add_vertex(v)
        if v not in self.adj_list[u]:
            self.adj_list[u].append(v)
        if u not in self.adj_list[v]:
            self.adj_list[v].append(u)

    def topological_sort(self) -> Tuple[List[str], bool]:
        """
        Kahn's Algorithm (BFS-based) for Topological Sort.
        Returns (sorted_order, has_cycle).
        """
        in_deg = dict(self.in_degree)
        queue = [v for v, deg in in_deg.items() if deg == 0]
        topo_order = []

        while queue:
            node = queue.pop(0)
            topo_order.append(node)
            for neighbor in self.adj_list.get(node, []):
                in_deg[neighbor] -= 1
                if in_deg[neighbor] == 0:
                    queue.append(neighbor)

        has_cycle = (len(topo_order) != len(self.adj_list))
        return topo_order, has_cycle

    def bfs_shortest_path(self, start: str, target: str) -> Optional[List[str]]:
        """Finds shortest peer connection path using Breadth-First Search."""
        if start not in self.adj_list or target not in self.adj_list:
            return None
        visited = {start}
        queue = [[start]]

        while queue:
            path = queue.pop(0)
            node = path[-1]
            if node == target:
                return path
            for neighbor in self.adj_list.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
        return None

    def dfs_explore(self, start: str) -> List[str]:
        """Explores reachable study circle nodes using Depth-First Search."""
        visited = set()
        order = []

        def _dfs(node: str):
            visited.add(node)
            order.append(node)
            for neighbor in self.adj_list.get(node, []):
                if neighbor not in visited:
                    _dfs(neighbor)

        if start in self.adj_list:
            _dfs(start)
        return order


# =============================================================================
# 7 & 8. SORTING & SEARCHING ALGORITHMS
# =============================================================================
class Sorter:
    """Pure implementation of Merge Sort and Quick Sort from first principles."""

    @staticmethod
    def merge_sort_by_percentage(arr: List[Student], descending: bool = True) -> List[Student]:
        """
        Merge Sort (Divide and Conquer, O(n log n) Guaranteed Time).
        Stable sort ideal for producing consistent Rank Lists.
        """
        if len(arr) <= 1:
            return list(arr)

        mid = len(arr) // 2
        left_half = Sorter.merge_sort_by_percentage(arr[:mid], descending)
        right_half = Sorter.merge_sort_by_percentage(arr[mid:], descending)

        return Sorter._merge(left_half, right_half, descending)

    @staticmethod
    def _merge(left: List[Student], right: List[Student], descending: bool) -> List[Student]:
        merged: List[Student] = []
        i = j = 0

        while i < len(left) and j < len(right):
            cond = (left[i].percentage >= right[j].percentage) if descending else (left[i].percentage <= right[j].percentage)
            if cond:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        while i < len(left):
            merged.append(left[i])
            i += 1
        while j < len(right):
            merged.append(right[j])
            j += 1

        return merged

    @staticmethod
    def quick_sort_by_roll(arr: List[Student], low: int, high: int) -> None:
        """
        Quick Sort (In-Place, O(n log n) Average Time).
        Sorts array in ascending order by Roll Number.
        """
        if low < high:
            pi = Sorter._partition(arr, low, high)
            Sorter.quick_sort_by_roll(arr, low, pi - 1)
            Sorter.quick_sort_by_roll(arr, pi + 1, high)

    @staticmethod
    def _partition(arr: List[Student], low: int, high: int) -> int:
        pivot = arr[high].roll_no
        i = low - 1
        for j in range(low, high):
            if arr[j].roll_no <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1


class Searcher:
    """Pure implementation of Binary Search & Linear Search."""

    @staticmethod
    def binary_search_by_roll(sorted_arr: List[Student], target_roll: int) -> Tuple[Optional[Student], int]:
        """
        Binary Search on contiguous array sorted by roll number.
        Returns (Student, steps). O(log n) time complexity.
        """
        low = 0
        high = len(sorted_arr) - 1
        steps = 0

        while low <= high:
            steps += 1
            mid = (low + high) // 2
            if sorted_arr[mid].roll_no == target_roll:
                return sorted_arr[mid], steps
            elif sorted_arr[mid].roll_no < target_roll:
                low = mid + 1
            else:
                high = mid - 1

        return None, steps

    @staticmethod
    def linear_search_by_name(arr: List[Student], name_substr: str) -> Tuple[List[Student], int]:
        """
        Linear Search on unsorted array or linked list.
        Returns (matches, steps). O(n) time complexity.
        """
        matches = []
        steps = 0
        target = name_substr.lower()
        for s in arr:
            steps += 1
            if target in s.name.lower():
                matches.append(s)
        return matches, steps


# =============================================================================
# SYSTEM CONTROLLER: Integrating All DSA Components
# =============================================================================
class StudentResultManager:
    """Coordinates records, DSA operations, state transitions, and reporting."""

    def __init__(self):
        self.student_list = StudentDoublyLinkedList()
        self.bst_index = StudentBST()
        self.undo_stack = UndoStack(capacity=30)
        self.clearance_queue = CircularQueue(capacity=15)
        self.prereq_graph = AcademicGraph()
        self.peer_network = AcademicGraph()
        self._next_request_id = 101

        # Seed realistic academic graphs and default data
        self._init_graphs()
        self._seed_sample_students()

    def _init_graphs(self):
        # 1. Prerequisite Course Graph (Directed Acyclic Graph)
        courses = [
            ("Digital Logic", "Computer Org"),
            ("Discrete Math", "Data Structures"),
            ("OOPs in C++", "Data Structures"),
            ("Data Structures", "Design & Analysis of Algorithms"),
            ("Computer Org", "Operating Systems"),
            ("Design & Analysis of Algorithms", "Advanced AI")
        ]
        for u, v in courses:
            self.prereq_graph.add_directed_edge(u, v)

    def _seed_sample_students(self):
        samples = [
            (101, "Rahul Patil",      [82.0, 88.0, 76.5, 90.0, 84.0]),
            (102, "Priya Sharma",     [92.0, 95.0, 90.0, 96.0, 94.0]),
            (103, "Amit Verma",       [70.0, 68.0, 74.0, 65.0, 72.0]),
            (104, "Snehal Deshmukh",  [85.0, 89.0, 82.0, 88.0, 86.0]),
            (105, "Aryan Gupta",      [75.0, 80.0, 78.0, 82.0, 79.0]),
            (106, "Tanvi Kulkarni",   [58.0, 62.0, 35.0, 60.0, 58.0]),
            (107, "Devendra Joshi",   [88.0, 90.0, 85.0, 92.0, 89.0]),
            (108, "Riya Shah",        [36.0, 50.0, 45.0, 48.0, 38.0]),
            (109, "Siddharth Nair",   [89.0, 93.0, 88.0, 94.0, 91.0]),
            (110, "Aniket Shinde",    [64.0, 68.0, 66.0, 70.0, 65.0])
        ]
        for roll, name, marks in samples:
            s = Student(roll, name, marks)
            self.student_list.insert_at_end(s)
            self.bst_index.insert(s)

        # Peer Study Group Network
        self.peer_network.add_undirected_edge("Rahul Patil", "Priya Sharma")
        self.peer_network.add_undirected_edge("Priya Sharma", "Snehal Deshmukh")
        self.peer_network.add_undirected_edge("Snehal Deshmukh", "Devendra Joshi")
        self.peer_network.add_undirected_edge("Amit Verma", "Aryan Gupta")
        self.peer_network.add_undirected_edge("Aryan Gupta", "Riya Shah")
        self.peer_network.add_undirected_edge("Siddharth Nair", "Devendra Joshi")

    # --- Student Record Transactions ---
    def add_student(self, roll_no: int, name: str, marks: List[float]) -> Tuple[bool, str]:
        if self.student_list.find_by_roll(roll_no):
            return False, f"Student with Roll No {roll_no} already exists!"
        student = Student(roll_no, name, marks)
        self.student_list.insert_at_end(student)
        self.bst_index.insert(student)
        # Push action to Undo Stack
        self.undo_stack.push(ActionSnapshot("INSERT", None, student))
        return True, f"Student '{name}' (Roll {roll_no}) successfully registered."

    def delete_student(self, roll_no: int) -> Tuple[bool, str]:
        deleted = self.student_list.delete_by_roll(roll_no)
        if not deleted:
            return False, f"Roll No {roll_no} not found."
        # Rebuild BST without deleted student
        self.bst_index.rebuild_from_list(self.student_list.to_array())
        # Push to Undo Stack
        self.undo_stack.push(ActionSnapshot("DELETE", deleted, None))
        return True, f"Student '{deleted.name}' (Roll {roll_no}) removed."

    def update_student_marks(self, roll_no: int, new_marks: List[float]) -> Tuple[bool, str]:
        student = self.student_list.find_by_roll(roll_no)
        if not student:
            return False, f"Roll No {roll_no} not found."
        before_state = student.clone()
        student.update_marks(new_marks)
        self.bst_index.insert(student)
        self.undo_stack.push(ActionSnapshot("UPDATE", before_state, student))
        return True, f"Marks updated for '{student.name}'. New %: {student.percentage:.2f}%"

    def undo_last_action(self) -> Tuple[bool, str]:
        action = self.undo_stack.pop()
        if not action:
            return False, "Undo stack is empty! No recent actions to revert."

        if action.action_type == "INSERT":
            # Revert insert by deleting
            assert action.student_after is not None
            self.student_list.delete_by_roll(action.student_after.roll_no)
            self.bst_index.rebuild_from_list(self.student_list.to_array())
            return True, f"Undo [INSERT]: Removed student '{action.student_after.name}' (Roll {action.student_after.roll_no})."

        elif action.action_type == "DELETE":
            # Revert delete by re-inserting
            assert action.student_before is not None
            s = action.student_before.clone()
            self.student_list.insert_at_end(s)
            self.bst_index.insert(s)
            return True, f"Undo [DELETE]: Restored student '{s.name}' (Roll {s.roll_no})."

        elif action.action_type == "UPDATE":
            # Revert update by restoring previous marks
            assert action.student_before is not None
            student = self.student_list.find_by_roll(action.student_before.roll_no)
            if student:
                student.update_marks(action.student_before.marks.to_list())
                self.bst_index.insert(student)
            return True, f"Undo [UPDATE]: Restored marks for '{action.student_before.name}' (Roll {action.student_before.roll_no})."

        return False, "Unknown action in stack."

    # --- Rank List & Toppers ---
    def generate_rank_list(self) -> List[Student]:
        raw_array = self.student_list.to_array()
        sorted_ranks = Sorter.merge_sort_by_percentage(raw_array, descending=True)
        return sorted_ranks

    def get_toppers(self, k: int = 3) -> List[Student]:
        ranks = self.generate_rank_list()
        return ranks[:k]

    # --- Search Methods ---
    def search_by_roll_bst(self, roll_no: int) -> Tuple[Optional[Student], int]:
        return self.bst_index.search_by_roll(roll_no)

    def search_by_roll_binary_search(self, roll_no: int) -> Tuple[Optional[Student], int]:
        arr = self.student_list.to_array()
        if not arr:
            return None, 0
        # In-place Quick Sort by Roll No for Binary Search
        Sorter.quick_sort_by_roll(arr, 0, len(arr) - 1)
        return Searcher.binary_search_by_roll(arr, roll_no)

    def search_by_name(self, name_query: str) -> Tuple[List[Student], int]:
        arr = self.student_list.to_array()
        return Searcher.linear_search_by_name(arr, name_query)

    # --- Queue Operations ---
    def submit_request(self, roll_no: int, req_type: str) -> Tuple[bool, str]:
        if not self.student_list.find_by_roll(roll_no):
            return False, f"Roll No {roll_no} not found in student database!"
        req = ClearanceRequest(self._next_request_id, roll_no, req_type)
        self._next_request_id += 1
        if self.clearance_queue.enqueue(req):
            return True, f"Request enqueued: {req}"
        return False, "Clearance queue is full! Please process pending requests first."

    def process_request(self) -> Tuple[Optional[ClearanceRequest], str]:
        req = self.clearance_queue.dequeue()
        if not req:
            return None, "Clearance request queue is empty."
        student = self.student_list.find_by_roll(req.roll_no)
        s_name = student.name if student else "Unknown"
        return req, f"Processed Request #{req.request_id} for {s_name} (Roll {req.roll_no}) -> [{req.request_type}] APPROVED."


# =============================================================================
# CLI INTERACTION & PRETTY REPORTING
# =============================================================================
def print_separator(char: str = "=", length: int = 80):
    print(char * length)

def display_student_table(students: List[Student], title: str = "Student Records", show_rank: bool = False):
    print_separator("=")
    print(f" {title.upper()} (Total Records: {len(students)})")
    print_separator("=")
    header = f"{'Rank' if show_rank else 'No.' :<6} | {'Roll' :<6} | {'Name' :<18} | {'Total' :<7} | {'%' :<6} | {'Grade' :<16}"
    print(header)
    print_separator("-")
    for idx, s in enumerate(students, 1):
        rank_or_no = f"#{idx}"
        print(f"{rank_or_no:<6} | {s.roll_no:<6} | {s.name:<18} | {s.total:<7.1f} | {s.percentage:<6.2f} | {s.grade:<16}")
    print_separator("=")


def run_interactive_cli():
    manager = StudentResultManager()

    while True:
        print("\n" + "="*80)
        print(" STUDENT RECORDS & RESULT MANAGER (FDS CAPSTONE)")
        print(" Demonstrating All Core Data Structures & Algorithms")
        print("="*80)
        print(" 1. [ARRAY & LINKED LIST] Display All Student Records")
        print(" 2. [LINKED LIST & BST]   Add New Student Record")
        print(" 3. [LINKED LIST & STACK] Delete Student Record (Supports Undo)")
        print(" 4. [ARRAY & STACK]       Update Student Marks (Supports Undo)")
        print(" 5. [STACK]               Undo Last Operation (LIFO Action History)")
        print(" 6. [TREE / BST]          Search Student by Roll Number (BST Search O(log n))")
        print(" 7. [ARRAY & BINARY SRCH] Search Student by Roll Number (Binary Search O(log n))")
        print(" 8. [LINEAR SEARCH]       Search Student by Name / Substring (O(n))")
        print(" 9. [MERGE SORT]          Generate Merit Rank List (Sorted Descending)")
        print("10. [QUICK SORT]          View Top Toppers (Top K Awardees)")
        print("11. [QUEUE (FIFO)]        Student Clearance / Transcript Request Queue")
        print("12. [GRAPH - TOPO SORT]   Course Prerequisite Graduation Pathway (DAG)")
        print("13. [GRAPH - BFS & DFS]   Peer Mentorship & Study Circle Discovery")
        print("14. [DEMO BENCHMARK]      Compare Search Algorithms Performance (BST vs Binary vs Linear)")
        print(" 0. Exit System")
        print("="*80)

        choice = input("Enter choice (0-14): ").strip()

        if choice == "1":
            students = manager.student_list.to_array()
            display_student_table(students, "All Enrolled Student Records")

        elif choice == "2":
            print("\n--- Add New Student Record ---")
            try:
                roll = int(input("Enter Roll Number: ").strip())
                name = input("Enter Full Name: ").strip()
                print(f"Enter marks out of 100 for {NUM_SUBJECTS} subjects:")
                marks = []
                for sub in SUBJECT_NAMES:
                    m = float(input(f"  {sub}: ").strip())
                    marks.append(m)
                success, msg = manager.add_student(roll, name, marks)
                print(f"\n[Result]: {msg}")
            except Exception as e:
                print(f"[Error]: Invalid input ({e})")

        elif choice == "3":
            print("\n--- Delete Student Record ---")
            try:
                roll = int(input("Enter Roll Number to delete: ").strip())
                success, msg = manager.delete_student(roll)
                print(f"\n[Result]: {msg}")
                if success:
                    print("Hint: You can select Option 5 (Undo) to restore this record!")
            except Exception as e:
                print(f"[Error]: Invalid roll number ({e})")

        elif choice == "4":
            print("\n--- Update Student Marks ---")
            try:
                roll = int(input("Enter Roll Number to update: ").strip())
                student = manager.student_list.find_by_roll(roll)
                if not student:
                    print(f"[Error]: Roll number {roll} not found.")
                    continue
                print(f"Updating marks for {student.name}. Current total: {student.total:.1f}")
                new_marks = []
                for sub in SUBJECT_NAMES:
                    m = float(input(f"  New {sub}: ").strip())
                    new_marks.append(m)
                success, msg = manager.update_student_marks(roll, new_marks)
                print(f"\n[Result]: {msg}")
            except Exception as e:
                print(f"[Error]: Input error ({e})")

        elif choice == "5":
            print("\n--- Undo Last Operation (Stack LIFO) ---")
            success, msg = manager.undo_last_action()
            print(f"[Undo Result]: {msg}")
            print(f"Remaining undo history size: {manager.undo_stack.size()}")

        elif choice == "6":
            print("\n--- Search Student via Binary Search Tree (BST) ---")
            try:
                roll = int(input("Enter Roll Number to search: ").strip())
                student, steps = manager.search_by_roll_bst(roll)
                if student:
                    print(f"\n[Found in {steps} BST comparison step(s)]:")
                    print(f"  Roll No    : {student.roll_no}")
                    print(f"  Name       : {student.name}")
                    print(f"  Subject Marks: {student.marks}")
                    print(f"  Total Marks: {student.total:.1f} / 500")
                    print(f"  Percentage : {student.percentage:.2f}%")
                    print(f"  Grade      : {student.grade}")
                else:
                    print(f"\n[Not Found]: Roll No {roll} does not exist in BST (Searched {steps} nodes).")
            except Exception as e:
                print(f"[Error]: Invalid input ({e})")

        elif choice == "7":
            print("\n--- Search Student via Binary Search on Sorted Array ---")
            try:
                roll = int(input("Enter Roll Number to search: ").strip())
                student, steps = manager.search_by_roll_binary_search(roll)
                if student:
                    print(f"\n[Found in {steps} Binary Search step(s)]:")
                    print(f"  Roll No    : {student.roll_no} | Name: {student.name} | %: {student.percentage:.2f}%")
                else:
                    print(f"\n[Not Found]: Roll No {roll} not found after {steps} iterations.")
            except Exception as e:
                print(f"[Error]: Invalid input ({e})")

        elif choice == "8":
            print("\n--- Search Student by Name / Substring (Linear Search) ---")
            q = input("Enter name or search substring: ").strip()
            matches, steps = manager.search_by_name(q)
            print(f"\n[Linear Search Completed in {steps} step(s) across list]: Found {len(matches)} match(es)")
            if matches:
                display_student_table(matches, f"Search Results for '{q}'")

        elif choice == "9":
            print("\n--- Merit Rank List (Merge Sort - Stable O(n log n)) ---")
            rank_list = manager.generate_rank_list()
            display_student_table(rank_list, "Official Semester Merit Rank List", show_rank=True)

        elif choice == "10":
            print("\n--- Top Toppers List (Quick Sort Partitioning) ---")
            try:
                k_val = int(input("How many toppers would you like to view? (Default 3): ") or 3)
                toppers = manager.get_toppers(k_val)
                display_student_table(toppers, f"Top {len(toppers)} Academic Toppers", show_rank=True)
            except Exception as e:
                print(f"[Error]: Invalid number ({e})")

        elif choice == "11":
            print("\n--- Circular Queue: Result & Transcript Processing ---")
            print(" 1. Submit New Request (Enqueue)")
            print(" 2. Process Next Pending Request (Dequeue - FIFO)")
            print(" 3. View All Queued Requests")
            sub_choice = input("Select sub-option (1-3): ").strip()
            if sub_choice == "1":
                try:
                    r_roll = int(input("Enter Student Roll Number: ").strip())
                    print("Request Types: 1. Transcript | 2. Grade Revaluation | 3. Bonafide Certificate")
                    type_map = {"1": "Official Transcript", "2": "Grade Revaluation", "3": "Bonafide Certificate"}
                    rt_key = input("Choose request type (1-3): ").strip()
                    rt_val = type_map.get(rt_key, "General Inquiry")
                    ok, msg = manager.submit_request(r_roll, rt_val)
                    print(f"[Queue Enqueue]: {msg}")
                except Exception as e:
                    print(f"[Error]: {e}")
            elif sub_choice == "2":
                req, msg = manager.process_request()
                print(f"[Queue Dequeue]: {msg}")
            elif sub_choice == "3":
                requests = manager.clearance_queue.get_all()
                print(f"\nPending Requests in Circular Queue ({len(requests)} items):")
                if not requests:
                    print("  (Queue is currently empty)")
                else:
                    for i, r in enumerate(requests, 1):
                        print(f"  {i}. {r}")

        elif choice == "12":
            print("\n--- Graph: Course Prerequisite Graduation Pathway ---")
            print("Demonstrating Topological Sort (Kahn's Algorithm on Directed Acyclic Graph)")
            topo_order, has_cycle = manager.prereq_graph.topological_sort()
            if has_cycle:
                print("[Warning]: Prerequisite cycle detected in curriculum graph!")
            else:
                print("\nRecommended Sequential Course Completion Pathway:")
                for step, course in enumerate(topo_order, 1):
                    prereqs = [u for u, v_list in manager.prereq_graph.adj_list.items() if course in v_list]
                    prereq_str = f" (Requires: {', '.join(prereqs)})" if prereqs else " (No prerequisite)"
                    print(f"  Semester Stage {step}: {course}{prereq_str}")

        elif choice == "13":
            print("\n--- Graph: Peer Mentorship & Study Circles ---")
            print("Demonstrating BFS (Shortest Mentorship Path) and DFS (Study Group Cluster)")
            print("Available Peers in Network:")
            print("  Aarav Sharma, Ananya Iyer, Diya Patel, Pooja Reddy, Rohan Verma, Kabir Mehta, Vikram Joshi")
            p1 = input("\nEnter starting student name: ").strip()
            p2 = input("Enter target student name to find connection: ").strip()

            path = manager.peer_network.bfs_shortest_path(p1, p2)
            if path:
                print(f"\n[BFS Shortest Mentorship Route]: {' -> '.join(path)} (Degrees of separation: {len(path)-1})")
            else:
                print(f"\n[BFS Result]: No connected peer pathway found between '{p1}' and '{p2}'.")

            cluster = manager.peer_network.dfs_explore(p1)
            print(f"[DFS Study Circle Cluster for {p1}]: {', '.join(cluster)}")

        elif choice == "14":
            print("\n--- Benchmark: Comparing Search Algorithms on Current Dataset ---")
            try:
                test_roll = int(input("Enter Roll Number to test search comparisons: ").strip())
                s_bst, bst_steps = manager.search_by_roll_bst(test_roll)
                s_bs, bs_steps = manager.search_by_roll_binary_search(test_roll)
                all_students = manager.student_list.to_array()
                s_lin, lin_steps = Searcher.linear_search_by_name(all_students, s_bst.name if s_bst else "XYZ")

                print_separator("-")
                print(f"{'Algorithm' :<25} | {'Complexity' :<15} | {'Steps Taken' :<12} | {'Found?' :<8}")
                print_separator("-")
                print(f"{'Binary Search Tree (BST)' :<25} | {'O(log n)' :<15} | {bst_steps :<12} | {str(s_bst is not None) :<8}")
                print(f"{'Binary Search (Sorted Array)' :<25} | {'O(log n)' :<15} | {bs_steps :<12} | {str(s_bs is not None) :<8}")
                print(f"{'Linear Search (Sequential)' :<25} | {'O(n)' :<15} | {lin_steps :<12} | {str(s_bst is not None) :<8}")
                print_separator("-")
            except Exception as e:
                print(f"[Error]: {e}")

        elif choice == "0":
            print("\nExiting Student Records & Result Manager. Goodbye!")
            sys.exit(0)

        else:
            print("[Warning]: Invalid selection! Please enter a number between 0 and 14.")

        input("\nPress [Enter] to return to main menu...")


if __name__ == "__main__":
    run_interactive_cli()
