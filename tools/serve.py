#!/usr/bin/env python3
"""Serve the repo over http for browser testing (no Node needed).
Run: python3 tools/serve.py [port]   then open
http://localhost:8644/"""
import os, sys, http.server, socketserver
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
port = int(sys.argv[1]) if len(sys.argv) > 1 else 8644
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("127.0.0.1", port), http.server.SimpleHTTPRequestHandler) as h:
    print("serving on http://localhost:%d" % port)
    h.serve_forever()
