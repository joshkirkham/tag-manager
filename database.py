"""
The Database object is responsible for managing the database files, and processing
user requests to edit them.
"""

import os

from Item import *
from LogP import LogP
from LookupP import LookupP
from SettingsP import SettingsP
from TagP import TagP

class Database:
    def __init__(self, dir):
        """
        :param dir: String of the directory with the db files in it. The required structure
                    of this directory is specified in the documentation
                    This should be an absolute path.
        """

        self.dir = dir
        if dir[-1] != '/':
            dir += '/'

        print(self.dir)
        # Ensure that necessary files exist, and allocated process classes to their
        # relevant portions of the database files
        if os.path.isdir(self.dir + "datafiles/") and \
                os.path.isdir(self.dir + "lookuptables/") and \
                os.path.isdir(self.dir + "tagfiles/") and \
                os.path.isfile(self.dir + "log") and \
                os.path.isfile(self.dir + "settings"):


            # Get the settings from the settings file first
            self.settingsP = SettingsP(self.dir + 'settings')


            self.logP = LogP(self.dir + 'log',
                             int(self.settingsP.resolve("MAX_LOG_SIZE")),
                             int(self.settingsP.resolve("LOG_BUFF_SIZE")))

            self.lookupP = LookupP(self.dir + "lookuptables/", self.logP,
                                   int(self.settingsP.resolve("NEXT_URN")))

            self.tagP = TagP(self.dir + "tagfiles/", self.logP)

        else:
            print("ERROR: Could not load necessary files from " + self.dir)
            exit(2)

        self.logP.log("=============== Database successfully initialized at: " + self.dir + " ===============")



    def close(self):
        """Close down the database, write any cached data, and prepare for the
        deletion of the database object"""

        next_urn = self.lookupP.close()
        self.settingsP.change_setting("NEXT_URN", str(next_urn))

        self.tagP.close()
        self.settingsP.close()
        self.logP.log("########## Closing Database Down ##########")
        self.logP.close()





def test_functionality():
   db_path = "C:/Users/josh/PycharmProjects/tagdb/database_files/"
   db = Database(db_path)
   db.tagP.add_tag("test")
   db.close()



if __name__ == "__main__":
    test_functionality()


#TODO Implement this functionality later, just test what you have going now
"""
    T
    def query(self, tag_list, sorting=None):
        
        Resolves a querey on the db. Returns a list of item objects which
        satisfy the query sorted in the specified manner

        :param tag_list: The list of tags to query for
        :param sorting: A function in the item class. Defaults to cmp_URN
        :return: A sorted list of objects
       
        URNs = sorted(self.tagP.process_query(tag_list))
        items = self.lookupP.get_items(URNs)
        if sorting == None:
            sorting = cmp_URN
        qsort(items, left, right, sorting)
        return items

    def add(self, item):
        existing_tags = self.tagP.list_current_tags()
        for tag in item.tags:
            if tag not in existing_tags:
                self.tagP.add_tag(tag)





def qsort(items, left, right, sorting):

    wall = left

    swap(items, left, (left + right) / 2)

    for i in range(left + 1, right + 1):
        if sorting(items[i], items[left]) < 0:
            wall += 1
            swap(items, wall, i)

    swap(items, wall, left)

    qsort(items, left, wall, sorting)
    qsort(items, wall+1, right, sorting)



def swap(arr, a, b):
    temp = arr[a]
    arr[a] = arr[b]
    arr[b] = temp



"""


