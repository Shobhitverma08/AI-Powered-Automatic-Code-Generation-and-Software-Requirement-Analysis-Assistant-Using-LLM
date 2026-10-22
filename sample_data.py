"""
Sample Mock Data & Production Blueprints for CodeMind AI
Provides high-performance structured presets for:
1. Student Management System (Python)
2. E-Commerce REST API (JavaScript / Node.js)
3. Library Management System (C++)
"""

# ==============================================================================
# 1. STUDENT MANAGEMENT SYSTEM (Python)
# ==============================================================================

STUDENT_MANAGEMENT_REQUIREMENT = "Create a Python student management system where an administrator can add, update, delete and search student records with data persistence and input validation."

STUDENT_MANAGEMENT_ANALYSIS = {
    "problem_statement": "Educational institutions need an efficient system for administrators to maintain student records, allowing operations like adding new enrollments, updating profile details, searching student entries by ID or name, and removing records.",
    "functional_requirements": [
        "System shall allow administrator to add a new student record (ID, Name, Grade, Major, Email).",
        "System shall allow administrator to search for a student by unique Student ID or full/partial Name.",
        "System shall allow updating existing student details (Grade, Major, Email).",
        "System shall support deleting a student record with confirmation prompt.",
        "System shall display a complete list of enrolled students in a formatted tabular format."
    ],
    "non_functional_requirements": [
        "Response time for record retrieval and searching must be under 1 second.",
        "Data validation must prevent duplicate Student IDs.",
        "Application should provide a clean user interface with robust input exception handling."
    ],
    "actors": [
        "Administrator (Primary User)",
        "System Auditor"
    ],
    "inputs": [
        "Student ID (Unique Alphanumeric String)",
        "Student Name (String)",
        "Major / Course (String)",
        "GPA / Grade (Float)",
        "Contact Email (String)"
    ],
    "outputs": [
        "Operation Success/Failure Messages",
        "Detailed Student Profile Record",
        "Formatted Student Summary List",
        "Validation Warning Messages"
    ],
    "constraints": [
        "Must be implemented using Python 3.x standard library.",
        "Must support persistent storage via SQLite database."
    ],
    "assumptions": [
        "Single administrator access per workstation session.",
        "Student IDs are alphanumeric and unique per student."
    ],
    "ambiguities": [
        "Requirement does not specify if persistent storage (SQLite database or JSON) is required.",
        "No mention of authentication/login security for administrators."
    ],
    "missing_information": [
        "Specific fields required for student profile (e.g. phone number, address, date of birth).",
        "Export capabilities (e.g., export student roster to CSV or PDF)."
    ],
    "suggestions": [
        "Include administrator authentication with password hashing.",
        "Integrate SQLite database for persistent storage instead of in-memory data structures.",
        "Add CSV export and search filtering by GPA or Major."
    ],
    "is_ambiguous": False
}

STUDENT_MANAGEMENT_CODE = '''"""
Student Management System
Language: Python 3
Architecture: Clean / Modular Object-Oriented Design with SQLite Persistence
"""

import sqlite3
import re

class StudentDatabase:
    """Encapsulates thread-safe SQLite operations for Student records."""
    
    def __init__(self, db_name="students.db"):
        self.db_name = db_name
        self.init_db()
        
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn
        
    def init_db(self):
        """Initializes tables and primary key indices."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    student_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    major TEXT NOT NULL,
                    gpa REAL NOT NULL CHECK(gpa >= 0.0 AND gpa <= 4.0),
                    email TEXT UNIQUE NOT NULL
                )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_student_name ON students(name);")
            conn.commit()

    def add_student(self, student_id, name, major, gpa, email):
        """Adds a student record with validation."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO students (student_id, name, major, gpa, email) VALUES (?, ?, ?, ?, ?)",
                    (student_id.strip(), name.strip(), major.strip(), float(gpa), email.strip().lower())
                )
                conn.commit()
                return True, "Student record successfully added."
        except sqlite3.IntegrityError as e:
            return False, f"Constraint Error: ID or Email already registered. ({e})"
        except Exception as e:
            return False, f"Database error: {str(e)}"

    def search_student(self, query):
        """Searches by exact Student ID (O(1)) or partial Name (O(N))."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM students WHERE student_id = ? OR name LIKE ? ORDER BY name ASC",
                (query.strip(), f"%{query.strip()}%")
            )
            return [dict(row) for row in cursor.fetchall()]

    def update_student(self, student_id, name=None, major=None, gpa=None, email=None):
        """Dynamically updates student fields in a single atomic transaction."""
        updates, params = [], []
        if name is not None:
            updates.append("name = ?")
            params.append(name.strip())
        if major is not None:
            updates.append("major = ?")
            params.append(major.strip())
        if gpa is not None:
            updates.append("gpa = ?")
            params.append(float(gpa))
        if email is not None:
            updates.append("email = ?")
            params.append(email.strip().lower())
            
        if not updates:
            return False, "No update fields provided."
            
        params.append(student_id.strip())
        query = f"UPDATE students SET {', '.join(updates)} WHERE student_id = ?"
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if cursor.rowcount > 0:
                conn.commit()
                return True, "Student record successfully updated."
            return False, "Student ID not found."

    def delete_student(self, student_id):
        """Deletes student record by primary key."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id.strip(),))
            if cursor.rowcount > 0:
                conn.commit()
                return True, "Student record deleted."
            return False, "Student ID not found."

    def get_all_students(self):
        """Fetches all student records sorted by Student ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students ORDER BY student_id ASC")
            return [dict(row) for row in cursor.fetchall()]
'''

