import requests
from datetime import datetime
from .resultset import ResultSet
from .nimbustsapiexception import NimbusTSAPIException

class NimbusTSAPI:
    def __init__(
            self,
            url,
            verify=True
        ):
        self.url = url
        self.verify = verify
        if not self.verify:
            requests.packages.urllib3.disable_warnings() 
    def getTSS(
            self,
            tscodes: list,
            datetimefrom: datetime,
            datetimeto: datetime,
        ):
        query = self.getGraphQLQuery(tscodes, datetimefrom,datetimeto)
        variables = {}
        results = self.postRequestAPI(
            requests.post,
            query=query
        )
        if 'errors' in results.keys():
            raise NimbusTSAPIException("Result has errors: " + str(results['errors']))
        return results
    def getGraphQLQuery(self,tscodes,datetimefrom,datetimeto):
        return """
        { 
            tss(
            tscodes:[\"""" + "\",\"".join(tscodes) + """\"] 
            datetimefrom: \"""" + datetimefrom.strftime("%Y-%m-%d %H:%M:%S") + """\"
            datetimeto: \"""" + datetimeto.strftime("%Y-%m-%d %H:%M:%S") + """\")
            {
                name
                values
                {   
                    datetime      
                    value
                }
            }
        }
        """
    def postRequestAPI(self,request,query):
        response = request(
            self.url,
            json={
                "query": query
            },
            verify=self.verify
        )
        return ResultSet(response.json())