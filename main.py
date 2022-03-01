# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import urllib.request as req
import xml.etree.ElementTree as ET
import pandas as pd

def connect_api(guid):
    # Search parameters for ABRSearchByNameSimpleProtocol service
    # Note, this service requires all parameters to be specified, even if you specify no query parameter
    # The parameters specified below will search for an entity with  the name 'coles' with postcode '2250'
    # In this case, unspecified search parameters all default to 'Y'
    # (i.e. will search for the legal & trading name 'coles' in all States and Territories
    name = 'coles'
    postcode = '2250'
    legalName = ''
    tradingName = ''
    NSW = 'Y'
    SA = 'Y'
    ACT = 'Y'
    VIC = 'Y'
    WA = 'Y'
    NT = 'Y'
    QLD = 'Y'
    TAS = 'Y'
    authenticationGuid = guid  # Your GUID should go here

    # Constructs the URL by inserting the search parameters specified above
    # GETs the url (using urllib.request.urlopen)
    conn = req.urlopen('https://abr.business.gov.au/abrxmlsearchRPC/AbrXmlSearch.asmx/' +
                       'ABRSearchByNameSimpleProtocol?name=' + name +
                       '&postcode=' + postcode + '&legalName=' + legalName +
                       '&tradingName=' + tradingName + '&NSW=' + NSW +
                       '&SA=' + SA + '&ACT=' + ACT + '&VIC=' + VIC +
                       '&WA=' + WA + '&NT=' + NT + '&QLD=' + QLD +
                       '&TAS=' + TAS + '&authenticationGuid=' + authenticationGuid)

    # XML is returned by the webservice
    # Put returned xml into variable 'returnedXML'
    # Output xml string to file 'output.xml' and print to console
    returnedXML = conn.read()
    # f = open('output2.xml', 'wb')
    # f.write(returnedXML)
    # f.close
    # print(returnedXML)
    return returnedXML

def df_return(xml_text):
    #transform string to xml
    tree = ET.fromstring(xml_text)
    result = []
    for items in tree.iter(tag='{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}searchResultsRecord'):
        # for abn in items.iter(tag = '{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}ABN'):
        # print(ET.tostring(abn,encoding='unicode',method='text'))
        # print(items.tag)
        # print(items.find('{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}identifierStatus'))
        i = {}
        for item in items.iter():

            if item.tag == '{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}identifierValue':
                i['abn'] = item.text

            if item.tag == '{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}identifierStatus':
                i['abn_status'] = item.text

            if item.tag == '{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}organisationName':
                i['trading_name'] = item.text
            elif item.tag == '{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}fullName':
                i['trading_name'] = item.text

            if item.tag == '{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}isCurrentIndicator':
                i['current'] = item.text

            if item.tag == '{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}isCurrentIndicator':
                i['current'] = item.text

            if item.tag == '{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}stateCode':
                i['state'] = item.text

            if item.tag == '{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}postcode':
                i['postcode'] = item.text

        result.append(i)

    pd_result = pd.DataFrame(result)
    return pd_result





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    xml_text = connect_api('33ae5dc0-c84a-47e2-8ebf-f54fc59abbf6')
    df = df_return(xml_text)
    test = df.to_csv('abn.csv',index=False)




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
