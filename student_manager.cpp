/*
=============================================================================
Project Title : Student Records & Result Manager (FDS Mini Project)
Course        : Fundamentals of Data Structures (FDS / DSA)
Language      : C++ (C++11 or higher - GCC / Dev-C++ / Code::Blocks compatible)
=============================================================================
Data Structures & Algorithms Covered:
  1. ARRAY               : Subject marks array marks[5]
  2. DOUBLY LINKED LIST  : Dynamic student repository (Node* prev, next)
  3. STACK (LIFO)        : Undo system for record modifications (ActionStack)
  4. QUEUE (FIFO)        : Circular Queue for result clearance/transcripts
  5. TREE (BST)          : Binary Search Tree indexed on Roll No for O(log n) search
  6. GRAPH               : Prerequisite DAG (Topological Sort) & Peer Network (BFS, DFS)
  7. SEARCHING           : Binary Search (O(log n)) & Linear Search (O(n))
  8. SORTING             : Merge Sort (O(n log n)) & Quick Sort (O(n log n))
=============================================================================
*/

#include <iostream>
#include <iomanip>
#include <string>
#include <vector>
#include <queue>
#include <stack>
#include <algorithm>

using namespace std;

const int NUM_SUBJECTS = 5;
const string SUBJECT_NAMES[NUM_SUBJECTS] = {
    "Data Structures", "Digital Logic", "Discrete Math", "OOPs in C++", "Computer Org"
};

// =============================================================================
// 1. ARRAY & MODEL: Student Entity with Marks Array
// =============================================================================
struct Student {
    int rollNo;
    string name;
    float marks[NUM_SUBJECTS]; // Fixed-size Contiguous Array
    float total;
    float percentage;
    string grade;

    Student() : rollNo(0), name(""), total(0.0f), percentage(0.0f), grade("F") {
        for (int i = 0; i < NUM_SUBJECTS; ++i) marks[i] = 0.0f;
    }

    Student(int roll, string n, const float m[NUM_SUBJECTS]) {
        rollNo = roll;
        name = n;
        total = 0.0f;
        for (int i = 0; i < NUM_SUBJECTS; ++i) {
            marks[i] = m[i];
            total += m[i];
        }
        percentage = total / NUM_SUBJECTS;
        grade = calculateGrade(percentage);
    }

    static string calculateGrade(float p) {
        if (p >= 90.0f) return "O (Outstanding)";
        if (p >= 80.0f) return "A+ (Excellent)";
        if (p >= 70.0f) return "A (Very Good)";
        if (p >= 60.0f) return "B+ (Good)";
        if (p >= 50.0f) return "B (Above Average)";
        if (p >= 40.0f) return "P (Pass)";
        return "F (Fail)";
    }
};

// =============================================================================
// 2. DOUBLY LINKED LIST: Dynamic Student Records List
// =============================================================================
struct DLLNode {
    Student data;
    DLLNode* prev;
    DLLNode* next;
    DLLNode(Student s) : data(s), prev(nullptr), next(nullptr) {}
};

class StudentDoublyLinkedList {
public:
    DLLNode* head;
    DLLNode* tail;
    int size;

    StudentDoublyLinkedList() : head(nullptr), tail(nullptr), size(0) {}

    ~StudentDoublyLinkedList() {
        DLLNode* curr = head;
        while (curr) {
            DLLNode* temp = curr->next;
            delete curr;
            curr = temp;
        }
    }

    bool insertAtEnd(Student s) {
        if (findByRoll(s.rollNo) != nullptr) return false; // Duplicate check
        DLLNode* newNode = new DLLNode(s);
        if (!head) {
            head = tail = newNode;
        } else {
            tail->next = newNode;
            newNode->prev = tail;
            tail = newNode;
        }
        size++;
        return true;
    }

    Student* findByRoll(int rollNo) {
        DLLNode* curr = head;
        while (curr) {
            if (curr->data.rollNo == rollNo) return &(curr->data);
            curr = curr->next;
        }
        return nullptr;
    }

