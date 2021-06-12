import webapp2
from model import Account, Branch
import cloudstorage as gcs
from google.appengine.api import app_identity
import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        html = open('header.html').read()
        self.response.write(html)
        html = open("index.html").read()
        self.response.write(html)

class IndexProcess(webapp2.RequestHandler):
    def post(self):
        html = open("header.html").read()
        self.response.write(html)
        # getting default bucket name
        bucket = app_identity.get_default_gcs_bucket_name()
        self.response.write("<h1>"+bucket+"</h1>")
        # reading all request parameters
        an = self.request.POST.get("tfAcNo") 
        ahn = self.request.POST.get("tfAcHName") 
        pin = self.request.POST.get("pfPIN") 
        gen = self.request.POST.get("rbtngen")
        city = self.request.POST.get("ddCity") 
        # reading branch detail
        bc = self.request.POST.get("tfBC")
        bn = self.request.POST.get("tfBN")
        ba = self.request.POST.get("taBA")
        # reading file attachements
        files = self.request.POST.getall("propic")
        for file in files:
            self.response.write(file.filename+"<hr/>")
            self.response.write(file.type+"<hr/>")
            # self.response.write(file.file.read()+"<hr/>")
            # creating a file on cloud storage to write image file
            fw = gcs.open("/"+bucket+"/"+file.filename, 
                    "w", 
                    file.type, 
                    options={'x-goog-acl':'public-read'})
            # writing content into file as uploaded by web browser
            fw.write(file.file.read())
            fw.close()
            fp = "https://storage.cloud.google.com/"+bucket+"/"+file.filename
            self.response.write("<hr/>"+fp)
        # sending data to the web browser
        self.response.write("<h3>"+an+"</h3>")
        self.response.write("<h3>"+ahn+"</h3>")
        self.response.write("<h3>"+pin+"</h3>")
        self.response.write("<h3>"+gen+"</h3>")
        self.response.write("<h3>"+city+"</h3>")
        self.response.write("<h3>"+bc+"</h3>")
        self.response.write("<h3>"+bn+"</h3>")
        self.response.write("<h3>"+ba+"</h3>")
        # creating an instance of Account class
        ac1 = Account()
        ac1.AcNo = int(an)
        ac1.AcHName = ahn
        ac1.PIN = int(pin)
        ac1.Gen = gen
        ac1.City = city
        # creating an instance of Branch class
        br = Branch()
        br.BCode = int(bc)
        br.BName = bn
        br.BAddress = ba
        # set into account instance
        ac1.BInfo = br
        ImgURL=fp       
        # putting an account instance into database
        key = ac1.put()
        self.response.write("Key : "+str(key) )

class AllAccount(webapp2.RequestHandler):
    def get(self):
        html = open("header.html").read()
        self.response.write( html )
        # retrieving all data from ndb in the form of Account objects
        result = Account.query()
        template_values = {'data':result}
        template = JINJA_ENVIRONMENT.get_template("allaccount.html")
        html = template.render(template_values)
        self.response.write( html )
        # self.response.write("<table border='1' cellspacing='10px'>")
        # self.response.write("<tr>")
        # self.response.write("<th>Ac No </th>")
        # self.response.write("<th>Ac H Name </th>")
        # self.response.write("<th>Ac PIN </th>")
        # self.response.write("<th>Ac Gender </th>")
        # self.response.write("<th>Ac City </th>")
        # self.response.write("<th>Url safe key </th>")
        # self.response.write("</tr>")
        # for item in result:
        #     self.response.write("<tr>")
        #     self.response.write("<td>"+str(item.AcNo)+"</td>")
        #     self.response.write("<td>"+item.AcHName+"</td>")
        #     self.response.write("<td>"+str(item.PIN)+"</td>")
        #     self.response.write("<td>"+item.Gen+"</td>")
        #     self.response.write("<td>"+item.City+"</td>")
        #     self.response.write("<td>"+item.key.urlsafe()+"</td>")
        #     self.response.write("</tr>")
        # self.response.write("</table>")

class SearchInterface(webapp2.RequestHandler):
    def get(self):
        html = open("header.html").read()
        self.response.write( html )
        html = open("searchact.html").read()
        self.response.write( html )

class SearchAcccount(webapp2.RequestHandler):
    def get(self):
        html = open("header.html").read()
        self.response.write(html)
        an = self.request.get("tfAcNo")
        # retrieving Account obj that has ac no 
        result = Account.query(Account.AcNo == int(an) )
        for item in result:
            self.response.write("<h3>"+str(item.AcNo)+"</h3>")
            self.response.write("<h3>"+item.AcHName+"</h3>")
            self.response.write("<h3>"+str(item.PIN)+"</h3>")
            self.response.write("<h3>"+item.Gen+"</h3>")
            self.response.write("<h3>"+item.City+"</h3>")
            
class GCloudStorage(webapp2.RequestHandler):
    def get(self):
        pass

start = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/addact', MainHandler),
    ('/indexCode', IndexProcess),
    ('/allact', AllAccount),
    ('/searchact', SearchInterface),
    ('/searchactno', SearchAcccount),
    ('/gcs', GCloudStorage)
], debug = True)