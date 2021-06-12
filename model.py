from google.appengine.ext import ndb 

class Branch(ndb.Model):
    'to describe branch info'
    BCode=ndb.IntegerProperty(required=True)
    BName=ndb.StringProperty()
    BAddress=ndb.TextProperty()

#inheriting a account class from model class
class Account(ndb.Model):
    'to describe an account info '
    AcNo=ndb.IntegerProperty(required=True)
    AcHName = ndb.StringProperty()
    PIN=ndb.IntegerProperty()
    AcBalance=ndb.FloatProperty(default=1000)
    #returns 50% of Ac balance into acoverlimit
    AcOverlimit = ndb.ComputedProperty(lambda self:self.AcBalance*0.5)
    Gen=ndb.StringProperty()
    City=ndb.StringProperty()
    AcDT=ndb.DateTimeProperty(auto_now_add=True)
    #structured property with branch 
    BInfo=ndb.StructuredProperty(Branch)
    ImgURL=ndb.StringProperty()