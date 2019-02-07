# DESCRIPTION
# This file contains code for representing Items, individual pieces of content stored in the db.
# An Item will contain a file-path to the content, as well as metadata about it.
# -The Item Class
# -A method to generate items from strings

#TODO add language
#TODO figgure out all the things that Item needs to contain
class Item():
    # The Item class represents an individual piece of content in the db and the metadata associated with it

    def __init__(self, urn, filepath, title, thumbnail, filetype, description, rating,  tags):
        """
        :param urn:         The URN of the item. An integer.
        :param filepath:    A string of the relative filepath within the datafiles
        :param title:       The title of the Item. "" if no title
        :param thumbnail:   A filepath to the thumbnail of the image. "" If the filepath is the thumbnail
        :param filetype:    A string representing the file type. (dir for directories, file extension for everything else)
        :param description: A short description of the file
        :param rating:      An integer from 1 to 10
        :param tags:        A list of strings of tag names
        """
        self.URN = urn #integer
        self.filepath = filepath
        self.title = title
        self.thumbnail = thumbnail
        self.filetype = filetype
        self.description = description
        self.rating = rating #integer
        self.tags = tags
        # self.author = author





    def string(self):
        """
        :return: A string representation of the Item. The URN must be the first element. All object
        attributes are converted to strings and separated by ":"s. The list of tags is separated by
        ";"s.

        Example: [URN:filepath:title:thumbnail-path:description:rating:tag1;tag2;:]
        """
        tag_string = ''
        for tag in self.tags:
            tag_string = tag_string + tag + ';'

        string = '[' + str(self.URN) + ':' \
             + self.filepath + ':' + \
             self.title + ':' + \
             self.thumbnail + ':' + \
             self.filetype + ':' + \
             self.description + ':' +\
             str(self.rating) + ':' + \
             tag_string + ':]'

        return string

    # ============= End Item class =================



def generate_item_from_string(s):
    """
    :param s: The string to parse
    :return: A new Item object whose .string() method would produce s
    """
    attr = s[1:-1].split(':')

    return Item(int(attr[0]),
                attr[1], attr[2], attr[3],
                attr[4], attr[5].replace('\n', '\t'), int(attr[6]),
                attr[7][0:-1].split(';')) #splitting the tag string by ; and getting rid of last ;



def cmp_URN(item1, item2):
    """
    Compares two item objects by their URN
    :return:    0 if equal
                negative int if item1 < item 2
                positive int if item1 > item2
   """
    return item1.URN - item2.URN



def cmp_rating(item1, item2):
    """Compares two item objects by their rating
    :return:    0 if equal
                negative int if item1 < item 2
                positive int if item1 > item2
   """
    return item1.rating - item2.rating



def cmp_name(item1, item2):
    """Compares two item objects by their name
    :return:    0 if equal
                negative int if item1 < item 2
                positive int if item1 > item2
   """
    if item1.title < item2.title:
        return -1
    if item1.title > item2.title:
        return 1
    return 0