    bool deleteByRoll(int rollNo, Student& deletedStudent) {
        DLLNode* curr = head;
        while (curr) {
            if (curr->data.rollNo == rollNo) {
                deletedStudent = curr->data;
                if (curr->prev) curr->prev->next = curr->next;
                else head = curr->next;

                if (curr->next) curr->next->prev = curr->prev;
                else tail = curr->prev;

                delete curr;
                size--;
                return true;
            }
            curr = curr->next;
        }
        return false;
    }

    vector<Student> toVector() const {
        vector<Student> result;
        DLLNode* curr = head;
        while (curr) {
            result.push_back(curr->data);
            curr = curr->next;
        }
        return result;
    }
};

// =============================================================================
// 3. STACK: LIFO Undo System
// =============================================================================
enum ActionType { ACT_INSERT, ACT_DELETE, ACT_UPDATE };

struct ActionSnapshot {
    ActionType type;
    Student before;
    Student after;
};

class UndoStack {
private:
    vector<ActionSnapshot> stackData;
    size_t capacity;
public:
    UndoStack(size_t cap = 30) : capacity(cap) {}

    void push(ActionSnapshot act) {
        if (stackData.size() >= capacity) {
            stackData.erase(stackData.begin()); // Evict oldest
        }
        stackData.push_back(act);
    }

    bool pop(ActionSnapshot& act) {
        if (stackData.empty()) return false;
        act = stackData.back();
        stackData.pop_back();
        return true;
    }

    bool isEmpty() const { return stackData.empty(); }
    size_t size() const { return stackData.size(); }
};

// =============================================================================
// 4. QUEUE: Circular Queue for Clearance / Verification Requests
// =============================================================================
struct ClearanceRequest {
    int reqId;
    int rollNo;
    string reqType;
};

class CircularQueue {
private:
    ClearanceRequest* arr;
    int front;
    int rear;
    int count;
    int capacity;
public:
    CircularQueue(int cap = 15) : capacity(cap), front(-1), rear(-1), count(0) {
        arr = new ClearanceRequest[capacity];
    }
    ~CircularQueue() { delete[] arr; }

    bool isFull() const { return count == capacity; }
    bool isEmpty() const { return count == 0; }

    bool enqueue(ClearanceRequest req) {
        if (isFull()) return false;
        if (front == -1) front = rear = 0;
        else rear = (rear + 1) % capacity;
        arr[rear] = req;
        count++;
        return true;
    }

    bool dequeue(ClearanceRequest& req) {
        if (isEmpty()) return false;
        req = arr[front];
        if (front == rear) front = rear = -1;
        else front = (front + 1) % capacity;
        count--;
        return true;
    }

    vector<ClearanceRequest> getAll() const {
        vector<ClearanceRequest> res;
        if (isEmpty()) return res;
        int idx = front;
        for (int i = 0; i < count; ++i) {
            res.push_back(arr[idx]);
            idx = (idx + 1) % capacity;
        }
        return res;
    }
};

// =============================================================================
// 5. TREE: Binary Search Tree (BST) for O(log n) Roll No Lookup
// =============================================================================
struct BSTNode {
    Student data;
    BSTNode* left;
    BSTNode* right;
    BSTNode(Student s) : data(s), left(nullptr), right(nullptr) {}
};

class StudentBST {
private:
    BSTNode* root;

    BSTNode* insertHelper(BSTNode* node, const Student& s) {
        if (!node) return new BSTNode(s);
        if (s.rollNo < node->data.rollNo) node->left = insertHelper(node->left, s);
        else if (s.rollNo > node->data.rollNo) node->right = insertHelper(node->right, s);
        else node->data = s; // Update
        return node;
    }

    void inorderHelper(BSTNode* node, vector<Student>& res) const {
        if (!node) return;
        inorderHelper(node->left, res);
        res.push_back(node->data);
        inorderHelper(node->right, res);
    }