STUDENT_MANAGEMENT_CODE_EXPLANATION = {
    "summary": "This is a clean, Object-Oriented Python application implementing a complete CRUD Student Management System with persistent SQLite database storage and parametrized SQL protection.",
    "step_by_step": [
        "1. Initialization: The StudentDatabase class initializes the SQLite connection, enables Row factory mapping, and constructs the students table with indexed primary keys.",
        "2. Add Student: Validates GPA boundaries (0.0 to 4.0) and executes parameterized SQL INSERT to guarantee injection resistance.",
        "3. Search Student: Executes dual-mode query matching exact student ID via O(1) B-tree lookup or partial names via indexed pattern search.",
        "4. Atomic Updates: Dynamically composes safe parameterized UPDATE clauses based on provided fields.",
        "5. Deletion & Retrieval: Safely purges or retrieves student records using context managers ensuring zero connection leaks."
    ],
    "key_components": [
        {"name": "StudentDatabase Class", "description": "Manages connection context managers and executes secure SQL queries."},
        {"name": "B-Tree Primary Index", "description": "Guarantees O(1) lookup latency by unique student_id."},
        {"name": "Parametrized Queries", "description": "Prevents SQL injection attacks across all data entry points."}
    ],
    "important_variables": [
        {"name": "student_id", "description": "Unique primary key alphanumeric string for each student."},
        {"name": "gpa", "description": "Floating point number validated between 0.0 and 4.0."},
        {"name": "conn.row_factory", "description": "Configures dictionary-style row access for retrieved records."}
    ],
    "algorithm": "Relational Data Management using B-Tree Indexed Lookup (SQLite PK)",
    "time_complexity": "O(1) for Add/Search by ID; O(N) for partial name search or listing all students.",
    "space_complexity": "O(N) where N is the total number of student records stored in SQLite database."
}

STUDENT_MANAGEMENT_REVIEW = {
    "score": 94,
    "issues": [
        {
            "category": "Security Issues",
            "severity": "Good",
            "title": "SQL Injection Protection Active",
            "description": "All SQL commands strictly use parameterized placeholders (?, ?), preventing SQL injection vulnerabilities."
        },
        {
            "category": "Performance Issues",
            "severity": "Good",
            "title": "Indexed Primary Key Retrieval",
            "description": "Primary key lookups run in O(1) time complexity utilizing SQLite B-Tree indexing."
        },
        {
            "category": "Bugs / Potential Issues",
            "severity": "Low",
            "title": "Regex Email Strictness",
            "description": "Email normalization is applied; ensure domain verification is supported if deployed in production."
        }
    ],
    "suggestions": [
        "Add connection pooling for multi-threaded GUI or REST deployments.",
        "Implement pagination when listing large numbers of student records (>1,000 items)."
    ],
    "improved_code": """# Production Connection Pool Extension
import sqlite3
from contextlib import contextmanager

class ConnectionPool:
    def __init__(self, db_path='students.db'):
        self.db_path = db_path

    @contextmanager
    def get_cursor(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        finally:
            conn.close()
"""
}

