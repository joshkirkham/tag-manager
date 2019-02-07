"""
The lookup process resolves URNs to Item objects, and maintains the lookuptables
in db_files/lookuptables/

TODO Add a chaching mechanism to this. Or at least allow multiple things inside
        the same file to be replaced/added/removed at once
"""

from Item import *

class LookupP:
    def __init__(self, lut_path, logP, next_URN):
        """
        :param lut_path: Path to the lookup tables for the database
        :param logP:    The database's LogP object
        :param next_URN:  The next URN that has not been used in the LUT
        """
        self.logger = logP
        self.next_URN = next_URN
        self.lut_path = lut_path

        if lut_path[-1] != '/':
            self.lut_path += '/'

        logP.log("lookupP initialized with lookup table directory " + str(self.lut_path))




    def get_items(self, URN_list):
        """Returns item objects with all of the URNs requested in the URN_list
        :param URN_list: The list of integer URNs to resolve. This should be sorted and all URNs
                        should be in bounds (less than current max URN)
        :throws Exception if a URN in URN_list is out of bounds
        """
        if URN_list == []:
            return []


        items = []  # List of Item objects to be returned
        current_filename = ""  # Which .lut file is open currently
        file = None

        for URN in URN_list:
            if int(URN) >= self.next_URN:
                self.logger.log("Tried to access out of bounds URN: "+str(URN))
                raise Exception("URN " + str(URN) + "Out of Bounds")

            needed_filename = self.compute_file(URN)

            # Open the proper file for the next URN to grab
            if current_filename != needed_filename:
                if current_filename != "":
                    file.close()
                current_filename = needed_filename
                file = open(current_filename, 'r')
                lines = file.readlines()

            items.append(Item.generate_item_from_string(lines[URN % 1000]))

        if file is not None:
            file.close()

        return items



    def add_item(self, item):
        """

        :param item: An Item object. If the Item has a defined URN, it will be ignored and
                    replaced with the next available URN
        :return:
        """

        item.URN = self.next_URN
        self.next_URN += 1

        item_string = item.string()

        # Open and append the new item to the appropriate .lut file
        needed_file = self.compute_file(item.URN)
        file = open(self.lut_path + needed_file, 'a+')
        file.write(item_string + "\n")
        file.close()


    def remove_item(self, urn):
        """
        Remove an item from the lookup table.
        :param urn: Integer URN to be removed
        :return: True if the item was removed, False if it was not
        """
        needed_lut_file = self.compute_file(urn)

        # Read the contents of the file
        file = open(needed_lut_file, 'r')
        lines = file.readlines()

        # Remove the desired URN
        remove_index = self.find_item_index(lines, urn)
        if remove_index >= 0:
            del lines[remove_index]
        else:
            return False

        file.close()

        # Write it back to the file
        file = open(needed_lut_file, 'w')
        file.writelines(lines)
        file.close()

        return True


    def replace_item(self, to_replace, new_item):
        """
        Replaces the LUT entry corresponding to a given URN with a new item.
        :param to_replace: The URN of the entry to be replaced
        :param new_item:  The Item object of the replacement item. If the replacement item already has
                            a URN it is ignored and overwritten.
        :return: True if the item was replaced, False if it was not
        """
        # Find and read the needed .lut file
        needed_lut_file = self.compute_file(to_replace)
        file = open(needed_lut_file, 'r')
        lines = file.readlines()
        file.close()

        # Edit the new Item's fields
        new_item.URN = to_replace

        # Find and replace the desired entry
        replace_index = self.find_item_index(lines, to_replace)
        if replace_index >= 0:
            lines[replace_index] = new_item.string()
        else:
           return False

        file = open(needed_lut_file, 'w')
        file.writelines(lines)
        file.close()
        return True




    def compute_file(self, urn):
        return self.lut + str(urn // 1000) + ".lut"



    def find_item_index(self, user_list, urn):
        """Search the user list for an entry beginning with urn
        :param user_list: The list of users to search
        :param urn: Integer URN
        :return: The index of the urn in the user_list if the urn is located, -1 if it is not
        """
        for i in range(0, len(user_list)):
            user = user_list[i]
            if str(urn) == user[i][1:user.find(':')]:
                return i

        return -1



    def close(self):
        return self.next_URN
        #export the next urn back to the database
        pass

