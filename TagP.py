"""
The tag process is responsible for managing the databases tag lookups
All tag files are in lower case
TODO Add a chaching mechanism for tags
"""

import os


class TagP:
    def __init__(self, tag_dir, logP):
        """
        :param tabledir: The location of the "tagfiles" directory to be used
        """
        self.logger = logP
        self.tag_files_path= tag_dir

        if self.tag_files_path[-1] != '/':
            self.tag_files_path += '/'

        self.logger.log("TagP initialized with tag file directory " + self.tag_files_path)



    def process_query(self, query_list):
        """
        Given a list of tag names, return all URNs who are in the intersection of those tags
        :param query_list: List of tag names to search for
        :return: A list of URNs in increasing order each of which are associated all tags in the query
        """
        #List of lists of UIDs from each tag
        tag_list = []

        # Turn all tag names into lower case
        self.sanitize_tag_input(query_list)

        # Add a list of UIDs for each tag in the query
        for tag in query_list:
            try:
                file = open(self.tag_files_path + tag + ".tag", 'r')
                UID_buffer = []
                for line in file:
                    UID_buffer.append(int(line))
                tag_list.append(UID_buffer)

            except FileNotFoundError:
                print('Tag: ' + tag + ' does not exist in the lookuptable')

            else:
                file.close()

        # Find the items duplicated in all lists of UIDs
        if len(tag_list) <= 1:
            return tag_list

        duplicates = tag_list[0]
        for i in range(1, len(tag_list)):
            duplicates = list(set(duplicates).intersection(set(tag_list[i])))
        self.logger.log("Successfully processed query for " + str(query_list))
        return duplicates




    def add_tag(self, tag):
        """
        Adds a tag to the databases tagfiles directory. If the tag already exists,
        nothing happens
        :param tag: The string name of the tag to be added
        :return: True if the tag was added, or already existed, False otherwise.
        """
        tag = tag.lower()

        try:
            file = open(self.tag_files_path + tag + ".tag", 'w+')
            self.logger.log("Added tag: " + tag + " to " + self.tag_files_path)
        except FileNotFoundError:
            print("Directory self.tagfiles could not be found")
            return False
        else:
            file.close()

        return True



    def remove_tag(self, tag):
        """
        Removes a tag file from the tag files
        :param tag: The name of the tag to be removed
        :return: True if it was removed, false if it wasn't.
        """
        tag = tag.lower()
        try:
            os.remove(self.tag_files_path + tag + ".tag")
        except OSError:
            return False

        return True



    def list_tags(self):
        """
        :return: An alphabetically sorted list of all the current tags
        """
        tag_list = sorted(os.listdir(self.tag_files_path))

        # Remove ".tag" suffix
        for i in range(0, len(tag_list)):
            tag_list[i] = tag_list[i][:-4]

        return tag_list




    def add_urn(self, URN, add_list):
        """
        Appends a URN into each of the tag files listed
        :param URN: An int of the URN to be added
        :param add_list: A list of tag names to add the URN to
        :return: The number of tags the URN was successfully added to
        """
        # Counter for the number of tag files the URN has been added to
        num_tags_added = 0

        current_tag_list = self.list_tags()
        self.sanitize_tag_input(add_list)

        # Try to append the URN to the tag file for each tag in add_list
        for tag in add_list:
            if tag  in current_tag_list:
                try:
                    file = open(self.tag_files_path + tag + ".tag", 'a')
                    file.write(str(URN) + '\n')
                    file.close()
                    num_tags_added += 1
                except FileNotFoundError:
                    self.logger.log("Failed to add urn to the tag " + tag)
                    self.logger.log('lookupP.add_URN(): The tag \" ' + tag + '\" does not exist')

        # Log the result
        self.logger.log("add_urn successfully added " + str(num_tags_added) + "/"
                        + str(len(add_list)) + "tags")

        return num_tags_added




    def remove_urn(self, URN, rem_list=None):
        """
        Removes a URN from all tags specified, or all existing tags if none
        are specified
        :param URN: An integer URN to be removed from 0 or more tags.
        :param rem_list: A list of tags to remove URN from. If it is None,
                        the URN will be removed from all tags.
        :return: The number of tags the URN was successfully removed from.
        """
        # A counter for how many tags the URN has been removed from
        rem_count = 0

        if rem_list is None:
            rem_list = self.list_tags()

        for tag in rem_list:
            try:
                file = open(self.tag_files_path + tag + ".tag", 'r')
                lines = file.readlines()
                file.close()

                lines.remove(str(URN) + "\n")
                file = open(self.tag_files_path + tag + ".tag" 'w')

                file.writelines(lines)
                file.close()
                rem_count += 1
                self.logger.log("Removed URN " + URN + "from " + str(file))

            except FileNotFoundError:
                self.logger.log("Failed to remove URN " + str(URN) + "from tag")
                self.logger.log('The file \" '+ tag+".tag"+'\" does not exist')

        self.logger.log("Removed " + str(URN) + " from " + str(rem_count) + "/" + str(len(rem_list))
                        + " specified tag files")

        return rem_count



    def sanitize_tag_input(self, tag_list):
        """
        Convert all tag names in a list to lower case
        :param tag_list: The list of tags to convert
        """
        for i in range(0, len(tag_list)):
            tag_list[i] = tag_list[i].lower()



    def close(self):
        pass