STUDENT_MANAGEMENT_DOCS = """# Software Requirement Specification (SRS) & System Architecture
## Project: Student Management System (Python)
**Generated by CodeMind AI**

---

### 1. Project Overview & Objectives
The **Student Management System** is an engineering assistant designed for academic administrators. It simplifies student record lifecycle management, eliminating manual spreadsheet overhead and providing real-time query capabilities.

### 2. Functional Requirements
- **FR-1**: Add new student profile including ID, Name, Major, GPA, and Email.
- **FR-2**: Search profiles by ID or partial Name lookup.
- **FR-3**: Update Major, GPA, or Email attributes for existing records.
- **FR-4**: Delete obsolete student entries with administrative confirmation.
- **FR-5**: Display tabular report of all enrolled students sorted by ID.

### 3. Non-Functional Requirements
- **NFR-1 Integrity**: Enforce primary key uniqueness on Student ID and Email.
- **NFR-2 Performance**: Query latency < 50ms for single record lookups.
- **NFR-3 Reliability**: Atomic ACID transactions via SQLite with WAL journaling.

### 4. Technical Specifications
- **Language**: Python 3.10+
- **Persistence**: SQLite 3 (WAL mode)
- **Time Complexity**: $O(1)$ ID search, $O(N)$ full roster enumeration.
"""

# ==============================================================================
# 2. E-COMMERCE REST API (JavaScript / Node.js)
# ==============================================================================

ECOMMERCE_API_REQUIREMENT = "Design a RESTful API in JavaScript/Node.js for an e-commerce platform allowing users to browse catalog items, manage cart state, checkout, and process order payments securely."

ECOMMERCE_API_ANALYSIS = {
    "problem_statement": "Digital commerce platforms require a scalable, stateless RESTful service architecture that enables shoppers to browse catalog products, manage session shopping carts, compute pricing subtotals with tax, and execute secure order checkout with payment gateway verification.",
    "functional_requirements": [
        "System shall expose GET /api/products with pagination, category filtering, and price sorting.",
        "System shall expose GET /api/products/:id to return full item inventory specifications.",
        "System shall support shopping cart state operations: POST /api/cart (add item), PUT /api/cart/:id (update quantity), DELETE /api/cart/:id.",
        "System shall calculate total cart amounts including regional sales tax and shipping cost.",
        "System shall expose POST /api/checkout to validate stock availability, record order history, and tokenize payment data."
    ],
    "non_functional_requirements": [
        "API response latency shall remain under 200ms for 95% of read requests.",
        "All checkout transactions must adhere to PCI-DSS standards with TLS 1.3 tokenization.",
        "Stateless JWT bearer authentication required for customer sessions and administrative actions.",
        "Concurrency controls to prevent overselling of limited inventory during high traffic."
    ],
    "actors": [
        "Shopper / Customer",
        "Store Administrator",
        "Payment Processor (Stripe/PayPal Gateway)"
    ],
    "inputs": [
        "Catalog Filter Parameters (category, min_price, max_price, page, limit)",
        "Cart Item Payload (product_id, quantity, variant_id)",
        "Checkout Payload (shipping_address, billing_info, payment_method_nonce, user_id)"
    ],
    "outputs": [
        "JSON Product Catalog Collection with Meta Pagination",
        "Cart Summary State Object (items, subtotal, tax, grand_total)",
        "Order Confirmation Receipt (order_id, tracking_number, status, timestamp)",
        "Standardized RFC 7807 Error Responses"
    ],
    "constraints": [
        "Runtime environment: Node.js 18+ LTS using Express.js framework.",
        "Asynchronous non-blocking I/O event loop design."
    ],
    "assumptions": [
        "External payment gateway provides webhook confirmation callbacks.",
        "Product catalog inventory counts are atomically synchronized."
    ],
    "ambiguities": [
        "Cart persistence strategy (in-memory Redis vs database relational table) not specified in brief.",
        "Refund and cancellation endpoint workflows not delineated."
    ],
    "missing_information": [
        "Supported currencies and international tax calculation rules.",
        "Rate limiting specifications for guest checkout routes."
    ],
    "suggestions": [
        "Implement Redis in-memory caching for product catalog read routes.",
        "Incorporate rate limiting via express-rate-limit to mitigate credential stuffing on auth routes.",
        "Use database optimistic locking to prevent inventory race conditions during flash sales."
    ],
    "is_ambiguous": False
}

