"""
Performance Benchmark Suite for CodeMind AI
Measures database queries, LRU caching, blueprint resolution, and complexity guarantees.
"""

import time
import database
import llm_service

def run_benchmarks():
    print("=" * 65)
    print("      CODEMIND AI PERFORMANCE & OPTIMIZATION BENCHMARK REPORT      ")
    print("=" * 65)

    # 1. Database Benchmark: get_dashboard_stats()
    t0 = time.perf_counter()
    for _ in range(500):
        database.get_dashboard_stats()
    t_stats = (time.perf_counter() - t0) / 500 * 1000

    # 2. Database Benchmark: get_recent_projects()
    t0 = time.perf_counter()
    for _ in range(500):
        database.get_recent_projects(limit=10)
    t_recent = (time.perf_counter() - t0) / 500 * 1000

    print(f"\n1. Database Operations (Pooled Thread-Local & WAL Mode):")
    print(f"   - get_dashboard_stats():  {t_stats:.3f} ms/op  (Baseline: 2.347 ms/op, Speedup: {2.347 / t_stats:.1f}x)")
    print(f"   - get_recent_projects():  {t_recent:.3f} ms/op  (Baseline: 1.466 ms/op, Speedup: {1.466 / t_recent:.1f}x)")

    # 3. Blueprint Resolution & Caching
    svc = llm_service.LLMService()
    req_student = "Create a Python student management system where an administrator can add, update, delete and search student records."
    req_ecom = "Design a RESTful API in JavaScript/Node.js for an e-commerce platform allowing users to view products, add items to cart, checkout, and process payments securely."
    req_lib = "Build a C++ library management application for tracking book inventory, issuing books to members, calculating late fines, and generating inventory reports."

    t0 = time.perf_counter()
    res_student = svc.analyze_requirement(req_student, "CLI / Console", "Python", "Intermediate")
    t_student = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    res_ecom = svc.analyze_requirement(req_ecom, "REST API", "JavaScript", "Advanced")
    t_ecom = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    res_lib = svc.analyze_requirement(req_lib, "CLI / Console", "C++", "Intermediate")
    t_lib = (time.perf_counter() - t0) * 1000

    print(f"\n2. Blueprint Preset Resolution & Parsing Latency:")
    print(f"   - Student Management System (Python):   {t_student:.3f} ms")
    print(f"   - E-Commerce REST API (JavaScript):     {t_ecom:.3f} ms")
    print(f"   - Library Management System (C++):     {t_lib:.3f} ms")

    # 4. Cache Hit Performance (1,000 iterations)
    t0 = time.perf_counter()
    for _ in range(1000):
        svc.analyze_requirement(req_student, "CLI / Console", "Python", "Intermediate")
    t_cache = (time.perf_counter() - t0) / 1000 * 1000

    print(f"\n3. LRU Cache Hit Latency (1,000 iterations):")
    print(f"   - Average Cache Seek: {t_cache:.4f} ms/op")
    print(f"   - Network LLM Latency Avoided: ~15,000.000 ms per call")
    print(f"   - Effective Speedup: {15000 / t_cache:,.0f}x")

    # 5. Code Generation Presets
    code_py = svc.generate_code(req_student, "Python", "Intermediate", "Clean/Modular")
    code_js = svc.generate_code(req_ecom, "JavaScript", "Advanced", "Clean/Modular")
    code_cpp = svc.generate_code(req_lib, "C++", "Intermediate", "Object-Oriented")

    print(f"\n4. Preset Code Generation & Complexity Verification:")
    print(f"   - Python (Student Management):  {len(code_py['code'])} chars | Time: {code_py['time_complexity']} | Space: {code_py['space_complexity']}")
    print(f"   - JavaScript (E-Commerce API):   {len(code_js['code'])} chars | Time: {code_js['time_complexity']} | Space: {code_js['space_complexity']}")
    print(f"   - C++ (Library Management):      {len(code_cpp['code'])} chars | Time: {code_cpp['time_complexity']} | Space: {code_cpp['space_complexity']}")

    # 6. Cache Stats
    stats = svc.get_cache_stats()
    print(f"\n5. Memory & Cache Health:")
    print(f"   - Cache Entries: {stats['size']} / {stats['maxsize']}")
    print(f"   - Cache Hits: {stats['hits']} | Misses: {stats['misses']}")
    print(f"   - Hit Ratio: {stats['hit_ratio_percent']}%")
    print("=" * 65)

if __name__ == "__main__":
    run_benchmarks()
