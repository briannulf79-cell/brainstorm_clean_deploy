#!/usr/bin/env python3
"""
Simple test WSGI entry point to debug Railway deployment
"""
import os
import sys

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def application(environ, start_response):
    """Simple WSGI application for testing"""
    status = '200 OK'
    headers = [('Content-type', 'application/json')]
    start_response(status, headers)
    return [b'{"status": "healthy", "message": "Test WSGI working"}']

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', port, application)
    print(f"Test server running on port {port}")
    server.serve_forever()