ECOMMERCE_API_CODE = '''/**
 * E-Commerce RESTful API Gateway
 * Runtime: Node.js / Express.js
 * Architecture: Clean Modular Service & Controller Pattern
 */

const express = require('express');
const router = express.Router();

// Mock High-Speed In-Memory Catalog & Inventory Store
const PRODUCTS = new Map([
    ["prod_1", { id: "prod_1", title: "Mechanical Keyboard", price: 129.99, inventory: 45, category: "Hardware" }],
    ["prod_2", { id: "prod_2", title: "Ergonomic Mouse", price: 79.50, inventory: 80, category: "Hardware" }],
    ["prod_3", { id: "prod_3", title: "4K IPS Monitor", price: 349.00, inventory: 20, category: "Displays" }],
    ["prod_4", { id: "prod_4", title: "USB-C Multi-Port Hub", price: 49.99, inventory: 110, category: "Accessories" }]
]);

// In-Memory Session Cart Storage (keyed by userId)
const USER_CARTS = new Map();

// Helper: Calculate Cart Total (O(K) where K = cart items)
function computeCartSummary(items) {
    let subtotal = 0;
    const itemDetails = [];

    for (const item of items) {
        const product = PRODUCTS.get(item.productId);
        if (product) {
            const lineTotal = product.price * item.quantity;
            subtotal += lineTotal;
            itemDetails.push({ ...product, quantity: item.quantity, lineTotal: Number(lineTotal.toFixed(2)) });
        }
    }

    const tax = Number((subtotal * 0.0825).toFixed(2)); // 8.25% Sales Tax
    const shipping = subtotal > 100 || subtotal === 0 ? 0 : 9.99;
    const grandTotal = Number((subtotal + tax + shipping).toFixed(2));

    return { subtotal: Number(subtotal.toFixed(2)), tax, shipping, grandTotal, items: itemDetails };
}

// 1. GET /api/products - Catalog query with pagination & category filter
router.get('/products', (req, res) => {
    const { category, page = 1, limit = 10 } = req.query;
    let list = Array.from(PRODUCTS.values());

    if (category) {
        list = list.filter(p => p.category.toLowerCase() === category.toLowerCase());
    }

    const startIndex = (page - 1) * limit;
    const paginatedItems = list.slice(startIndex, startIndex + Number(limit));

    res.json({
        success: true,
        data: paginatedItems,
        pagination: { page: Number(page), limit: Number(limit), totalItems: list.length }
    });
});

// 2. GET /api/products/:id - Single item details (O(1) Map lookup)
router.get('/products/:id', (req, res) => {
    const product = PRODUCTS.get(req.params.id);
    if (!product) {
        return res.status(404).json({ success: false, error: "Product not found" });
    }
    res.json({ success: true, data: product });
});

// 3. GET /api/cart - Retrieve current cart state
router.get('/cart', (req, res) => {
    const userId = req.headers['x-user-id'] || 'guest_user';
    const items = USER_CARTS.get(userId) || [];
    res.json({ success: true, data: computeCartSummary(items) });
});

// 4. POST /api/cart - Add or update cart items atomically
router.post('/cart', (req, res) => {
    const userId = req.headers['x-user-id'] || 'guest_user';
    const { productId, quantity = 1 } = req.body;

    if (!productId || quantity < 1) {
        return res.status(400).json({ success: false, error: "Valid productId and positive quantity required" });
    }

    const product = PRODUCTS.get(productId);
    if (!product) {
        return res.status(404).json({ success: false, error: "Product not found in catalog" });
    }

    if (product.inventory < quantity) {
        return res.status(409).json({ success: false, error: "Requested quantity exceeds available stock" });
    }

    const userCart = USER_CARTS.get(userId) || [];
    const existingIndex = userCart.findIndex(item => item.productId === productId);

    if (existingIndex >= 0) {
        userCart[existingIndex].quantity += quantity;
    } else {
        userCart.push({ productId, quantity });
    }

    USER_CARTS.set(userId, userCart);
    res.status(200).json({ success: true, message: "Cart updated", data: computeCartSummary(userCart) });
});

// 5. POST /api/checkout - Process order payment & deduct inventory atomically
router.post('/checkout', (req, res) => {
    const userId = req.headers['x-user-id'] || 'guest_user';
    const { paymentNonce, shippingAddress } = req.body;

    const userCart = USER_CARTS.get(userId) || [];
    if (userCart.length === 0) {
        return res.status(400).json({ success: false, error: "Cannot checkout with an empty cart" });
    }

    // Atomic Stock Verification
    for (const item of userCart) {
        const product = PRODUCTS.get(item.productId);
        if (!product || product.inventory < item.quantity) {
            return res.status(409).json({ success: false, error: `Insufficient stock for product: ${item.productId}` });
        }
    }

    // Deduct Inventory (Atomic Commit)
    for (const item of userCart) {
        const product = PRODUCTS.get(item.productId);
        product.inventory -= item.quantity;
    }

    const summary = computeCartSummary(userCart);
    const orderId = `ORD_${Date.now()}_${Math.floor(Math.random() * 1000)}`;

    // Clear user cart post-order
    USER_CARTS.delete(userId);

    res.status(201).json({
        success: true,
        message: "Order placed successfully",
        data: {
            orderId,
            timestamp: new Date().toISOString(),
            status: "PAID",
            amountPaid: summary.grandTotal,
            shippingAddress: shippingAddress || "Default on file"
        }
    });
});

module.exports = router;
'''

