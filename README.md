
Flying Squirrel Python Client
=============================


Flying Squirrel Web Hooks Client
================================

First, you need to import flyingsquirrel module:

    import flyingsquirrel

To establish a webhooks client connection you need three parameters:
`transport_url`, `ticket` (passed from the application that manages
endpoints) and `callback_url` - a url to which new messages will be
delivered.

    conn = flyingsquirrel.WebHooksClient(transport_url, ticket, callback_url)

From now on, you need to handle the url pointed by `callback_url`. For
example, using "BaseHTTPServer" class you may write something like:

    class WebHooksCallback(BaseHTTPServer.BaseHTTPRequestHandler):
        def do_POST(self):
            global conn
            body = self.rfile.read(int(self.headers.get('Content-Length', '0')))
            status = conn.deliver_message(body, self.headers)
            self.send_response(status)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

Following that dispatching, you can do usual publish/subscribe actions:

    def cb(data, **kwargs):
        print "received message %r" % (data,)
    conn.subscribe('recv', cb)

    conn.publish('send', 'test')

Or request/reply:

    def worker(msg, send_answer, **kwargs):
        print "Request received %r" % (msg,)
        send_answer('answer')

    conn.serve('rep', worker)

    def cb(answer, **kwargs):
        print "Answer received %r" % (answer,)

    print "Sending request"
    conn.request('req', 'a', cb)

Documentation
-------------

### WebHooksClient object

    conn = flyingsquirrel.WebHooksClient(transport_url, ticket, callback_url)

#### Methods

 - *disconnect()*
 - *deliver_message(body, headers)*
 - *publish(channel, body)*
 - *subscribe(channel, callback)*
 - *request(channel, question, callback)*
 - *serve(channel, callback)*


Flying Squirrel API
===================

You need this import:

    import flyingsquirrel


To connect to Flying Squirrel service you need the `api_url`.

   api = flyingsquirrel.API(api_url)
   endpoint = api.create_endpoint(endpoint_name,
                                  endpoint_definition)

   transport_url = endpoint['protocols']['webhooks']
   ticket = api.generate_ticket(endpoint_name, identity)

Documentation
-------------

### API object

    api = flyingsquirrel.API(api_url)

#### Methods:

 - *get_endpoint(name)*
 - *create_endpoint(name, definition)*
 - *delete_endpoint(name)*
 - *list_endpoints()*
 - *generate_ticket(name, identity, [timeout])*


