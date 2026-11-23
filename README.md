# Student Records & Result Manager
> **Course:** Fundamentals of Data Structures & Algorithms (FDS / DSA)  
> **Topic:** Comprehensive Student Academic Record & Result Management System  
> **Key Concepts Covered:** Array, Doubly Linked List, Stack, Circular Queue, Binary Search Tree, Graph, Searching, Sorting

---

## 1. Project Overview & Objectives

In academic institutions, managing student examination results, grade distributions, prerequisite subject sequencing, and service requests (e.g., transcripts or grade revaluations) requires specialized data structures tailored for efficiency, dynamic sizing, and transactional safety.

This project implements an end-to-end **Student Records & Result Manager** from first principles without relying on third-party libraries or high-level built-in shortcut functions. Every single fundamental Data Structures & Algorithms (DSA) concept is integrated into a practical academic workflow.

---

## 2. Comprehensive DSA Mapping Table

| Data Structure / Algorithm | Practical Academic Feature in Project | Time Complexity | Space Complexity | Why This DSA is Used |
| :--- | :--- | :--- | :--- | :--- |
| **1. Array (Contiguous)** | Subject mark sheet `marks[5]` per student | Access: $O(1)$ | $O(1)$ | Fixed number of subjects per semester; cache-friendly contiguous access. |
| **2. Doubly Linked List** | Primary student record repository | Insertion: $O(1)$<br>Deletion: $O(n)$ | $O(n)$ | Dynamic student intake without resizing overhead; bidirectional traversal. |
| **3. Stack (LIFO)** | Transactional Undo system for edits & deletions | Push: $O(1)$<br>Pop: $O(1)$ | $O(k)$ history | Reverts recent mistakes (e.g., accidentally deleted student or wrong marks entry). |
| **4. Circular Queue (FIFO)** | Clearance & Transcript Request Pipeline | Enqueue: $O(1)$<br>Dequeue: $O(1)$ | $O(C)$ capacity | First-Come First-Served fairness for student document processing without index shifting. |
| **5. Tree (Binary Search Tree)** | Roll Number search index & In-order roll listing | Search: $O(\log n)$<br>Insert: $O(\log n)$ | $O(n)$ | Fast non-linear lookups; in-order traversal yields naturally sorted roll directory. |
| **6. Graph (DAG & Undirected)** | Prerequisite Course Curriculum & Peer Mentorship | Topo: $O(V + E)$<br>BFS: $O(V + E)$ | $O(V + E)$ | Kahn's TopoSort guarantees valid semester course sequences; BFS finds shortest mentoring paths. |
| **7. Sorting (Merge Sort)** | Official Merit Rank List generation | $O(n \log n)$ Guaranteed | $O(n)$ | **Stable sort**: ensures students with tied percentages maintain their original relative order. |
| **8. Sorting (Quick Sort)** | In-place Roll Number sorting for Binary Search & Toppers | $O(n \log n)$ Average | $O(\log n)$ call stack | Fast in-place partitioning with minimal memory footprint. |
| **9. Searching (Binary Search)** | Instant roll number verification on sorted arrays | $O(\log n)$ | $O(1)$ | Halves search space each step; ideal for static end-of-semester mark audits. |
| **10. Searching (Linear Search)** | Substring search by student name | $O(n)$ | $O(1)$ | Flexible search across partial names where ordering is unknown. |

---

## 3. System Architecture & Data Flow

```
                      +-----------------------------+
                      | Student Enters System / CLI |
                      +--------------+--------------+
                                     |
               +---------------------+---------------------+
               |                     |                     |
     [Data Mutations]       [Lookups & Analysis]    [Academic Workflow]
               |                     |                     |
     +---------v---------+ +---------v---------+ +---------v---------+
     | Doubly Linked List| | Binary Search Tree| | Circular Queue    |
     | (Primary Store)   | | (O(log n) Search) | | (Transcript FCFS) |
     +---------+---------+ +---------+---------+ +---------+---------+
               |                     |                     |
     +---------v---------+ +---------v---------+ +---------v---------+
     | Stack (LIFO)      | | Merge & Quick Sort| | Graph (DAG & Net) |
     | (Undo Manager)    | | (Rank & Toppers)  | | (TopoSort & BFS)  |
     +-------------------+ +-------------------+ +-------------------+
```

---

## 4. Key Functional Modules

### 4.1. Student Record Management (Array + Doubly Linked List)
- Stores student roll number, full name, 5 subject marks (stored in a fixed-size contiguous array), total score, percentage, and letter grade ($O, A+, A, B+, B, P, F$).
- Uses a **Doubly Linked List (`StudentDoublyLinkedList`)** so student records can be inserted at the tail in $O(1)$ time, deleted without array shifting, and traversed both forwards and backwards.

