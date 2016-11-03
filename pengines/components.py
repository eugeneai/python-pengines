from pengines.interfaces import IPengine
from zope.interface import implementer
import json, requests
import pprint

ALLOWED_KW=set(["template", "chunk", "alias"])

@implementer(IPengine)
class Pengine(object):
    """Instances of the class provide interface
    to SWI-Prolog pengine server. """

    chunk=1000

    def __init__(self, url, alias=None, options=None):
        self.alias=alias
        if options==None:
            options={}
        self.options=options
        self.url=url
        self._url=url.rstrip("/")+"/pengine"
        self.created=False
        self.destroyed=False
        self.more=False

    def _send(self, target='send', query=None):
        tgt=self._url+"/"+target+"?format=json"
        if target!="create":
            tgt+="&id={}".format(self.id)
        if query==None:
            raise ValueError("query string cannot be None")
        #if query=='':
        #    raise ValueError("query string cannot be empty")
        if type(query)==str:
            data=query
        else:
            data=json.dumps(query)
        data+=" .\n"
        # print ("Sent:" + str(data), "to:", tgt)
        rc=requests.post(
            tgt,
            data=data,
            headers={'Content-Type': 'application/json; charset=UTF-8'}
        )
        if rc.status_code!=requests.codes.ok:
            raise RuntimeError ('status code {}'.format(rc.status_code))
        # print ("Received:",rc, rc.text)
        rc=json.loads(rc.text)
        self._query=query
        data=self._process(rc)
        del self._query
        return rc,data

    def _process(self,rc):
        # print ("RC:",rc)
        data=None
        if 'event' in rc:
            ev=rc['event']
            if ev=='create':
                self.created=True
                self.slave_limit=rc['slave_limit']
                self.id=rc['id']
                data=rc
            elif ev=='destroy':
                self.created=False
                self.destroyed=True
                data=rc['data']
            elif ev=="success":
                data=rc
                self.success(data)
            elif ev=="error":
                self.error(rc)
            elif ev=="output":
                data=rc['data']
                self.output(data)
            #else:
            #    print ("UNKNOWN:", rc)
        if data!=None:
            if 'more' in data:
                self.more=data['more']
            if rc!=data and 'data' in data:
                self._process(data)
        return data

    def create(self, **kwargs):
        k={}
        k.update(kwargs)
        k['format']='json'
        rc,data=self._send('create', query=k)

    def ask(self, query):
        rc,data=self._send(query="ask({},[])".format(query))
        return data

    def query(self, query, **kwargs):
        kw={}
        kw.update(kwargs)
        if not "chunk" in kw:
            kw['chunk']=self.chunk

        opts=[]
        for k,v in kw.items():
            if k in ALLOWED_KW:
                opts.append(k+"("+str(v)+")")
        opts="["+",".join(opts)+"]"

        if not self.created:
            raise StopIteration
        rc,data=self._send(query="ask({},{})".format(query, opts))
        if data['event']=='failure':
            raise StopIteration
        #projection=rc['projection']
        while True:
            # print (data)
            streaming=data['data']
            for answer in streaming:
                yield answer
            more=data['more']
            if more:
                rc,data=self.next()
            else:
                break

    def next(self, N=None):
        if N:
            return self._send(query="next({})".format(N))
        else:
            return self._send(query="next")

    def stop(self):
        return self._send(query="stop")

    def abort(self):
        return self._send(target='abort', query="")

    def destroy(self):
        return self._send(query='destroy')

    def error(self, rc):
        err=rc['code']
        msg=rc['data']
        print (self._query)
        raise RuntimeError(msg)

    def success(self, data):
        pass

    def output(self, data):
        pprint.pprint (data)

    def input(self, data):
        raise RuntimeError("not implemented.")

if __name__=="__main__":
    p="""
    a(x,1).
    a(y,3).
    a(y,4).
    a(y,5).
    a(y,3).
    a(y,3).
    a(y,6).
    a(y,7).
    a(y,8).
    a(y,9).
    a(u,6).
    """
    pl=Pengine("http://pengines.swi-prolog.org/")
    pl.create(src_text=p)
    print (pl.id)

    for row in pl.query('a(X,Y)',chunk=200):
        for k,v in row.items():
            print ("{}={}, ".format(k,v), end='')
        print ()
    quit()