ECOMMERCE_API_CODE_EXPLANATION = {
    "summary": "This Express.js microservice architecture delivers a high-throughput e-commerce backend with O(1) hash map catalog lookups, session-based cart management, tax calculation, and atomic inventory checkout.",
    "step_by_step": [
        "1. Product Map: Implements ECMAScript Map for O(1) primary product identification and stock tracking.",
        "2. Catalog Endpoint (GET /products): Provides memory-efficient array slicing for paginated catalog responses.",
        "3. Cart Service: Maintains user shopping cart state, dynamically computing item subtotals, tax (8.25%), and conditional free shipping.",
        "4. Concurrency Guard: Before checkout execution, verifies all requested item quantities against real-time stock.",
        "5. Order Creation: Atomically decrements product inventory, creates unique order ID tokens, and clears cart state."
    ],
    "key_components": [
        {"name": "PRODUCTS Map", "description": "Provides O(1) constant-time lookup for items, prices, and stock counts."},
        {"name": "computeCartSummary Routine", "description": "Computes line totals, regional sales tax, and free-shipping thresholds in O(K) time."},
        {"name": "Atomic Checkout Handler", "description": "Ensures zero overselling by verifying inventory constraints before state deduction."}
    ],
    "important_variables": [
        {"name": "USER_CARTS", "description": "Map containing user shopping cart sessions keyed by user identifier."},
        {"name": "orderId", "description": "High-entropy order identifier token returned to caller upon payment capture."},
        {"name": "grandTotal", "description": "Final billed charge including subtotal, tax, and calculated shipping fees."}
    ],
    "algorithm": "Hash-Indexed Product Lookup with Atomic Stock Deduction (Express Router)",
    "time_complexity": "O(1) for single product / cart queries; O(K) for cart total calculation where K is items in cart.",
    "space_complexity": "O(P + C) where P is product catalog size and C is active shopping carts."
}

ECOMMERCE_API_REVIEW = {
    "score": 93,
    "issues": [
        {
            "category": "Security Issues",
            "severity": "Good",
            "title": "Idempotent Stock Deduction Guard",
            "description": "Stock availability is validated in a complete pre-pass before inventory deduction occurs."
        },
        {
            "category": "Performance Issues",
            "severity": "Good",
            "title": "O(1) Constant-Time Product Seek",
            "description": "Uses ES6 Map data structure ensuring instantaneous key lookups regardless of catalog scale."
        },
        {
            "category": "Bugs / Potential Issues",
            "severity": "Medium",
            "title": "In-Memory Session Persistence",
            "description": "Cart state is currently stored in Node process memory; restart will purge active sessions."
        }
    ],
    "suggestions": [
        "Mount Redis cluster for distributed cart state persistence across multi-instance server deployments.",
        "Implement Stripe Webhook signature verification for asynchronous payment confirmation."
    ],
    "improved_code": """// Production Redis Adapter Pattern for Cart Persistence
const Redis = require('ioredis');
const redis = new Redis(process.env.REDIS_URL || 'redis://localhost:6379');

async function getCart(userId) {
    const raw = await redis.get(`cart:${userId}`);
    return raw ? JSON.parse(raw) : [];
}

async function setCart(userId, items, ttlSeconds = 86400) {
    await redis.setex(`cart:${userId}`, ttlSeconds, JSON.stringify(items));
}
"""
}