### 4.2. Transactional Undo History (Stack)
- Every time a record is added, deleted, or marks are modified, an `ActionSnapshot` is pushed onto the **Undo Stack**.
- If a faculty member or administrator makes a mistake, selecting **Option 5 (Undo)** pops the most recent action and automatically restores the previous state.

### 4.3. Clearance & Verification Processing (Circular Queue)
- Students apply for transcripts, grade revaluation, or bonafide certificates.
- Requests enter a fixed-size **Circular Queue** where `enqueue` and `dequeue` run in strictly $O(1)$ time without wasting space or shifting array elements.

### 4.4. Fast Retrieval via Binary Search Tree (BST)
- A secondary tree index is maintained on student roll numbers.
- Searching for a roll number runs in $O(\log n)$ comparisons rather than scanning every record sequentially.
- Performing an in-order traversal yields an ascending sequence of students by roll number.

### 4.5. Merit Rank List & Toppers Generation (Merge Sort & Quick Sort)
- **Merge Sort**: Used for the comprehensive Semester Rank List. Because Merge Sort is **stable**, students who obtain identical percentages retain their original input order.
- **Quick Sort**: Utilized to sort records in-place by roll number to prepare buffers for **Binary Search**, and to isolate the top $K$ academic awardees.

### 4.6. Prerequisite Pathway & Peer Mentorship (Graph)
- **Course Prerequisite DAG**: Represents courses (e.g., *Discrete Math* $\rightarrow$ *Data Structures* $\rightarrow$ *Algorithms* $\rightarrow$ *AI*). **Kahn's Algorithm (Topological Sort)** calculates the valid semester sequence and checks for circular curriculum deadlocks.
- **Peer Mentorship Network**: Uses **Breadth-First Search (BFS)** to find the shortest referral connection between two students and **Depth-First Search (DFS)** to discover isolated study clusters.

---

## 5. How to Run the Project

### Option A: Interactive Visual Web Dashboard (Recommended)
You can launch the complete visual web dashboard right in your browser:
```powershell
cd "C:\Users\samik\.gemini\antigravity\scratch\student-records-fds-project"
python server.py
```
This automatically opens `http://localhost:8080/dashboard.html` with:
- **Live Student Directory & Mark Sheets** (Array & Doubly Linked List)
- **Top 3 Podium & Merit Rank List** (Merge Sort $O(n \log n)$)
- **Interactive Binary Search Tree (BST) Canvas Visualizer** ($O(\log n)$ path tracing)
- **Circular Queue (FIFO) Slot Visualizer** (Transcript & Clearance processing)
- **Course Prerequisite DAG (Topological Sort)** & **Peer Mentorship Network (BFS)**
- **Algorithm Benchmark Lab** (BST Search vs. Binary Search vs. Linear Search)
- **Stack-based Undo Button** ($O(1)$ LIFO mutation recovery)

Alternatively, you can directly open [`dashboard.html`](file:///C:/Users/samik/.gemini/antigravity/scratch/student-records-fds-project/dashboard.html) in any web browser.

### Option B: Python 3 Interactive CLI Application
Navigate to the project directory and run:
```bash
python main.py
```

To run the automated verification test suite:
```bash
python test_suite.py
```

### Option B: Standard C++ Version (Dev-C++, Code::Blocks, VS Code, GCC)
The project includes a pure C++ implementation `student_manager.cpp`.
Compile with any standard C++ compiler:
```bash
g++ -std=c++11 -O2 student_manager.cpp -o student_manager
./student_manager
```

---

## 6. Viva-Voce Questions & Model Answers

**Q1: Why did you choose a Doubly Linked List over a dynamic array for student storage?**  
*Answer:* A Doubly Linked List permits $O(1)$ insertions at the tail and $O(1)$ node deletions once a node pointer is located, without the memory reallocation and element shifting required by dynamic arrays. Its bidirectional pointers also allow reverse traversal.

**Q2: Why is Merge Sort preferred over Quick Sort for generating the official rank list?**  
*Answer:* Merge Sort is a **stable** sorting algorithm with a guaranteed worst-case time complexity of $O(n \log n)$. Stability is crucial in academic grading to ensure that candidates with identical percentages preserve their original submission or registration seniority.

**Q3: How does the Undo feature use a Stack?**  
*Answer:* Stacks adhere to the Last-In, First-Out (LIFO) principle. By pushing an action snapshot (`action_type`, `before_state`, `after_state`) onto the stack during any write operation, an undo request simply pops the top element and applies the inverse mutation.

**Q4: How does Kahn's Algorithm for Topological Sort work in your course prerequisite graph?**  
*Answer:* Kahn's algorithm computes the in-degree (number of prerequisite dependencies) for every course vertex. Nodes with an in-degree of 0 are enqueued. As each node is dequeued, the in-degree of its adjacent courses is decremented. If all vertices are processed, a valid graduation sequence is produced; if not, a circular dependency cycle exists.
#   F D S _ C P  
 