    void clearTree(BSTNode* node) {
        if (!node) return;
        clearTree(node->left);
        clearTree(node->right);
        delete node;
    }
public:
    StudentBST() : root(nullptr) {}
    ~StudentBST() { clearTree(root); }

    void insert(const Student& s) { root = insertHelper(root, s); }

    bool search(int rollNo, Student& result, int& steps) const {
        BSTNode* curr = root;
        steps = 0;
        while (curr) {
            steps++;
            if (curr->data.rollNo == rollNo) {
                result = curr->data;
                return true;
            } else if (rollNo < curr->data.rollNo) {
                curr = curr->left;
            } else {
                curr = curr->right;
            }
        }
        return false;
    }

    vector<Student> inorder() const {
        vector<Student> res;
        inorderHelper(root, res);
        return res;
    }

    void rebuild(const vector<Student>& students) {
        clearTree(root);
        root = nullptr;
        for (const auto& s : students) insert(s);
    }
};

// =============================================================================
// 6. GRAPH: Prerequisite DAG (Topological Sort) & Peer Network (BFS/DFS)
// =============================================================================
class AcademicGraph {
public:
    vector<string> vertices;
    vector<vector<int>> adjList;
    vector<int> inDegree;

    int getVertexIndex(const string& name) {
        for (size_t i = 0; i < vertices.size(); ++i) {
            if (vertices[i] == name) return (int)i;
        }
        vertices.push_back(name);
        adjList.push_back(vector<int>());
        inDegree.push_back(0);
        return (int)vertices.size() - 1;
    }

    void addDirectedEdge(const string& u, const string& v) {
        int uIdx = getVertexIndex(u);
        int vIdx = getVertexIndex(v);
        adjList[uIdx].push_back(vIdx);
        inDegree[vIdx]++;
    }

    void addUndirectedEdge(const string& u, const string& v) {
        int uIdx = getVertexIndex(u);
        int vIdx = getVertexIndex(v);
        adjList[uIdx].push_back(vIdx);
        adjList[vIdx].push_back(uIdx);
    }

    bool topologicalSort(vector<string>& order) const {
        int n = (int)vertices.size();
        vector<int> inDeg = inDegree;
        queue<int> q;
        for (int i = 0; i < n; ++i) {
            if (inDeg[i] == 0) q.push(i);
        }
        order.clear();
        while (!q.empty()) {
            int u = q.front();
            q.pop();
            order.push_back(vertices[u]);
            for (int v : adjList[u]) {
                if (--inDeg[v] == 0) q.push(v);
            }
        }
        return order.size() == vertices.size(); // true if no cycle
    }

    vector<string> bfsShortestPath(const string& start, const string& target) {
        vector<string> path;
        int sIdx = -1, tIdx = -1;
        for (size_t i = 0; i < vertices.size(); ++i) {
            if (vertices[i] == start) sIdx = (int)i;
            if (vertices[i] == target) tIdx = (int)i;
        }
        if (sIdx == -1 || tIdx == -1) return path;

        int n = (int)vertices.size();
        vector<bool> visited(n, false);
        vector<int> parent(n, -1);
        queue<int> q;

        visited[sIdx] = true;
        q.push(sIdx);

        bool found = false;
        while (!q.empty()) {
            int curr = q.front();
            q.pop();
            if (curr == tIdx) { found = true; break; }
            for (int neighbor : adjList[curr]) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    parent[neighbor] = curr;
                    q.push(neighbor);
                }
            }
        }
        if (found) {
            int curr = tIdx;
            while (curr != -1) {
                path.push_back(vertices[curr]);
                curr = parent[curr];
            }
            reverse(path.begin(), path.end());
        }
        return path;
    }
};

