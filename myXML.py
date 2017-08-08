
# coding: utf-8

# In[ ]:

#!/usr/bin/env python


"""enables to audit and correct OpenStreetMap (OSM) XML files as well as to transfer data into SQLLite3 database.

.. module:: myXML
   :platform: Windows
   :synopsis: A useful module indeed.

.. moduleauthor:: Jan Foerster <jan.foerster@airbus.com>


"""

#__license__ = 'Jan FOERSTER'
#__revision__ = ' $Id: MyXML.py 1 2017-07-30 09:27:45z cokelaer $ '
#__docformat__ = 'reStructuredText'

import xml.etree.cElementTree as ET
from collections import defaultdict
import codecs as co
import cerberus, schema, csv
import re, pprint

class Investigation(object):
    """Investigation class. Investigation class analyzes a XML object for OpenStreetMap (OSM).
 
    .. class:: Investigation
       Initializes only private variables, containing results of callable methods.

       :method: :func:`view_Tags_Attributes`
       :method: :func:`count_Tags`
       :method: :func:`load_XML_Data`
       :method: :func:`audit_Zip_Codes`
       :method: :func:`audit_Street_Names`
       :method: :func:`audit_Phone_Numbers`
       :method: :func:`audit_Data_Chars`
       :method: :func:`audit_Unique_Values`
        
       :function: :func:`sort_Dictionary`
       :function: :func:`get_Tags_Attributes`
       :function: :func:`get_Tags`
       :function: :func:`get_XML_Data`
       :function: :func:`get_Street_Names`
       :function: :func:`get_Aligned_Street_Names`
       :function: :func:`get_ZIP_Codes`
       :function: :func:`get_Phone_Numbers`
       :function: :func:`get_Aligned_Phone_Numbers`
       :function: :func:`get_Problematic_Chars`
       :function: :func:`get_Unique_Values`
       
       
    """ 

    #Initializing Class
    def __init__(self, xml_file):
        #Input XML file
        self.xml_file = xml_file
        
        #private dictionaries            
        ## def view_tags_attributes
        self._xml_file_tags_and_attributes = defaultdict(set)
        
        ##def count_tags
        self._xml_file_tags = {}
        
        ##def audit_street_names
        self._street_types = defaultdict(set)
        self._aligned_street_types = defaultdict(set)
        
        ##def audit_zip_type
        self._zip_types = defaultdict(set)
        
        ##def audit_phone
        self._phone_types = defaultdict(set)
        self._aligned_phone_types = defaultdict(set)
        
        ##def audit_data_chars
        self._data_structures = {'lower': 0, 'lower_colon': 0, 'problemchars': 0, 'other': 0}
        
        #private sets
        ##def audit_unique_value
        self._unique_values = defaultdict(int)

    def view_Tags_Attributes(self):
        """identifies XML tags and their belonging attributes as XML infrastructure
 
        :Example:

        >>> myOSMfile.view_Tags_Attributes()
        >>> pprint.pprint(myOSMfile.get_Tags_Attributes())

        .. seealso:: :func:`get_Tags_Attributes`.
        .. warning:: first, function :func:`view_Tags_Attributes` needs to be executed, otherwise return value is None.
        .. todo:: execute first :func:`view_Tags_Attributes`.
        
        
        """ 
        for _, elem in ET.iterparse(self.xml_file):
            for attrName in elem.keys():
                self._xml_file_tags_and_attributes[elem.tag].add(attrName)            
        
    def get_Tags_Attributes(self):
        """returns private SeDefaultDict(Set) showing occurance of XML tags and their attributes

        :returns: self._xml_file_tags_and_attributes 
        :rtype: defaultdict(set)

        :Example:
        
        >>> myOSMfile.view_Tags_Attributes()
        >>> pprint.pprint(myOSMfile.get_Tags_Attributes())
        
        .. seealso:: :func:`view_Tags_Attributes`.
        .. warning:: first, function :func:`view_Tags_Attributes` needs to be executed, otherwise return value is None.
        .. todo:: execute first :func:`view_Tags_Attributes`.
        
        
        """ 
        return self._xml_file_tags_and_attributes      
    
    def count_Tags(self):
        """counts occurance of XML tags

        :Example:
        
        >>> myOSMfile.count_Tags()
        >>> pprint.pprint(myOSMfile.get_Tags()) 
        
        .. seealso:: :func:`get_Tags`.
        .. warning:: first, function :func:`count_Tags` needs to be executed, otherwise return value is None.
        .. todo:: execute first :func:`count_Tags`.
        
        
        """ 
        for _, elem in ET.iterparse(self.xml_file):
            if elem.tag not in self._xml_file_tags:
                self._xml_file_tags[elem.tag] = 1
            else:    
                self._xml_file_tags[elem.tag] += 1

    def get_Tags(self):
        """returns private Set() counting occurance of XML tags

        :returns: self._xml_file_tags
        :rtype: Set()

        :Example:
        
        >>> myOSMfile.count_Tags()
        >>> pprint.pprint(myOSMfile.get_Tags()) 
        
        .. seealso:: :func:`count_Tags`.
        .. warning:: first, function :func:`count_Tags` needs to be executed, otherwise return value is None.
        .. todo:: execute first :func:`count_Tags`.
        
        
        """  
        return self._xml_file_tags                
                    
    def audit_Zip_Codes(self):   
        """identifies incorrect ZIP codes, not being compliant to:
        
        >>> zip_type_re = re.compile(r'^[2]{1}[0-9]{4}$')

        :Example:

        >>> myOSMfile.audit_Zip_Codes()
        >>> pprint.pprint(myOSMfile.get_ZIP_Codes()) 
        
        .. seealso:: :func:`get_ZIP_Codes`
        .. warning:: first, function :func:`audit_Zip_Codes` needs to be executed, otherwise return value is None.
        .. todo:: execute first :func:`audit_Zip_Codes`.
        
        
        """         
        zip_type_re = re.compile(r'^[2]{1}[0-9]{4}$')
        
        #Check tag for zip data content 
        def is_zip_name(elem):
            return (elem.attrib['k'] == 'addr:postcode')
    
        #Add zip figures in dictionary by type
        #Takes 2 arguments: dictionary and string. If string doesn't match pattern adds it to dictionary. 
        def audit_zip_type(zip_types, zip_name):
            m = zip_type_re.search(zip_name)
            if m:
                zip_type = m.group()
                if zip_type not in zip_types:
                    zip_types[zip_type].add(zip_name)
            else:
                zip_types['unknown'].add(zip_name)
                
        #Clean Street names in compliance to above Dictionary
        def update_zip():
            ##Elimenate dicrepancies from given directory
            for zip_keys, zip_codes in self._zip_types.iteritems():
                for zip_code in zip_codes:
                    m = zip_type_re.search(zip_code)
                    if m:
                        zip_code = m.group()
                    else:
                        zip_code = 'unknown'
                self._zip_types[zip_keys] = zip_code   
            
        #Main
        with co.open(self.xml_file, 'r', 'utf-8'):            
            for event, elem in ET.iterparse(self.xml_file, events=('start',)):
                if elem.tag == 'node' or elem.tag == 'way':
                    for tag in elem.iter('tag'):
                        if is_zip_name(tag):
                            audit_zip_type(self._zip_types, tag.attrib['v'])
        
        update_zip()

    def get_ZIP_Codes(self, dict_attr_in = ''):
        """returns private DefaultDict(set) of *original* ZIP codes
        
        :param str dict_attr_in: Indicate specific dictionary key
        
        :returns: self._zip_types
        :rtype: defaultdict(set) tuple of key, value

        :Example:

        >>> myOSMfile.audit_Zip_Codes()
        >>> pprint.pprint(myOSMfile.get_ZIP_Codes())
        
        .. seealso:: :func:`audit_Zip_Codes`
        .. warning:: first, function :func:`audit_Zip_Codes` needs to be executed, otherwise return value is None.
        .. todo:: execute first :func:`audit_Zip_Codes`.
        
        
        """           
        if dict_attr_in == '':
            return self._zip_types
        else:
            return self._zip_types[dict_attr_in]        

    def audit_Street_Names(self):
        """identifies incorrect street names, not being compliant to:
        
        >>> street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

        :Example:
        
        >>> myOSMfile.audit_Street_Names()
        >>> pprint.pprint('Unknown Streets %s' % + myOSMfile.get_Street_Names('unknown'))
        >>> pprint.pprint('Unknown Streets %s' % + myOSMfile.get_Street_Names('mysterious'))
    
        .. seealso:: :func:`get_Street_Names` or :func:`get_Aligned_Street_Names`
        .. warning:: first, func :func:`audit_Street_Names` needs to be executed, otherwise return value is None.
        .. todo:: execute first :func:`audit_Street_Names`.
        
        
        """    
        expectedStreet = [  u'acker'
                          , u'aue'
                          , u'allee'
                          , u'bahn'
                          , u'berg'
                          , u'berge'
                          , u'blatt'
                          , u'brack'
                          , u'brücke'
                          , u'chaussee'
                          , u'damm'
                          , u'deich'
                          , u'diek'
                          , u'eiche'
                          , u'fleet'
                          , u'feld'
                          , u'graben'
                          , u'haide'
                          , u'hang'
                          , u'heide'
                          , u'hoef'
                          , u'hof'
                          , u'holz'
                          , u'kai'
                          , u'kamp'
                          , u'kehre'
                          , u'kirchenweg'
                          , u'kirchweg'
                          , u'knick'
                          , u'koppel'
                          , u'land'
                          , u'markt'
                          , u'marsch'
                          , u'moor'
                          , u'nordereich'
                          , u'ort'
                          , u'passage'
                          , u'park'
                          , u'platz'
                          , u'redder'
                          , u'ring'
                          , u'sand'
                          , u'strasse'
                          , u'straße'
                          , u'stieg'
                          , u'styg'
                          , u'tal'
                          , u'terrasse'
                          , u'tor'
                          , u'treppe'
                          , u'teich'
                          , u'twiete'
                          , u'ufer'
                          , u'wald'
                          , u'wall'
                          , u'weg'
                          , u'weide'
                          , u'weiden'
                          , u'winkel'
                          , u'wisch'
                         ]

        #street_type_re = re.compile(r'\w+(' + '|'.join(map(re.escape, expectedStreet)) + ')\w?', re.I|re.U)
        #street_type_re = re.compile(r'\w+(([-]\w+)|(\b\w+\b))?(' + '|'.join(map(re.escape, expectedStreet)) + ')\w?', re.I|re.U)
        #street_type_re = re.compile(r'\s*(' + '|'.join(map(re.escape, expectedStreet)) + ')\s?', re.I|re.U)
        street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

        
        mappingStreet =  {  'nr.' : ''
                          , 'str.': 'Strasse'
                          , '65'  : ''
                          , '85'  : ''
                          , '108' : ''
                         }

        def is_street_name(elem):
            #return (elem.tag == 'tag') and (elem.attrib['k'] == 'addr:street')
            return (elem.attrib['k'] == 'addr:street')

        def update_street_name(street_name, mappingStreet):
            ##Elimenate dicrepancies from given directory
            m = street_type_re.search(street_name)
            if m:  
                try:
                    street_replacement = mappingStreet[m.group()]
                    street_name = street_type_re.sub(street_replacement, street_name)
                    return street_name
                except:
                    return street_name
            else:
                street_name = 'unknown'
                return street_name

        def audit_street_type(street_types, street_name):

            origin_street_name = street_name            

            #street_name = ''.join(street_name.lower().split())
            street_name = street_name.lower()

            #Allocate categories as above defined
            for m in street_type_re.finditer(street_name):
                street_types[m.group()].add(origin_street_name)

            #for those unknown items re-iterate                
            m = street_type_re.search(street_name)
            if m:
                street_type = m.group()
                if street_type not in expectedStreet:
                    street_types[street_type].add(origin_street_name)
            else:
                street_types['mysterious'].add(origin_street_name)

        #Main  
        ## Open file and find out discrepancies
        for event, elem in ET.iterparse(self.xml_file, events=('start',)):
            if elem.tag == 'node' or elem.tag == 'way':
                for tag in elem.iter('tag'):
                    if is_street_name(tag):
                        audit_street_type(self._street_types, tag.attrib['v'])
    
        ##Elimenate dicrepancies from given directory
        for street_keys, street_names in self._street_types.iteritems():
            for street_name in street_names:
                self._aligned_street_types[street_name] = update_street_name(street_name, mappingStreet)

    def get_Street_Names(self, dict_attr_in = ''):
        """returns private DefaultDict(set) of *original* street names
        
        :param str dict_attr_in: Indicate specific dictionary key
        
        :returns: self._street_types
        :rtype: defaultdict(set) tuple of key, value

        :Example:

        >>> myOSMfile.audit_Street_Names()
        >>> pprint.pprint('Unknown Streets %s' % + myOSMfile.get_Street_Names('unknown'))
        >>> pprint.pprint('Unknown Streets %s' % + myOSMfile.get_Street_Names('mysterious'))
    
        .. seealso:: :func:`audit_Street_Names`
        .. warning:: first, function :func:`audit_Street_Names` needs to be executed, otherwise return value is None.
        .. todo:: execute first :func:`audit_Street_Names`.
        
        
        """           
        if dict_attr_in == '':
            return self._street_types
        else:
            return self._street_types[dict_attr_in]

    def get_Aligned_Street_Names(self, dict_attr_in = ''):
        """returns private DefaultDict(set) of *updated & corrected* street names
        
        :param str dict_attr_in: Indicate specific dictionary key
        
        :returns: self._aligned_street_types
        :rtype: defaultdict(set) tuple of key, value

        :Example:

        >>> myOSMfile.audit_Street_Names()
        >>> pprint.pprint('Unknown Streets %s' % + myOSMfile.get_Aligned_Street_Names('unknown'))
        >>> pprint.pprint('Unknown Streets %s' % + myOSMfile.get_Aligned_Street_Names('mysterious'))
    
        .. seealso:: :func:`audit_Street_Names`
        .. warning:: first, function :func:`audit_Street_Names` needs to be executed, otherwise return value is None.
        .. todo:: execute first :func:`audit_Street_Names`.
        
        
        """            
        if dict_attr_in == '':
            return self._aligned_street_types
        else:
            return self._aligned_street_types[dict_attr_in]                 
                
    def audit_Phone_Numbers(self):
        """identifies incorrect phone numbers, not being compliant to:
        
        >>> phone_type_re = re.compile(r'(?=^\+[4][9][1-9]{1})[0-9]{6,15}', re.X)
        >>> phone_type_re2 = re.compile(r'(?=^((04)|((\+|00)49[0]?)))')
        >>> phone_eleminate_chars_re = re.compile('(\.|\(|\)|\-|\/|s)*', re.X)

        :Example:

        >>> myOSMfile.audit_Phone_Numbers()
        >>> pprint.pprint(myOSMfile.get_Aligned_Phone_Numbers()) 
        
        .. seealso:: :func:`get_Phone_Numbers` or :func:`get_Aligned_Phone_Numbers`
        .. todo:: execute first :func:`audit_Phone_Numbers`.
        
        
        """               
        phone_type_re = re.compile(r'(?=^\+[4][9][1-9]{1})[0-9]{6,15}', re.X)
        phone_type_re2 = re.compile(r'(?=^((04)|((\+|00)49[0]?)))')
        phone_eleminate_chars_re = re.compile('(\.|\(|\)|\-|\/|s)*', re.X) 

        mappingPhone = {  "00490" : "+49 (0)"
                        , "0049"  : "+49 (0)"
                        , "+49"   : "+49 (0)"
                        , "+490"  : "+49 (0)"
                        , "04"    : "+49 (0)4"
                       }

        def is_phone_number(elem):
            return (elem.attrib['k'] == 'phone')
               
        # Adding street names in dictionary good_format: original
        def audit_phone_type(phone_types, phone):
            #memorize for dictionary original xml value
            old_phone = phone

            # eliminate all whitespaces and special chars in the string
            phone = ''.join(phone.split())
            phone = phone_eleminate_chars_re.subn('', phone)[0]

            #Cross-ckeck now grouped phone number for validity for Hamburg, Germany region, starting with +49 (0)4
            m = phone_type_re.search(phone)
            
            if m:
                phone__pattern = m.group()   
                if phone_pattern not in phone_types:
                    phone_types[old_phone].add(phone)
            else:
                phone_types["unknown"].add(phone)
      
        def update_phone_number(phone, mappingPhone):
            m = phone_type_re2.search(phone)
            
            if m:
                phone_pre = mappingPhone[m.group(1)]   
                phone = phone.replace(m.group(1), phone_pre)
                phone = ' '.join(phone[i:i+9] for i in xrange(0, len(phone), 9))
            else:
                pass
            return phone
        
        #Main 
        ## Open file and find out discrepancies
        with co.open(self.xml_file, 'r', 'utf-8'):
            #street_types = defaultdict(set)
            for event, elem in ET.iterparse(self.xml_file, events=('start',)):
                if elem.tag == 'node' or elem.tag == 'way':
                    for tag in elem.iter('tag'):
                        if is_phone_number(tag):
                            audit_phone_type(self._phone_types, tag.attrib['v']) 
                
        ##Elimenate dicrepancies from given directory
        for phone_keys, phone_numbers in self._phone_types.iteritems():
            for phone_number in phone_numbers:
                self._aligned_phone_types[phone_number] = update_phone_number(phone_number, mappingPhone)

    def get_Phone_Numbers(self, dict_attr_in = ''):
        """returns private DefaultDict(set) of *original* phone numbers
        
        :param str dict_attr_in: Indicate specific dictionary key
        
        :returns: self._phone_types
        :rtype: defaultdict(set) tuple of key, value

        :Example:

        >>> myOSMfile.audit_Phone_Numbers()
        >>> pprint.pprint(myOSMfile.get_Aligned_Phone_Numbers()) 
        
        .. seealso:: :func:`audit_Phone_Numbers`
        .. warning:: first, function :func:`audit_Phone_Numbers` needs to be executed, otherwise return value is None.
        .. todo:: execute first :func:`audit_Phone_Numbers`.
        
        
        """            
        if dict_attr_in == '':
            return self._phone_types
        else:
            return self._phone_types[dict_attr_in]
    
    def get_Aligned_Phone_Numbers(self, dict_attr_in = ''):
        """returns private DefaultDict(set) of *updated & corrected* phone numbers
        
        :param str dict_attr_in: Indicate specific dictionary key

        :returns: self._aligned_phone_types
        :rtype: defaultdict(set) tuple of key, value

        :Example:

        >>> myOSMfile.audit_Phone_Numbers()
        >>> pprint.pprint(myOSMfile.get_Aligned_Phone_Numbers()) 
        
        .. seealso:: :func:`audit_Phone_Numbers`
        .. warning:: first, function :func:`audit_Phone_Numbers` needs to be executed, otherwise return value is None.
        .. todo:: execute first :func:`audit_Phone_Numbers`.
        
        
        """              
        if dict_attr_in == '':
            return self._aligned_phone_types
        else:
            return self._aligned_phone_types[dict_attr_in]                                
                
    def audit_Data_Chars(self):
        """identifies categories of characters (lower, lower_colon, problemchars, other) of XML file as private DefaultDict(int)
        
        lower = re.compile(r'^([a-z]|_)*$')
        lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
        problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

        :Example:

        >>> myOSMfile.audit_Data_Chars()
        >>> pprint.pprint(myOSMfile.get_Problematic_Chars()) 
        
        .. seealso:: :func:`get_Problematic_Chars`
        .. warning:: first, function :func:`get_Problematic_Chars` needs to be executed, otherwise return value is None.
        .. todo:: execute first :func:`get_Problematic_Chars`.
        
        
        """               
        lower = re.compile(r'^([a-z]|_)*$')
        lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
        problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
               
        def key_type(elem, data_structure):
            if elem.tag == 'tag':
                if lower.match(elem.attrib['k']):
                    data_structure['lower'] += 1
                elif lower_colon.match(elem.attrib['k']):
                    data_structure['lower_colon'] += 1
                elif problemchars.match(elem.attrib['k']):
                    data_structure['problemchars'] += 1
                else:
                    data_structure['other'] += 1
            return data_structure
        
        #Main
        with co.open(self.xml_file, 'r', 'utf-8'):
            for event, elem in ET.iterparse(self.xml_file, events=('start',)):
                self._data_structures = key_type(elem, self._data_structures)

    def get_Problematic_Chars(self):
        """returns categories of characters (lower, lower_colon, problemchars, other) of XML file as private DefaultDict(int)
        
        lower = re.compile(r'^([a-z]|_)*$')
        lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
        problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

        :returns: self._data_structures
        :rtype: defaultdict(int)

        :Example:

        >>> myOSMfile.audit_Data_Chars()
        >>> pprint.pprint(myOSMfile.get_Problematic_Chars()) 
        
        .. seealso:: :func:`audit_Data_Chars`
        .. warning:: first, function :func:`audit_Data_Chars` needs to be executed, otherwise return value is None.
        .. todo:: execute first :func:`audit_Data_Chars`.
        
        
        """           
        return self._data_structures                
                
    def audit_Unique_Values(self, elem_tag_in, elem_lookup_in):
        """returns private DefaultDict(int) of specified XML-Tag and XML-Attribute

        :param str elem_tag_in: 
        :param str elem_lookup_in: 

        :returns: self._unique_values
        :rtype: defaultdict(int)

        :Example:
        Receiving the Users and their Number of Contributions given by OSM XML file in decreasing order as dictionary:

        >>> myOSMfile.audit_Unique_Values('node', 'user')
        >>> pprint.pprint(myOSMfile.sort_Dictionary(myOSMfile.get_Unique_Values()))
        
        .. seealso:: :func:`get_Unique_Values` and :func:`sort_Dictionary`.
        .. warning:: first, function :func:`audit_Unique_Value` needs to be executed, otherwise return value is None.
        .. todo:: execute first :func:`audit_Unique_Value`.
        
        
        """               
        def get_unique_value(elem):
            unique_value = elem.attrib[elem_lookup_in]
            return unique_value
        
        #Main
        with co.open(self.xml_file, 'r', 'utf-8'):
            for event, elem in ET.iterparse(self.xml_file, events=('start',)):
                if elem.tag == elem_tag_in:
                    self._unique_values[get_unique_value(elem)] += 1

    def get_Unique_Values(self):
        """returns private DefaultDict(int) of specified XML-Tag and XML-Attribute

        :returns: self._unique_values
        :rtype: defaultdict(int)

        :Example:
        Receiving the Users and their Number of Contributions given by OSM XML file in decreasing order as dictionary:

        >>> myOSMfile.audit_Unique_Values('node', 'user')
        >>> pprint.pprint(myOSMfile.sort_Dictionary(myOSMfile.get_Unique_Values()))
        
        .. seealso:: :func:`audit_Unique_Value` and :func:`sort_Dictionary`.
        .. warning:: first, function :func:`audit_Unique_Value` needs to be executed, otherwise return value is None.
        .. todo:: execute first :func:`audit_Unique_Value`.
        
        
        """          
        return self._unique_values                    
                    
    def sort_Dictionary(self, dict_in, params_in='value'):
        """returns private DefaultDict(set) of *original* street names
        
        :param str params_in: If 'value' (standard) is indicated, input dictionary is returned sorted by its' value in reverse order (= True)
        If 'keys' is indicated, input dictionary is returned sorted by its' keys in ascending order (reverse = False).
        
        :returns: self._street_types
        :rtype: defaultdict(set)

        :Example:

        >>> myOSMfile.audit_Unique_Values('node', 'user')
        >>> pprint.pprint(myOSMfile.sort_Dictionary(myOSMfile.get_Unique_Values()))
    
        .. warning:: private DefaultDict need to be existing, otherwise return value is None.
        
        
        """ 
        if params_in == 'value':
            return sorted(dict_in.items(), key = lambda(keys, values): values, reverse=True)
        elif params_in == 'keys':
            return sorted(dict_in.items(), key = lambda(keys, values): keys, reverse=False) 
        else:
            return sorted(dict_in.keys(), key = lambda s: s.lower())
    
