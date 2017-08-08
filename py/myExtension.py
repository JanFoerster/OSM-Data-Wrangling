
# coding: utf-8

# In[4]:

#!/usr/bin/env python


"""writes Unicode Dictionary to CSV file.

.. module:: myExtension
   :platform: Windows
   :synopsis: A useful module indeed.

.. moduleauthor:: Jan Foerster <jan.foerster@airbus.com>


"""

#__license__ = 'Jan FOERSTER'
#__revision__ = ' $Id: MyXML.py 1 2017-07-30 09:27:45z cokelaer $ '
#__docformat__ = 'reStructuredText'

import xml.etree.cElementTree as ET
from collections import defaultdict
from jfo.schema import schema
import re, pprint, csv, codecs, cerberus

class myUnicodeDictWriter(csv.DictWriter, object):
    """myUnicodeDictWriter class. Writes Dictionary to CSV files with Unicode characters.
 
    .. class:: myUnicodeDictWriter
       Initializes only private variables, containing results of callable methods.

       :method: :func:`writerow`
       :method: :func:`writerows`
       
       
    """ 
    def writerow(self, row):
        """writes one row as unicoded row. Instance of Super-Instance csv.DictWriter.
        
        :Example:

        >>> nodes_writer.writerow(el['node'])
        
        .. seealso:: :func:`writerows`.
        
        
        """ 
        super(myUnicodeDictWriter, self).writerow({
            key: (value.encode('utf-8') if isinstance(value, unicode) else value) for key, value in row.iteritems()
        })

    def writerows(self, rows):
        """writes several rows as unicoded row. Instance of Super-Instance csv.DictWriter.
        
        :Example:

        >>> node_tags_writer.writerows(el['node_tags'])
        
        .. seealso:: :func:`writerow`.
        
        
        """ 
        for row in rows:
            self.writerow(row)
            

class myDict2CSVTransformer(object):
    """myDict2CSVTransformer class. Reads OSM XML file into dictionary, validates content and creates CSV files.

    .. class:: myDict2CSVTransformer
       Initializes only private variables, containing results of callable methods.

       :method: :func:`start_Transformation`


    """ 

    #Initializing Class
    def __init__(self, xml_file_in):
        self._xml_file_in = xml_file_in

       
        
    def start_Transformation(self, validate = True):
    #def start_Transformation(file_in, validate = True):
        """Iteratively process each XML element and write to csv(s)

        :param str file_in: Absolute path and name of XML file
        :param bool validate: If Validation of package Cerberus shall be done.(True is standard)

        :Example:

        >>> myHamburgTransformer = myDict2CSVTransformer('OpenStreetMap-Hamburg-31.osm')
        >>> myHamburgTransformer.start_Transformation()

        .. note:: If validation is selected, execution of script can take up to 15 times longer.
        """ 
        # Fields of new csv files
        # Make sure the fields order in the csvs matches the column order in the 
        # sql table schema
        NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
        NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
        WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
        WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
        WAY_NODES_FIELDS = ['id', 'node_id', 'position']

        # Path to new csv files
        NODES_PATH = "nodes.csv"
        NODE_TAGS_PATH = "nodes_tags.csv"
        WAYS_PATH = "ways.csv"
        WAY_NODES_PATH = "ways_nodes.csv"
        WAY_TAGS_PATH = "ways_tags.csv" 
        
        # Importing schema for transformation from schema.py file
        SCHEMA = schema

        # Regular expression compilers
        PROBLEMCH = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

        # Validating element to match schema
        def validate_element(element, validator, schema=SCHEMA):
            """Raise ValidationError if element does not match schema"""
            if validator.validate(element, schema) is not True:
                field, errors = next(validator.errors.iteritems())
                message_string = "\nElement of type '{0}' has the following errors:\n{1}"
                error_strings = (
                    "{0}: {1}".format(k, v if isinstance(v, str) else ", ".join(v))
                    for k, v in errors.iteritems()
                )
                raise cerberus.ValidationError(
                    message_string.format(field, "\n".join(error_strings))
                )

        def get_element(xml_file_in, tags=('node', 'way', 'relation')):
            """Yield element if it is the right type of tag"""
            context = ET.iterparse(xml_file_in, events=('start', 'end'))
            _, root = next(context)
            for event, elem in context:
                if event == 'end' and elem.tag in tags:
                    yield elem
                    root.clear()

        # Main function for transformation of XML data to Python dict
        def shape_element(element
                          , node_attr_fields=NODE_FIELDS
                          , way_attr_fields=WAY_FIELDS
                          , prob_ch=PROBLEMCH
                          , default_tag_type='regular'
                         ):

            tag_attribs = {}
            way_nodes = []
            tags = []
            count = 0

            if element.tag == 'node':
                tagfields = node_attr_fields
            elif element.tag == 'way':
                tagfields = way_attr_fields

            if element.tag == 'node' or 'way':
                for attrib in element.attrib:
                    if attrib in tagfields:
                        tag_attribs[attrib] = element.attrib[attrib]

            for subelem in element:
                if subelem.tag == 'tag' and prob_ch.match(subelem.attrib['k']) == None:
                    tag = {}
                    tag['id'] = tag_attribs['id']
                    tag['value'] = subelem.attrib['v']
                    key = subelem.attrib['k']
                    tag['key'] = key[key.find(':') + 1:]
                    if ':' in key:
                        tag['type'] = key[:key.find(':')]
                    else:
                        tag['type'] = default_tag_type
                    tags.append(tag)
                elif subelem.tag == 'nd':
                    way_node = {}
                    way_node['id'] = tag_attribs['id']
                    way_node['node_id'] = subelem.attrib['ref']
                    way_node['position'] = count
                    count += 1
                    way_nodes.append(way_node)

            if element.tag == 'node':
                return {'node': tag_attribs, 'node_tags': tags}
            elif element.tag == 'way':
                return {'way': tag_attribs, 'way_nodes': way_nodes, 'way_tags': tags}

        #Main process_map
        with codecs.open(NODES_PATH, 'w') as nodes_file,             codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file,             codecs.open(WAYS_PATH, 'w') as ways_file,             codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file,             codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

                nodes_writer = myUnicodeDictWriter(nodes_file, NODE_FIELDS)
                node_tags_writer = myUnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
                ways_writer = myUnicodeDictWriter(ways_file, WAY_FIELDS)
                way_nodes_writer = myUnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
                way_tags_writer = myUnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

                nodes_writer.writeheader()
                node_tags_writer.writeheader()
                ways_writer.writeheader()
                way_nodes_writer.writeheader()
                way_tags_writer.writeheader()

                validator = cerberus.Validator()

                for element in get_element(self._xml_file_in, tags=('node', 'way')):
                    el = shape_element(element)
                    if el:
                        if validate is True:
                            validate_element(el, validator)

                        if element.tag == 'node':
                            nodes_writer.writerow(el['node'])
                            node_tags_writer.writerows(el['node_tags'])
                        elif element.tag == 'way':
                            ways_writer.writerow(el['way'])
                            way_nodes_writer.writerows(el['way_nodes'])
                            way_tags_writer.writerows(el['way_tags'])    

if __name__ == '__main__':
    #code for standalone use 
    #Note: Validation is ~ 15X slower. Consider using a small
    #myHamburgTransformer = myDict2CSVTransformer('OpenStreetMap-Hamburg-31.osm')
    #myHamburgTransformer.start_Transformation()
    #start_Transformation('OpenStreetMap-Hamburg-31.osm')