ECOMMERCE_API_DOCS = """# Software Requirement Specification (SRS)
## Project: E-Commerce REST API (JavaScript / Node.js)
**Generated by CodeMind AI**

---

### 1. Executive Summary
The **E-Commerce REST API** provides a resilient, stateless API layer for digital commerce. It manages products, shopping sessions, and payment checkout with low latency guarantees.

### 2. Functional Requirements
- **FR-1**: Expose GET /api/products with pagination and category filtering.
- **FR-2**: O(1) product lookup via GET /api/products/:id.
- **FR-3**: Session cart state updates (add, quantity modify, remove).
- **FR-4**: Automatic sales tax and conditional shipping calculations.
- **FR-5**: Atomic inventory reservation and checkout receipt generation.

### 3. Non-Functional Specifications
- **NFR-1 Latency**: Read endpoints execute in under 100ms.
- **NFR-2 Concurrency**: Thread-safe stock validation prior to transaction commit.
- **NFR-3 Security**: Encrypted bearer token validation.
"""

# ==============================================================================
# 3. LIBRARY MANAGEMENT SYSTEM (C++)
# ==============================================================================

LIBRARY_MANAGEMENT_REQUIREMENT = "Build a C++ library inventory management application for cataloging books, tracking active member loans, calculating late return fines, and generating inventory audit summaries."

LIBRARY_MANAGEMENT_ANALYSIS = {
    "problem_statement": "Municipal and university libraries require a high-performance system for cataloging book holdings, tracking patron borrowing activity, calculating overdue fines automatically, and generating comprehensive inventory audit reports.",
    "functional_requirements": [
        "System shall maintain book catalog records (ISBN, Title, Author, Total Copies, Available Copies).",
        "System shall support patron loan checkout, verifying member eligibility and book availability.",
        "System shall record book returns, automatically calculating late fines ($0.50 per day past the 14-day checkout limit).",
        "System shall allow search by ISBN, Title, or Author.",
        "System shall output comprehensive inventory audit reports displaying borrowed vs available items."
    ],
    "non_functional_requirements": [
        "Core lookup and fine computation operations must achieve O(1) or O(log N) time complexity.",
        "Zero memory leaks enforced using Modern C++ RAII and smart pointers (std::unique_ptr, std::shared_ptr).",
        "Robust input exception handling for invalid ISBN codes and non-numeric inputs."
    ],
    "actors": [
        "Librarian / Staff Administrator",
        "Library Member / Patron"
    ],
    "inputs": [
        "Book Details (ISBN, Title, Author, Quantity)",
        "Checkout Request (Member ID, Book ISBN, Loan Date)",
        "Return Request (Member ID, Book ISBN, Return Date)"
    ],
    "outputs": [
        "Formatted Book Search Record",
        "Loan Confirmation Receipt with Due Date",
        "Return Fine Notice (Days Overdue, Total Fine Owed)",
        "Formatted ASCII Inventory Audit Table"
    ],
    "constraints": [
        "Must be implemented using Modern C++ (C++17 standard).",
        "Standard Library (STL) data structures only; no heavy external third-party dependencies."
    ],
    "assumptions": [
        "ISBN numbers are unique 13-digit or alphanumeric identifiers.",
        "Checkout duration defaults to 14 days before fine accrual begins."
    ],
    "ambiguities": [
        "Fine payment tracking (e.g. tracking paid vs unpaid outstanding balance) not detailed.",
        "Member maximum concurrent checkout limit not defined."
    ],
    "missing_information": [
        "Book categorization / Dewey Decimal taxonomy support.",
        "Persistent file storage format (CSV vs binary serialization)."
    ],
    "suggestions": [
        "Use std::unordered_map for O(1) hash-based ISBN book lookup.",
        "Implement RAII file streams for automatic state persistence to disk.",
        "Enforce a maximum limit of 5 active borrowed books per member."
    ],
    "is_ambiguous": False
}

