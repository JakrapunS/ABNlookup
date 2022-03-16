# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from fuzzywuzzy import fuzz
import pandas as pd
import xml.etree.ElementTree as ET
import urllib.request as req

def connect_api(name,guid,post):
    """
    Connect to ABN Lookup API

    :param name: Company Name
    :param guid: authen id
    :param post: postcode
    :return: XML file
    """

    # Search parameters for ABRSearchByNameSimpleProtocol service
    # Note, this service requires all parameters to be specified, even if you specify no query parameter
    # The parameters specified below will search for an entity with  the name 'coles' with postcode '2250'
    # In this case, unspecified search parameters all default to 'Y'
    # (i.e. will search for the legal & trading name 'coles' in all States and Territories
    name_clean = name.replace(" ","%20")
    name = name_clean
    postcode = post
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
    """
    Transfrom XML to dataframe

    :param xml_text: XML result from API
    :return: pandas dataframe
    """
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

            if item.tag == '{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}mainName':
                for item in items.iter('{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}mainName'):
                    for j in item.iter():
                        if j.tag == '{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}organisationName':
                            i['trading_name'] = j.text
                        elif j.tag == '{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}fullName':
                            i['trading_name'] = j.text

                        if j.tag == '{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}isCurrentIndicator':
                            i['current_name'] = j.text

            elif item.tag == '{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}businessName':
                for item in items.iter('{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}businessName'):
                    for j in item.iter():
                        if j.tag == '{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}organisationName':
                            i['trading_name'] = j.text
                        elif j.tag == '{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}fullName':
                            i['trading_name'] = j.text

                        if j.tag == '{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}isCurrentIndicator':
                            i['current_name'] = j.text


            elif item.tag == '{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}legalName':
                for item in items.iter('{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}legalName'):
                    for j in item.iter():
                        if j.tag == '{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}organisationName':
                            i['trading_name'] = j.text
                        elif j.tag == '{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}fullName':
                            i['trading_name'] = j.text

                        if j.tag == '{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}isCurrentIndicator':
                            i['current_name'] = j.text
            elif item.tag == '{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}mainTradingName':
                for item in items.iter('{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}mainTradingName'):
                    for j in item.iter():
                        if j.tag == '{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}organisationName':
                            i['trading_name'] = j.text
                        elif j.tag == '{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}fullName':
                            i['trading_name'] = j.text

                        if j.tag == '{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}isCurrentIndicator':
                            i['current_name'] = j.text

            if item.tag == '{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}mainBusinessPhysicalAddress':
                for item in items.iter(
                        '{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}mainBusinessPhysicalAddress'):
                    for j in item.iter():
                        if j.tag == '{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}stateCode':
                            i['state'] = j.text
                        elif j.tag == '{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}postcode':
                            i['postcode'] = j.text

                        if j.tag == '{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}isCurrentIndicator':
                            i['current_address'] = j.text

            if item.tag == '{http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes}score':
                i['score'] = item.text

        result.append(i)

    pd_result = pd.DataFrame(result)
    return pd_result


def abn_search(name, post=''):
    """
    Search ABN by name and postcode. Also compute Levenshtein Distance for the case that have equally score from api.

    :param name: Company name
    :param post: postcode
    :return: company ABN
    """
    if post == 'nan':
        post = ''
    xml_text = connect_api(name, '33ae5dc0-c84a-47e2-8ebf-f54fc59abbf6', str(post))
    df = df_return(xml_text)
    # Check if can find the company
    if df.empty:
        return ""
    else:
        df['score'] = df['score'].apply(lambda x: int(x))
        df2 = df[df['abn_status'] == 'Active'].reset_index(drop=True)
        s_max = df2['score'].max()
        # Filter only score = max
        df2 = df2[df2['score'] == s_max].reset_index(drop=True)
        # If only one record left retrun abn of that record
        if df2.shape[0] == 1:
            return df2.iloc[0]['abn']
        #If more than one record check name similarity and return thge most similar one.
        else:
            df2['Lev_score'] = df2['trading_name'].apply(lambda x: fuzz.ratio(x.lower(), name.lower()))
            df2 = df2.sort_values(by=['Lev_score'], ascending=False)
            return df2.iloc[0]['abn']





# Press the green button in the gutter to run the script.
if __name__ == '__main__':


    abn = abn_search('A C & J I Kearley','')
    print("ABN: ",abn)




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
