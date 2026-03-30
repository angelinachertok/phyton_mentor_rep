#!/usr/bin/env python3

import json
import sys
import importlib.util
from pathlib import Path
from datetime import datetime

def check_python_lessons():
    """Check Python lesson files."""
    import os
    # Look for lesson files in the mentor repository (current directory)
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
    import os
    test_results_dir = Path(os.environ.get('RESULTS_DIR', '/mnt/results'))
    test_results_dir.mkdir(exist_ok=True)
    
    test_results = []
    
    # Check Python lesson files
    python_results = check_python_lessons()
    test_results.extend(python_results)
    
    # Save results as JUnit XML
    total_tests = len(test_results)
    passed_tests = len([r for r in test_results if r["status"] == "passed"])
    failed_tests = len([r for r in test_results if r["status"] == "failed"])
    error_tests = len([r for r in test_results if r["status"] == "error"])
    skipped_tests = len([r for r in test_results if r["status"] == "skipped"])
    
    xml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<testsuites name="Python Ingestion Tests" tests="{total_tests}" failures="{failed_tests}" errors="{error_tests}" skipped="{skipped_tests}">
    <testsuite name="Python Lessons" tests="{total_tests}" failures="{failed_tests}" errors="{error_tests}" skipped="{skipped_tests}">
'''
    
    for result in test_results:
        status = "passed" if result["status"] == "passed" else "failed" if result["status"] == "failed" else "error" if result["status"] == "error" else "skipped"
        xml_content += f'''        <testcase name="{result['name']}" classname="PythonTests" status="{status}">
'''
        if status in ["failed", "error"]:
            xml_content += f'''            <failure message="{result['message']}">{result.get('details', '')}</failure>
'''
        elif status == "skipped":
            xml_content += f'''            <skipped message="{result['message']}"/>
'''
        xml_content += '''        </testcase>
'''
    
    xml_content += '''    </testsuite>
</testsuites>'''
    
    with open(test_results_dir / 'results.xml', 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"Test completed: {passed_tests}/{total_tests} passed")
    return results_data

if __name__ == "__main__":
    main()
