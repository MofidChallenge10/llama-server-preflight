import json, sys, threading, unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
sys.path.insert(0,'src')
from llama_server_preflight.__main__ import check
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  body=b'{}'; code=200
  if self.path=='/v1/models': body=json.dumps({'data':[{'id':'tiny-model'}]}).encode()
  elif self.path=='/health': body=b'{"status":"ok"}'
  else: code=404
  self.send_response(code); self.send_header('Content-Type','application/json'); self.end_headers(); self.wfile.write(body)
 def log_message(self,*args): pass
class TestCheck(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.server=HTTPServer(('127.0.0.1',0),Handler); cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True); cls.thread.start()
 @classmethod
 def tearDownClass(cls): cls.server.shutdown(); cls.thread.join()
 def test_ready_and_model(self):
  result=check(f'http://127.0.0.1:{self.server.server_port}','tiny-model'); self.assertTrue(result['ready'])
 def test_missing_model(self):
  result=check(f'http://127.0.0.1:{self.server.server_port}','other'); self.assertFalse(result['ready'])
if __name__=='__main__': unittest.main()
