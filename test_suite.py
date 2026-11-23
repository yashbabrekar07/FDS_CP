"""
Automated Test Verification for Student Records & Result Manager (FDS).
Validates:
  1. Array calculations
  2. Doubly Linked List operations
  3. Stack Undo mechanism
  4. Circular Queue FIFO behavior
  5. Binary Search Tree search & traversals
  6. Graph (Topological Sort, BFS, DFS)
  7. Merge Sort & Quick Sort
  8. Binary Search & Linear Search
"""

import sys
from main import (
    Student, MarksArray, StudentDoublyLinkedList, UndoStack, ActionSnapshot,
    CircularQueue, ClearanceRequest, StudentBST, AcademicGraph, Sorter, Searcher,
    StudentResultManager
)

def run_tests():
    print("==================================================")
    print(" Running FDS Verification Test Suite")
    print("==================================================")

    # 1. Array Test
    marks = MarksArray([80, 90, 85, 95, 100])
    assert marks.total() == 450.0, f"Expected total 450, got {marks.total()}"
    assert marks.percentage() == 90.0, f"Expected % 90, got {marks.percentage()}"
    print("[PASS] 1. Fixed Marks Array abstraction verified.")

    # 2. Doubly Linked List
    dll = StudentDoublyLinkedList()
    s1 = Student(1, "Alice", [90, 90, 90, 90, 90])
    s2 = Student(2, "Bob", [80, 80, 80, 80, 80])
    assert dll.insert_at_end(s1) is True
    assert dll.insert_at_end(s2) is True
    assert dll.insert_at_end(s1) is False # Duplicate roll
    assert dll.size == 2
    assert dll.find_by_roll(2).name == "Bob"
    deleted = dll.delete_by_roll(1)
    assert deleted.roll_no == 1
    assert dll.size == 1
    print("[PASS] 2. Doubly Linked List (Insert, Delete, Search) verified.")

    # 3. Stack Test (Undo)
    stack = UndoStack(capacity=5)
    stack.push(ActionSnapshot("INSERT", None, s1))
    assert not stack.is_empty()
    assert stack.peek().action_type == "INSERT"
    popped = stack.pop()
    assert popped.action_type == "INSERT"
    assert stack.is_empty()
    print("[PASS] 3. Stack (LIFO push/pop/peek) verified.")

    # 4. Circular Queue Test
    q = CircularQueue(capacity=3)
    assert q.is_empty()
    assert q.enqueue(ClearanceRequest(1, 101, "Transcript"))
    assert q.enqueue(ClearanceRequest(2, 102, "Grade Reval"))
    assert q.enqueue(ClearanceRequest(3, 103, "Bonafide"))
    assert q.is_full()
    assert not q.enqueue(ClearanceRequest(4, 104, "Overflow"))
    deq1 = q.dequeue()
    assert deq1.request_id == 1
    assert q.enqueue(ClearanceRequest(4, 104, "Circular Enqueue"))
    print("[PASS] 4. Circular Queue (FIFO wrap-around & clearance) verified.")

    # 5. Tree (BST) Test
    bst = StudentBST()
    students_data = [
        Student(50, "M", [70]*5),
        Student(20, "B", [60]*5),
        Student(80, "T", [90]*5),
        Student(10, "A", [50]*5),
        Student(30, "C", [65]*5)
    ]
    for s in students_data:
        bst.insert(s)
    found_s, steps = bst.search_by_roll(30)
    assert found_s is not None and found_s.name == "C"
    inorder = bst.inorder_traversal()
    inorder_rolls = [s.roll_no for s in inorder]
    assert inorder_rolls == [10, 20, 30, 50, 80], f"BST In-order failed: {inorder_rolls}"
    print("[PASS] 5. Binary Search Tree (O(log n) lookup & In-Order traversal) verified.")

    # 6. Graph Tests
    g = AcademicGraph()
    g.add_directed_edge("Math", "DSA")
    g.add_directed_edge("DSA", "Algo")
    g.add_directed_edge("Algo", "AI")
    topo, has_cycle = g.topological_sort()
    assert not has_cycle
    assert topo.index("Math") < topo.index("DSA") < topo.index("Algo") < topo.index("AI")

    # Peer BFS & DFS
    p_net = AcademicGraph()
    p_net.add_undirected_edge("A", "B")
    p_net.add_undirected_edge("B", "C")
    p_net.add_undirected_edge("C", "D")
    p_net.add_undirected_edge("X", "Y")
    path = p_net.bfs_shortest_path("A", "D")
    assert path == ["A", "B", "C", "D"]
    cluster = p_net.dfs_explore("A")
    assert set(cluster) == {"A", "B", "C", "D"}
    assert p_net.bfs_shortest_path("A", "Y") is None
    print("[PASS] 6. Graph (Topological Sort, BFS Shortest Path, DFS Exploration) verified.")

    # 7. Sorting Tests (Merge Sort & Quick Sort)
    s_sort_test = [
        Student(101, "Low", [50]*5),     # 50%
        Student(102, "Top", [95]*5),     # 95%
        Student(103, "Mid", [75]*5),     # 75%
        Student(104, "High", [88]*5)     # 88%
    ]
    ranked = Sorter.merge_sort_by_percentage(s_sort_test, descending=True)
    assert ranked[0].name == "Top" and ranked[1].name == "High" and ranked[-1].name == "Low"

    # Quick Sort
    quick_test = list(s_sort_test)
    Sorter.quick_sort_by_roll(quick_test, 0, len(quick_test) - 1)
    assert [s.roll_no for s in quick_test] == [101, 102, 103, 104]
    print("[PASS] 7. Sorting (Merge Sort descending ranks & Quick Sort ascending rolls) verified.")

    # 8. Searching Tests (Binary Search & Linear Search)
    s_found, steps = Searcher.binary_search_by_roll(quick_test, 103)
    assert s_found is not None and s_found.roll_no == 103
    s_not_found, _ = Searcher.binary_search_by_roll(quick_test, 999)
    assert s_not_found is None

    matches, _ = Searcher.linear_search_by_name(quick_test, "Hig")
    assert len(matches) == 1 and matches[0].name == "High"
    print("[PASS] 8. Searching (Binary Search O(log n) & Linear Search O(n)) verified.")

    # 9. Manager & Undo Integration Test
    mgr = StudentResultManager()
    init_count = mgr.student_list.size
    mgr.add_student(999, "TestStudent", [90]*5)
    assert mgr.student_list.size == init_count + 1
    # Undo addition
    mgr.undo_last_action()
    assert mgr.student_list.size == init_count
    assert mgr.student_list.find_by_roll(999) is None
    print("[PASS] 9. Manager Transactional Undo integration verified.")

    print("\n>>> ALL 9 FDS VERIFICATION TEST SUITES PASSED PERFECTLY! <<<")

if __name__ == "__main__":
    run_tests()