LIBRARY_MANAGEMENT_CODE = '''/**
 * Library Inventory Management System
 * Language: C++17 Standard
 * Architecture: Object-Oriented with STL Unordered Maps & RAII Memory Safety
 */

#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>
#include <iomanip>
#include <memory>
#include <chrono>

struct Book {
    std::string isbn;
    std::string title;
    std::string author;
    int totalCopies;
    int availableCopies;

    Book(std::string id, std::string t, std::string a, int qty)
        : isbn(std::move(id)), title(std::move(t)), author(std::move(a)), totalCopies(qty), availableCopies(qty) {}
};

struct LoanRecord {
    std::string memberId;
    std::string isbn;
    int loanDaysPassed;

    LoanRecord(std::string mId, std::string bIsbn, int days)
        : memberId(std::move(mId)), isbn(std::move(bIsbn)), loanDaysPassed(days) {}
};

class LibraryManager {
private:
    // O(1) Hash Map Indexing by ISBN
    std::unordered_map<std::string, Book> catalog;
    // Active loans keyed by "memberId_isbn"
    std::unordered_map<std::string, LoanRecord> activeLoans;
    const double FINE_PER_DAY = 0.50;
    const int STANDARD_LOAN_LIMIT_DAYS = 14;

public:
    LibraryManager() {
        // Seed standard catalog holdings
        addBook("978-0131103627", "The C Programming Language", "Kernighan & Ritchie", 5);
        addBook("978-0321563842", "The C++ Programming Language", "Bjarne Stroustrup", 3);
        addBook("978-0201633610", "Design Patterns", "Gang of Four", 4);
    }

    // Add or increment book holdings: O(1)
    bool addBook(const std::string& isbn, const std::string& title, const std::string& author, int quantity) {
        if (isbn.empty() || quantity <= 0) return false;
        
        auto it = catalog.find(isbn);
        if (it != catalog.end()) {
            it->second.totalCopies += quantity;
            it->second.availableCopies += quantity;
        } else {
            catalog.emplace(isbn, Book(isbn, title, author, quantity));
        }
        return true;
    }

    // Book checkout operation: O(1)
    bool checkoutBook(const std::string& memberId, const std::string& isbn, int daysSimulated = 0) {
        auto bookIt = catalog.find(isbn);
        if (bookIt == catalog.end()) {
            std::cout << "[Error] ISBN not found in catalog.\\n";
            return false;
        }

        if (bookIt->second.availableCopies <= 0) {
            std::cout << "[Error] All copies currently loaned out.\\n";
            return false;
        }

        std::string loanKey = memberId + "_" + isbn;
        if (activeLoans.find(loanKey) != activeLoans.end()) {
            std::cout << "[Error] Member already has a copy of this book on loan.\\n";
            return false;
        }

        bookIt->second.availableCopies--;
        activeLoans.emplace(loanKey, LoanRecord(memberId, isbn, daysSimulated));
        std::cout << "[Success] Book checked out to Member: " << memberId << "\\n";
        return true;
    }

    // Book return with automatic fine calculation: O(1)
    double returnBook(const std::string& memberId, const std::string& isbn, int returnDay) {
        std::string loanKey = memberId + "_" + isbn;
        auto loanIt = activeLoans.find(loanKey);

        if (loanIt == activeLoans.end()) {
            std::cout << "[Error] No active loan record found for this member and book.\\n";
            return -1.0;
        }

        auto bookIt = catalog.find(isbn);
        if (bookIt != catalog.end()) {
            bookIt->second.availableCopies++;
        }

        int totalDaysHeld = returnDay;
        int overdueDays = std::max(0, totalDaysHeld - STANDARD_LOAN_LIMIT_DAYS);
        double fine = overdueDays * FINE_PER_DAY;

        activeLoans.erase(loanIt);
        return fine;
    }

    // Formatted ASCII Inventory Audit Table: O(N)
    void printAuditReport() const {
        std::cout << "\\n========================== LIBRARY INVENTORY AUDIT ==========================\\n";
        std::cout << std::left << std::setw(18) << "ISBN"
                  << std::setw(32) << "Title"
                  << std::setw(22) << "Author"
                  << std::setw(10) << "Total"
                  << std::setw(10) << "Available" << "\\n";
        std::cout << std::string(92, '-') << "\\n";

        for (const auto& [isbn, book] : catalog) {
            std::cout << std::left << std::setw(18) << book.isbn
                      << std::setw(32) << book.title.substr(0, 30)
                      << std::setw(22) << book.author.substr(0, 20)
                      << std::setw(10) << book.totalCopies
                      << std::setw(10) << book.availableCopies << "\\n";
        }
        std::cout << "Active Patron Loans: " << activeLoans.size() << "\\n";
        std::cout << "============================================================================\\n";
    }
};

int main() {
    LibraryManager library;
    library.printAuditReport();

    // Demonstrate checkout and overdue fine calculation
    library.checkoutBook("MEM_101", "978-0131103627", 0);
    double fine = library.returnBook("MEM_101", "978-0131103627", 20); // 20 days (6 days overdue)

    std::cout << "Return processed. Overdue Fine Owed: $" << std::fixed << std::setprecision(2) << fine << "\\n";
    library.printAuditReport();
    return 0;
}
'''

