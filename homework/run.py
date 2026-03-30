#!/usr/bin/env python3

import json
import sys
import importlib.util
from pathlib import Path
from datetime import datetime

def check_python_lessons():
    """Check Python lesson files."""
    import os
    homework_dir = Path(os.path.join(os.getcwd(), 'homework'))
    test_results = []
    
    # Find student solutions
    lesson_files = []
    for file_path in homework_dir.glob('lesson_*.py'):
        if not (file_path.name.endswith('_good.py') or file_path.name.endswith('_perfect.py')):
            lesson_files.append(file_path)
    
    if not lesson_files:
        test_results.append({
            "name": "python_lessons",
            "status": "skipped",
            "message": "No Python lesson files found (excluding _good and _perfect)",
            "details": {}
        })
        return test_results
    
    for lesson_file in lesson_files:
        lesson_name = lesson_file.stem
        
        try:
            # Load the module
            spec = importlib.util.spec_from_file_location(lesson_name, lesson_file)
            module = importlib.util.module_from_spec(spec)
            
            # Execute the module
            spec.loader.exec_module(module)
            
            # Check for required variables based on lesson
            required_vars = []
            if lesson_name == "lesson_1":
                required_vars = ['category_a', 'category_b', 'total_value']
            elif lesson_name == "lesson_2":
                required_vars = ['data_processed', 'transformation_applied']
            
            missing_vars = []
            present_vars = {}
            
            for var in required_vars:
                if hasattr(module, var):
                    present_vars[var] = str(getattr(module, var))
                else:
                    missing_vars.append(var)
            
            if missing_vars:
                test_results.append({
                    "name": lesson_name,
                    "status": "failed",
                    "message": f"Missing required variables: {', '.join(missing_vars)}",
                    "details": present_vars
                })
            else:
                test_results.append({
                    "name": lesson_name,
                    "status": "passed",
                    "message": f"All required variables present: {', '.join(required_vars)}",
                    "details": present_vars
                })
                
        except Exception as e:
            test_results.append({
                "name": lesson_name,
                "status": "error",
                "message": f"Error processing {lesson_name}: {str(e)}",
                "details": {}
            })
    
    return test_results

def main():
    """Main function to run all tests."""
    test_results = []
    
    # Check Python lesson files
    python_results = check_python_lessons()
    test_results.extend(python_results)
    
    # Create TestResults directory
    test_results_dir = Path('TestResults')
    test_results_dir.mkdir(exist_ok=True)
    
    # Save results to JSON
    results_data = {
        "timestamp": datetime.now().isoformat(),
        "total_tests": len(test_results),
        "passed": len([r for r in test_results if r["status"] == "passed"]),
        "failed": len([r for r in test_results if r["status"] == "failed"]),
        "skipped": len([r for r in test_results if r["status"] == "skipped"]),
        "errors": len([r for r in test_results if r["status"] == "error"]),
        "results": test_results
    }
    
    with open(test_results_dir / 'results.json', 'w', encoding='utf-8') as f:
        json.dump(results_data, f, indent=2, ensure_ascii=False)
    
    print(f"Test completed: {results_data['passed']}/{results_data['total_tests']} passed")
    return results_data

if __name__ == "__main__":
    main()