if __name__ == '__main__':
    # code for standalone use
    #myOSMfile = Investigation('OpenStreetMap-Hamburg-31.osm')
    #myOSMfile.view_Tags_Attributes()
    #pprint.pprint(myOSMfile.get_Tags_Attributes())
    
    #myOSMfile.count_Tags()
    #pprint.pprint(myOSMfile.get_Tags())    
    
    #myOSMfile.audit_Data_Chars()
    #pprint.pprint(myOSMfile.get_Problematic_Chars())    
    
    #myOSMfile.audit_Unique_Values('node', 'user')
    #pprint.pprint(myOSMfile.sort_Dictionary(myOSMfile.get_Unique_Values()))

    #myOSMfile.audit_Phone_Numbers()
    #pprint.pprint(myOSMfile.get_Aligned_Phone_Numbers())    
    
    #myOSMfile.audit_Zip_Codes()
    #pprint.pprint(myOSMfile.get_ZIP_Codes())
    
    #myOSMfile.audit_Street_Names()
    #pprint.pprint(myOSMfile.sort_Dictionary(myOSMfile.get_Street_Names()))
    #pprint.pprint(myOSMfile.get_Street_Names())
    #pprint.pprint('Unknown Streets %s' % + myOSMfile.get_Street_Names('unknown'))
    #pprint.pprint('Unknown Streets %s' % + myOSMfile.get_Street_Names('mysterious'))
    #sorted(myOSMfile.get_Aligned_Street_Names().keys())
    