// =============================================================================
// 7 & 8. SORTING & SEARCHING ALGORITHMS
// =============================================================================
class AlgorithmSuite {
public:
    // Merge Sort for Merit List (Descending by Percentage)
    static void merge(vector<Student>& arr, int left, int mid, int right) {
        int n1 = mid - left + 1;
        int n2 = right - mid;
        vector<Student> L(n1), R(n2);
        for (int i = 0; i < n1; ++i) L[i] = arr[left + i];
        for (int j = 0; j < n2; ++j) R[j] = arr[mid + 1 + j];

        int i = 0, j = 0, k = left;
        while (i < n1 && j < n2) {
            if (L[i].percentage >= R[j].percentage) arr[k++] = L[i++];
            else arr[k++] = R[j++];
        }
        while (i < n1) arr[k++] = L[i++];
        while (j < n2) arr[k++] = R[j++];
    }

    static void mergeSort(vector<Student>& arr, int left, int right) {
        if (left < right) {
            int mid = left + (right - left) / 2;
            mergeSort(arr, left, mid);
            mergeSort(arr, mid + 1, right);
            merge(arr, left, mid, right);
        }
    }

    // Quick Sort (Ascending by Roll Number)
    static int partition(vector<Student>& arr, int low, int high) {
        int pivot = arr[high].rollNo;
        int i = low - 1;
        for (int j = low; j < high; ++j) {
            if (arr[j].rollNo <= pivot) {
                i++;
                swap(arr[i], arr[j]);
            }
        }
        swap(arr[i + 1], arr[high]);
        return i + 1;
    }

    static void quickSort(vector<Student>& arr, int low, int high) {
        if (low < high) {
            int pi = partition(arr, low, high);
            quickSort(arr, low, pi - 1);
            quickSort(arr, pi + 1, high);
        }
    }

    // Binary Search on Roll Number
    static int binarySearch(const vector<Student>& arr, int targetRoll, int& steps) {
        int low = 0, high = (int)arr.size() - 1;
        steps = 0;
        while (low <= high) {
            steps++;
            int mid = low + (high - low) / 2;
            if (arr[mid].rollNo == targetRoll) return mid;
            if (arr[mid].rollNo < targetRoll) low = mid + 1;
            else high = mid - 1;
        }
        return -1;
    }

    // Linear Search by Name Substring
    static vector<Student> linearSearchByName(const vector<Student>& arr, const string& query, int& steps) {
        vector<Student> matches;
        steps = 0;
        for (const auto& s : arr) {
            steps++;
            if (s.name.find(query) != string::npos) {
                matches.push_back(s);
            }
        }
        return matches;
    }
};

// =============================================================================
// CLI CONTROLLER & MAIN DRIVER
// =============================================================================
void printTable(const vector<Student>& list, string title, bool showRank = false) {
    cout << "\n===============================================================================\n";
    cout << " " << title << " (Count: " << list.size() << ")\n";
    cout << "===============================================================================\n";
    cout << left << setw(6) << (showRank ? "Rank" : "No.")
         << " | " << setw(6) << "Roll"
         << " | " << setw(18) << "Name"
         << " | " << setw(7) << "Total"
         << " | " << setw(7) << "%"
         << " | " << setw(16) << "Grade" << "\n";
    cout << "-------------------------------------------------------------------------------\n";
    for (size_t i = 0; i < list.size(); ++i) {
        string tag = "#" + to_string(i + 1);
        cout << left << setw(6) << tag
             << " | " << setw(6) << list[i].rollNo
             << " | " << setw(18) << list[i].name
             << " | " << setw(7) << fixed << setprecision(1) << list[i].total
             << " | " << setw(7) << fixed << setprecision(2) << list[i].percentage
             << " | " << setw(16) << list[i].grade << "\n";
    }
    cout << "===============================================================================\n";
}