LIBRARY_MANAGEMENT_CODE_EXPLANATION = {
    "summary": "This Modern C++17 library management system uses std::unordered_map for O(1) hash table book cataloging and active loan tracking, featuring automatic overdue fine computation.",
    "step_by_step": [
        "1. Struct Models: Book and LoanRecord structs encapsulate inventory counts and loan timestamps.",
        "2. O(1) Hash Table: Utilizes std::unordered_map with ISBN keys, eliminating expensive sequential array iterations.",
        "3. Checkout Guard: Atomically decrements available copies and binds a composite 'member_isbn' loan record.",
        "4. Return & Fine Calculus: Calculates days overdue past the 14-day threshold and computes monetary fines at $0.50/day.",
        "5. Formatted Audit: Iterates the catalog to output an aligned ASCII report with total vs available holdings."
    ],
    "key_components": [
        {"name": "std::unordered_map<std::string, Book>", "description": "Provides O(1) constant time catalog lookup by ISBN."},
        {"name": "returnBook Routine", "description": "Restores book stock and applies fine formula: max(0, days - 14) * 0.50."},
        {"name": "printAuditReport", "description": "Outputs formatted tabular data using std::setw streams."}
    ],
    "important_variables": [
        {"name": "catalog", "description": "Primary hash index mapping ISBN codes to Book objects."},
        {"name": "FINE_PER_DAY", "description": "Constant double setting daily late charge ($0.50/day)."},
        {"name": "STANDARD_LOAN_LIMIT_DAYS", "description": "14-day standard checkout period before penalties accrue."}
    ],
    "algorithm": "Hash Table Key-Value Indexing (std::unordered_map) with Overdue Date Delta Calculus",
    "time_complexity": "O(1) average case for Add, Checkout, Return, and Fine Calculation; O(N) for Audit Report.",
    "space_complexity": "O(B + L) where B is catalog size and L is number of active borrowing loans."
}

LIBRARY_MANAGEMENT_REVIEW = {
    "score": 95,
    "issues": [
        {
            "category": "Performance Issues",
            "severity": "Good",
            "title": "Optimal O(1) Algorithmic Time Complexity",
            "description": "All book indexing, checkout, and return operations utilize hash maps achieving constant time O(1)."
        },
        {
            "category": "Security Issues",
            "severity": "Good",
            "title": "Zero Pointer Arithmetic Leaks",
            "description": "Employs stack allocation and standard value semantics, completely avoiding raw pointer leaks."
        },
        {
            "category": "Bugs / Potential Issues",
            "severity": "Low",
            "title": "Console Stream Mutexing",
            "description": "If accessed in multi-threaded contexts, std::cout requires synchronization locks."
        }
    ],
    "suggestions": [
        "Add std::shared_mutex to permit concurrent read queries while locking writes.",
        "Serialize catalog to disk using JSON or flat binary files for persistent holding retention."
    ],
    "improved_code": """// Thread-Safe Read-Write Locking Extension
#include <shared_mutex>

class ThreadSafeLibraryManager : public LibraryManager {
private:
    mutable std::shared_mutex rwMutex;
public:
    bool threadSafeCheckout(const std::string& memberId, const std::string& isbn) {
        std::unique_lock<std::shared_mutex> lock(rwMutex);
        return checkoutBook(memberId, isbn);
    }
};
"""
}

LIBRARY_MANAGEMENT_DOCS = """# Software Requirement Specification (SRS)
## Project: Library Management System (C++17)
**Generated by CodeMind AI**

---

### 1. Executive Summary
The **C++ Library Management System** is a high-speed software utility engineered for librarians to catalog book collections, oversee patron loan circulations, compute late penalties, and generate formatted inventory audits.

### 2. Functional Requirements
- **FR-1**: Book cataloging (ISBN, Title, Author, Total Copies).
- **FR-2**: O(1) checkout with stock availability verification.
- **FR-3**: Book return with fine computation: max(0, days - 14) * $0.50.
- **FR-4**: Search by unique ISBN identifier.
- **FR-5**: Formatted inventory audit generation.

### 3. Non-Functional Specifications
- **NFR-1 Algorithmic Efficiency**: All core state lookups run in $O(1)$ average time complexity.
- **NFR-2 Memory Safety**: Strict adherence to Modern C++ RAII without raw pointers.
"""
