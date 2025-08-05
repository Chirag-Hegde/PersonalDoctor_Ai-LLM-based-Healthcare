#!/usr/bin/env python3
"""
Test script for the working HealifyAI application
"""

import sys
import os

# Add deployment_hf to path
sys.path.append('deployment_hf')

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import flask
        print("✅ Flask imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Flask: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ NumPy imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import NumPy: {e}")
        return False
    
    return True

def test_app_functions():
    """Test if the app functions work"""
    print("\nTesting app functions...")
    
    try:
        # Import app functions
        from app_minimal import predict_disease_simple, answer_medical_question
        
        # Test disease prediction
        test_symptoms = "fever, headache, fatigue"
        result = predict_disease_simple(test_symptoms)
        print("✅ Disease prediction test successful")
        print(f"   Input: {test_symptoms}")
        print(f"   Output: {result[:100]}...")
        
        # Test Q&A
        test_question = "What are the symptoms of diabetes?"
        result = answer_medical_question(test_question)
        print("✅ Q&A test successful")
        print(f"   Input: {test_question}")
        print(f"   Output: {result[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ App function test failed: {e}")
        return False

def test_flask_app():
    """Test if Flask app can be created"""
    print("\nTesting Flask app creation...")
    
    try:
        from app_minimal import app
        print("✅ Flask app created successfully")
        return True
    except Exception as e:
        print(f"❌ Flask app creation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Working HealifyAI Application")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_app_functions,
        test_flask_app
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is working correctly.")
        print("\nTo run the application:")
        print("1. Activate virtual environment: healify_env\\Scripts\\activate")
        print("2. Navigate to deployment: cd deployment_hf")
        print("3. Run app: python app_minimal.py")
        print("4. Open browser: http://localhost:5000")
        print("\nOr use the startup script: start_working_app.bat")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")

if __name__ == "__main__":
    main() 