int main() {
    StudentDoublyLinkedList studentList;
    StudentBST bst;
    UndoStack undoStack;
    CircularQueue reqQueue(15);
    AcademicGraph prereqGraph;
    AcademicGraph peerGraph;
    int nextReqId = 201;

    // Seed Courses DAG
    prereqGraph.addDirectedEdge("Digital Logic", "Computer Org");
    prereqGraph.addDirectedEdge("Discrete Math", "Data Structures");
    prereqGraph.addDirectedEdge("OOPs in C++", "Data Structures");
    prereqGraph.addDirectedEdge("Data Structures", "Algorithms");
    prereqGraph.addDirectedEdge("Computer Org", "Operating Systems");

    // Seed Initial Students (10 students)
    float m1[5] = {82.0f, 88.0f, 76.5f, 90.0f, 84.0f}; studentList.insertAtEnd(Student(101, "Rahul Patil", m1));
    float m2[5] = {92.0f, 95.0f, 90.0f, 96.0f, 94.0f}; studentList.insertAtEnd(Student(102, "Priya Sharma", m2));
    float m3[5] = {70.0f, 68.0f, 74.0f, 65.0f, 72.0f}; studentList.insertAtEnd(Student(103, "Amit Verma", m3));
    float m4[5] = {85.0f, 89.0f, 82.0f, 88.0f, 86.0f}; studentList.insertAtEnd(Student(104, "Snehal Deshmukh", m4));
    float m5[5] = {75.0f, 80.0f, 78.0f, 82.0f, 79.0f}; studentList.insertAtEnd(Student(105, "Aryan Gupta", m5));
    float m6[5] = {58.0f, 62.0f, 35.0f, 60.0f, 58.0f}; studentList.insertAtEnd(Student(106, "Tanvi Kulkarni", m6));
    float m7[5] = {88.0f, 90.0f, 85.0f, 92.0f, 89.0f}; studentList.insertAtEnd(Student(107, "Devendra Joshi", m7));
    float m8[5] = {36.0f, 50.0f, 45.0f, 48.0f, 38.0f}; studentList.insertAtEnd(Student(108, "Riya Shah", m8));
    float m9[5] = {89.0f, 93.0f, 88.0f, 94.0f, 91.0f}; studentList.insertAtEnd(Student(109, "Siddharth Nair", m9));
    float m10[5] = {64.0f, 68.0f, 66.0f, 70.0f, 65.0f}; studentList.insertAtEnd(Student(110, "Aniket Shinde", m10));

    bst.rebuild(studentList.toVector());

    // Peer Mentorship Network
    peerGraph.addUndirectedEdge("Aarav Sharma", "Ananya Iyer");
    peerGraph.addUndirectedEdge("Ananya Iyer", "Diya Patel");
    peerGraph.addUndirectedEdge("Diya Patel", "Pooja Reddy");
    peerGraph.addUndirectedEdge("Rohan Verma", "Kabir Mehta");

    int choice = -1;
    while (choice != 0) {
        cout << "\n===============================================================================\n";
        cout << "       STUDENT RECORDS & RESULT MANAGER (C++ FDS MINI PROJECT)                \n";
        cout << "===============================================================================\n";
        cout << " 1. [ARRAY & LINKED LIST] Display All Student Records\n";
        cout << " 2. [LINKED LIST & BST]   Add New Student Record\n";
        cout << " 3. [LINKED LIST & STACK] Delete Student Record (Supports Undo)\n";
        cout << " 4. [STACK]               Undo Last Operation (LIFO Stack)\n";
        cout << " 5. [TREE (BST)]          Search Student by Roll Number (O(log n))\n";
        cout << " 6. [ARRAY & BINARY SRCH] Search Student by Roll Number (Binary Search)\n";
        cout << " 7. [LINEAR SEARCH]       Search Student by Name (O(n))\n";
        cout << " 8. [MERGE SORT]          Generate Merit Rank List (O(n log n))\n";
        cout << " 9. [QUICK SORT]          View Top Academic Toppers\n";
        cout << "10. [CIRCULAR QUEUE]      Clearance / Transcript Request Pipeline\n";
        cout << "11. [GRAPH - TOPO SORT]   Course Prerequisite Graduation Pathway\n";
        cout << "12. [GRAPH - BFS]         Find Shortest Peer Mentorship Pathway\n";
        cout << " 0. Exit System\n";
        cout << "===============================================================================\n";
        cout << "Enter choice (0-12): ";
        if (!(cin >> choice)) {
            cin.clear();
            cin.ignore(1000, '\n');
            continue;
        }

        switch (choice) {
            case 1: {
                vector<Student> all = studentList.toVector();
                printTable(all, "All Registered Students");
                break;
            }
            case 2: {
                int roll; string name; float m[NUM_SUBJECTS];
                cout << "Enter Roll Number: "; cin >> roll;
                cout << "Enter Student Full Name: "; cin.ignore(); getline(cin, name);
                cout << "Enter marks (0-100) for 5 subjects:\n";
                for (int i = 0; i < NUM_SUBJECTS; ++i) {
                    cout << "  " << SUBJECT_NAMES[i] << ": ";
                    cin >> m[i];
                }
                Student newS(roll, name, m);
                if (studentList.insertAtEnd(newS)) {
                    bst.insert(newS);
                    ActionSnapshot snap; snap.type = ACT_INSERT; snap.after = newS;
                    undoStack.push(snap);
                    cout << "[Success]: Student added successfully.\n";
                } else {
                    cout << "[Error]: Roll number already exists!\n";
                }
                break;
            }
            case 3: {
                int roll; cout << "Enter Roll Number to delete: "; cin >> roll;
                Student deletedS;
                if (studentList.deleteByRoll(roll, deletedS)) {
                    bst.rebuild(studentList.toVector());
                    ActionSnapshot snap; snap.type = ACT_DELETE; snap.before = deletedS;
                    undoStack.push(snap);
                    cout << "[Success]: Removed " << deletedS.name << " (Roll " << roll << "). Undo is available.\n";
                } else {
                    cout << "[Error]: Roll number not found.\n";
                }
                break;
            }
            case 4: {
                ActionSnapshot snap;
                if (undoStack.pop(snap)) {
                    if (snap.type == ACT_INSERT) {
                        Student dummy;
                        studentList.deleteByRoll(snap.after.rollNo, dummy);
                        bst.rebuild(studentList.toVector());
                        cout << "[Undo Success]: Reverted insertion of " << snap.after.name << "\n";
                    } else if (snap.type == ACT_DELETE) {
                        studentList.insertAtEnd(snap.before);
                        bst.insert(snap.before);
                        cout << "[Undo Success]: Restored deleted student " << snap.before.name << "\n";
                    }
                } else {
                    cout << "[Info]: Undo stack is empty!\n";
                }
                break;
            }
            case 5: {
                int roll, steps; cout << "Enter Roll Number to search in BST: "; cin >> roll;
                Student res;
                if (bst.search(roll, res, steps)) {
                    cout << "[Found in BST in " << steps << " steps]: " << res.name << " | %: " << fixed << setprecision(2) << res.percentage << "% | Grade: " << res.grade << "\n";
                } else {
                    cout << "[Not Found in BST after " << steps << " steps].\n";
                }
                break;
            }
            case 6: {
                int roll, steps; cout << "Enter Roll Number for Binary Search: "; cin >> roll;
                vector<Student> arr = studentList.toVector();
                AlgorithmSuite::quickSort(arr, 0, (int)arr.size() - 1);
                int idx = AlgorithmSuite::binarySearch(arr, roll, steps);
                if (idx != -1) {
                    cout << "[Binary Search Found in " << steps << " steps]: " << arr[idx].name << " (Roll " << arr[idx].rollNo << ")\n";
                } else {
                    cout << "[Binary Search Not Found after " << steps << " steps].\n";
                }
                break;
            }
            case 7: {
                string q; cout << "Enter name or substring: "; cin.ignore(); getline(cin, q);
                int steps;
                vector<Student> matches = AlgorithmSuite::linearSearchByName(studentList.toVector(), q, steps);
                cout << "[Linear Search completed in " << steps << " steps]: Found " << matches.size() << " match(es).\n";
                if (!matches.empty()) printTable(matches, "Matches for '" + q + "'");
                break;
            }
            case 8: {
                vector<Student> rankList = studentList.toVector();
                if (!rankList.empty()) {
                    AlgorithmSuite::mergeSort(rankList, 0, (int)rankList.size() - 1);
                }
                printTable(rankList, "Merit Rank List (Merge Sort - Stable O(n log n))", true);
                break;
            }
            case 9: {
                int k; cout << "How many top rankers to view? (e.g. 3): "; cin >> k;
                vector<Student> rankList = studentList.toVector();
                if (!rankList.empty()) {
                    AlgorithmSuite::mergeSort(rankList, 0, (int)rankList.size() - 1);
                }
                if (k > (int)rankList.size()) k = (int)rankList.size();
                vector<Student> toppers(rankList.begin(), rankList.begin() + k);
                printTable(toppers, "Top " + to_string(k) + " Academic Toppers", true);
                break;
            }
            case 10: {
                cout << "1. Enqueue Request | 2. Dequeue (Process) Request | 3. View Queue: ";
                int qChoice; cin >> qChoice;
                if (qChoice == 1) {
                    int rRoll; string rType;
                    cout << "Enter Roll Number: "; cin >> rRoll;
                    cout << "Enter Request Type (e.g., Transcript, Reval): "; cin.ignore(); getline(cin, rType);
                    ClearanceRequest req = {nextReqId++, rRoll, rType};
                    if (reqQueue.enqueue(req)) cout << "[Queue]: Request #" << req.reqId << " enqueued.\n";
                    else cout << "[Queue Error]: Circular queue is full!\n";
                } else if (qChoice == 2) {
                    ClearanceRequest req;
                    if (reqQueue.dequeue(req)) cout << "[Queue Dequeue]: Processed Request #" << req.reqId << " for Roll " << req.rollNo << " [" << req.reqType << "]\n";
                    else cout << "[Queue Info]: Queue is empty.\n";
                } else if (qChoice == 3) {
                    auto allReqs = reqQueue.getAll();
                    cout << "Pending Requests (" << allReqs.size() << "):\n";
                    for (const auto& r : allReqs) cout << "  Req #" << r.reqId << " | Roll " << r.rollNo << " | " << r.reqType << "\n";
                }
                break;
            }
            case 11: {
                vector<string> order;
                if (prereqGraph.topologicalSort(order)) {
                    cout << "\nCurriculum Graduation Sequence (Topological Sort / Kahn's Algorithm):\n";
                    for (size_t i = 0; i < order.size(); ++i) {
                        cout << "  Stage " << (i + 1) << ": " << order[i] << "\n";
                    }
                } else {
                    cout << "[Cycle Warning]: Prerequisite cycle found!\n";
                }
                break;
            }
            case 12: {
                string s, t;
                cout << "Enter starting student: "; cin.ignore(); getline(cin, s);
                cout << "Enter target student: "; getline(cin, t);
                vector<string> path = peerGraph.bfsShortestPath(s, t);
                if (!path.empty()) {
                    cout << "[BFS Path]: ";
                    for (size_t i = 0; i < path.size(); ++i) {
                        cout << path[i] << (i + 1 < path.size() ? " -> " : "");
                    }
                    cout << "\n";
                } else {
                    cout << "[BFS]: No mentorship path between " << s << " and " << t << "\n";
                }
                break;
            }
            case 0:
                cout << "Exiting system. Have a great day!\n";
                break;
            default:
                cout << "Invalid choice! Enter 0-12.\n";
        }
    }
    return 0;
}
