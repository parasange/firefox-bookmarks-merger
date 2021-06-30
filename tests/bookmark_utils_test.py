import json
import os
import unittest

from firefox_bookmarks_merger import bookmark_utils
from firefox_bookmarks_merger import file_operations
from difflib import Differ

global test_file1, test_file2

test_file1 = "../tests/testcase1.json"
test_file2 = "../tests/testcase2.json"

def load_testcase(self, filename):

    bookmarks_object_wrapper = file_operations.load_bookmarks_file(filename)
    bookmarks_object = bookmarks_object_wrapper.get("json")

    self.assertIsNotNone(bookmarks_object)
    self.assertIsInstance(type(bookmarks_object), type(dict))

    return bookmarks_object

def compare_files(self, test_file, test_output, remove_output=True, debug_print = False):

    with open(test_file) as expected, open(test_output) as output:
        differ = Differ()
        for line in differ.compare(expected.readlines(), output.readlines()):
            if debug_print:
                print(line)
            self.assertEqual(line.startswith(' '), True)

    expected.close()
    output.close()

    if remove_output:
        os.remove(test_output)

class BookmarksMergerIOMethods(unittest.TestCase):

    def test_write_tree_to_txt(self):
        print("\n[UNITTEST] test_write_tree_to_txt()")

        def run_testcase_1():

            print("[UNITTEST]\t\t... run_testcase_1")
            bookmarks_object = load_testcase(self, test_file1)

            expected_file = "../tests/expected/testcase1_tree_to_file_expected.txt"
            test_output = "../tests/testcase1_tree_to_file.txt"

            output = open(test_output, "w")
            file_operations.write_tree_to_txt(bookmarks_object, output)
            output.close()

            compare_files(self, expected_file, test_output)

        def run_testcase_2():

            print("[UNITTEST]\t\t... run_testcase_2")
            bookmarks_object = load_testcase(self, test_file2)

            expected_file = "../tests/expected/testcase2_tree_to_file_expected.txt"
            test_output = "../tests/testcase2_tree_to_file.txt"

            output = open(test_output, "w")
            file_operations.write_tree_to_txt(bookmarks_object, output)
            output.close()

            compare_files(self, expected_file, test_output)

        run_testcase_1()
        run_testcase_2()

    def test_write_tree_to_json(self):
        print("\n[UNITTEST] test_write_tree_to_json()")

        def run_testcase_1():
            print("[UNITTEST]\t\t... run_testcase_1")

            bookmarks_object = load_testcase(self, test_file1)

            test_output = test_file1[0:-5] + "_tree_to_json_copy.json"
            file_operations.write_tree_to_json(test_output, bookmarks_object)

            compare_files(self, test_file1, test_output)

        def run_testcase_2():
            print("[UNITTEST]\t\t... run_testcase_2")

            bookmarks_object = load_testcase(self, test_file2)

            test_output = test_file2[0:-5] + "_tree_to_json_copy.json"
            file_operations.write_tree_to_json(test_output, bookmarks_object)

            compare_files(self, test_file2, test_output)

        run_testcase_1()
        run_testcase_2()

class BookmarksMergerBasicMethods(unittest.TestCase):

    def test_get_bookmark_children_from_rootFolder(self):
        print("\n[UNITTEST] test_get_bookmark_children_from_rootFolder()")

        def run_testcase_1():
            print("[UNITTEST]\t\t... run_testcase_1")

            bookmarks_object = load_testcase(self, test_file1)
            [json_root, bookmarks] = bookmark_utils.get_bookmark_children(bookmarks_object)

            self.assertIsNotNone(json_root)
            self.assertIsNotNone(bookmarks)
            self.assertEqual(json_root.get("children"), [])
            self.assertEqual(len(bookmarks), 3)

        def run_testcase_2():
            print("[UNITTEST]\t\t... run_testcase_2")

            bookmarks_object = load_testcase(self, test_file2)
            [json_root, bookmarks] = bookmark_utils.get_bookmark_children(bookmarks_object)

            self.assertIsNotNone(json_root)
            self.assertIsNotNone(bookmarks)
            self.assertEqual(json_root.get("children"), [])
            self.assertEqual(len(bookmarks), 3)

        run_testcase_1()
        run_testcase_2()

    def test_get_bookmark_children_from_toolbarFolder(self):
        print("\n[UNITTEST] test_get_bookmark_children_from_toolbarFolder()")

        def run_testcase_1():
            print("[UNITTEST]\t\t... run_testcase_1")

            bookmarks_object = load_testcase(self, test_file1)
            [json_root, bookmarks] = bookmark_utils.get_bookmark_children(bookmarks_object, "toolbarFolder")

            self.assertIsNotNone(json_root)
            self.assertIsNotNone(bookmarks)
            self.assertEqual(json_root.get("children"), [])
            self.assertEqual(len(bookmarks), 2)

        def run_testcase_2():
            print("[UNITTEST]\t\t... run_testcase_2")

            bookmarks_object = load_testcase(self, test_file2)
            [json_root, bookmarks] = bookmark_utils.get_bookmark_children(bookmarks_object, "toolbarFolder")

            self.assertIsNotNone(json_root)
            self.assertIsNotNone(bookmarks)
            self.assertEqual(json_root.get("children"), [])
            self.assertEqual(len(bookmarks), 3)


        run_testcase_1()
        run_testcase_2()

    def test_get_bookmark_children_from_menuFolder(self):
        print("\n[UNITTEST] test_get_bookmark_children_from_menuFolder()")

        def run_testcase_1():
            print("[UNITTEST]\t\t... run_testcase_1")

            bookmarks_object = load_testcase(self, test_file1)
            [json_root, bookmarks] = bookmark_utils.get_bookmark_children(bookmarks_object, "bookmarksMenuFolder")

            self.assertIsNotNone(json_root)
            self.assertIsNotNone(bookmarks)
            self.assertEqual(json_root.get("children"), [])
            self.assertEqual(len(bookmarks), 3)

        def run_testcase_2():
            print("[UNITTEST]\t\t... run_testcase_2")

            bookmarks_object = load_testcase(self, test_file2)
            [json_root, bookmarks] = bookmark_utils.get_bookmark_children(bookmarks_object, "bookmarksMenuFolder")

            self.assertIsNotNone(json_root)
            self.assertIsNotNone(bookmarks)
            self.assertEqual(json_root.get("children"), [])
            self.assertEqual(len(bookmarks), 3)

        run_testcase_1()
        run_testcase_2()

    def test_get_bookmark_children_from_unfiledFolder(self):
        print("\n[UNITTEST] test_get_bookmark_children_from_unfiledFolder()")

        def run_testcase_1():
            print("[UNITTEST]\t\t... run_testcase_1")

            bookmarks_object = load_testcase(self, test_file1)
            [json_root, bookmarks] = bookmark_utils.get_bookmark_children(bookmarks_object, "unfiledBookmarksFolder")

            self.assertIsNotNone(json_root)
            self.assertIsNotNone(bookmarks)
            self.assertEqual(json_root.get("children"), [])
            self.assertEqual(len(bookmarks), 3)

        def run_testcase_2():
            print("[UNITTEST]\t\t... run_testcase_2")

            bookmarks_object = load_testcase(self, test_file2)
            [json_root, bookmarks] = bookmark_utils.get_bookmark_children(bookmarks_object, "unfiledBookmarksFolder")

            self.assertIsNotNone(json_root)
            self.assertIsNotNone(bookmarks)
            self.assertEqual(json_root.get("children"), [])
            self.assertEqual(len(bookmarks), 3)

        run_testcase_1()
        run_testcase_2()

    def test_get_bookmark_children_from_bad_location(self):
        print("\n[UNITTEST] test_get_bookmark_children_from_bad_location()")

        def run_testcase_1():
            print("[UNITTEST]\t\t... run_testcase_1")

            bookmarks_object = load_testcase(self, test_file1)
            [json_root, bookmarks] = bookmark_utils.get_bookmark_children(bookmarks_object, "badLocation")

            self.assertIsNone(json_root)
            self.assertIsNone(bookmarks)

        def run_testcase_2():
            print("[UNITTEST]\t\t... run_testcase_2")

            bookmarks_object = load_testcase(self, test_file2)
            [json_root, bookmarks] = bookmark_utils.get_bookmark_children(bookmarks_object, "badLocation")

            self.assertIsNone(json_root)
            self.assertIsNone(bookmarks)

        run_testcase_1()
        run_testcase_2()

    def test_set_bookmark_children(self):
        print("\n[UNITTEST] test_set_bookmark_children()")

        def run_testcase_1():
            print("[UNITTEST]\t\t... run_testcase_1")

            bookmarks_object = load_testcase(self, test_file1)
            [json_root, bookmarks] = bookmark_utils.get_bookmark_children(bookmarks_object)

            self.assertIsNotNone(json_root)
            self.assertIsNotNone(bookmarks)
            self.assertEqual(json_root.get("children"), [])
            self.assertEqual(len(bookmarks), 3)

            merged_bookmarks = bookmark_utils.set_bookmark_children(json_root, bookmarks)
            self.assertEqual(len(merged_bookmarks), 5)

        def run_testcase_2():
            print("[UNITTEST]\t\t... run_testcase_2")

            bookmarks_object = load_testcase(self, test_file2)
            [json_root, bookmarks] = bookmark_utils.get_bookmark_children(bookmarks_object)

            self.assertIsNotNone(json_root)
            self.assertIsNotNone(bookmarks)
            self.assertEqual(json_root.get("children"), [])
            self.assertEqual(len(bookmarks), 3)

            merged_bookmarks = bookmark_utils.set_bookmark_children(json_root, bookmarks)
            self.assertEqual(len(merged_bookmarks), 5)


        run_testcase_1()
        run_testcase_2()

    def test_strip_ids_in_tree(self):
        print("\n[UNITTEST] test_strip_ids_in_tree()")

        def run_testcase_1():
            print("[UNITTEST]\t\t... run_testcase_1")

            bookmarks_object = load_testcase(self, test_file1)

            bookmarks_object_length = len(bookmarks_object)
            bookmark_utils.strip_ids_in_tree(bookmarks_object)
            self.assertEqual(bookmarks_object_length, len(bookmarks_object))

            [json_root, bookmarks] = bookmark_utils.get_bookmark_children(bookmarks_object, flatten=True)
            self.assertIsNotNone(json_root)
            self.assertIsNotNone(bookmarks)
            self.assertEqual(json_root.get("children"), [])
            self.assertEqual(len(bookmarks), 9)

            for flattened_bookmark in bookmarks:
                self.assertEqual(flattened_bookmark.get("id"), None)
                self.assertEqual(flattened_bookmark.get("guid"), None)
                self.assertEqual(flattened_bookmark.get("index"), None)

        def run_testcase_2():
            print("[UNITTEST]\t\t... run_testcase_2")

            bookmarks_object = load_testcase(self, test_file2)

            bookmarks_object_length = len(bookmarks_object)
            bookmark_utils.strip_ids_in_tree(bookmarks_object)
            self.assertEqual(bookmarks_object_length, len(bookmarks_object))

            [json_root, bookmarks] = bookmark_utils.get_bookmark_children(bookmarks_object, flatten=True)
            self.assertIsNotNone(json_root)
            self.assertIsNotNone(bookmarks)
            self.assertEqual(json_root.get("children"), [])
            self.assertEqual(len(bookmarks), 9)

            for flattened_bookmark in bookmarks:
                self.assertEqual(flattened_bookmark.get("id"), None)
                self.assertEqual(flattened_bookmark.get("guid"), None)
                self.assertEqual(flattened_bookmark.get("index"), None)


        run_testcase_1()
        run_testcase_2()

class BookmarksMergerPrivateMethods(unittest.TestCase):

    def test_flatten_bookmarks(self):
        print("\n[UNITTEST] test_flatten_bookmarks()")

        def run_testcase_1():
            print("[UNITTEST]\t\t... run_testcase_1")

            bookmarks_object = load_testcase(self, test_file1)
            [json_root, bookmarks] = bookmark_utils.get_bookmark_children(bookmarks_object, flatten=True)

            self.assertIsNotNone(json_root)
            self.assertIsNotNone(bookmarks)
            self.assertEqual(json_root.get("children"), [])
            self.assertEqual(len(bookmarks), 9)

        def run_testcase_2():
            print("[UNITTEST]\t\t... run_testcase_2")

            bookmarks_object = load_testcase(self, test_file2)
            [json_root, bookmarks] = bookmark_utils.get_bookmark_children(bookmarks_object, flatten=True)

            self.assertIsNotNone(json_root)
            self.assertIsNotNone(bookmarks)
            self.assertEqual(json_root.get("children"), [])
            self.assertEqual(len(bookmarks), 9)

        run_testcase_1()
        run_testcase_2()

class BookmarksMergerCleanMethods(unittest.TestCase):

    def test_clean_bookmark_children_from_menuFolder(self):
        print("\n[UNITTEST] test_clean_bookmark_children_from_menuFolder()")

        def run_testcase_1():
            print("[UNITTEST]\t\t... run_testcase_1")

            bookmarks_object = load_testcase(self, test_file1)
            bookmarks_object_cleaned = bookmark_utils.clean(bookmarks_object, "bookmarksMenuFolder", False)

            children = bookmarks_object_cleaned.get("children")

            self.assertEqual(len(bookmarks_object_cleaned.get("children")), 3)

        def run_testcase_2():
            print("[UNITTEST]\t\t... run_testcase_2")

            bookmarks_object = load_testcase(self, test_file2)
            bookmarks_object_cleaned = bookmark_utils.clean(bookmarks_object, "bookmarksMenuFolder", False)

            children = bookmarks_object_cleaned.get("children")

            self.assertEqual(len(bookmarks_object_cleaned.get("children")), 3)

        run_testcase_1()
        run_testcase_2()

    def test_clean_bookmark_children_from_menuFolder_and_merge_folder(self):
        print("\n[UNITTEST] test_clean_bookmark_children_from_menuFolder_and_merge_folder()")

        def run_testcase_1():
            print("[UNITTEST]\t\t... run_testcase_1")

            bookmarks_object = load_testcase(self, test_file1)
            bookmarks_object_cleaned = bookmark_utils.clean(bookmarks_object, "bookmarksMenuFolder")

            self.assertEqual(len(bookmarks_object_cleaned.get("children")), 3)

        def run_testcase_2():
            print("[UNITTEST]\t\t... run_testcase_2")

            bookmarks_object = load_testcase(self, test_file2)
            bookmarks_object_cleaned = bookmark_utils.clean(bookmarks_object, "bookmarksMenuFolder")

            self.assertEqual(len(bookmarks_object_cleaned.get("children")), 3)

        run_testcase_1()
        run_testcase_2()

    def test_clean_bookmark_children_from_toolbarFolder(self):
        print("\n[UNITTEST] test_clean_bookmark_children_from_toolbarFolder()")

        def run_testcase_1():
            print("[UNITTEST]\t\t... run_testcase_1")

            bookmarks_object = load_testcase(self, test_file1)
            bookmarks_object_cleaned = bookmark_utils.clean(bookmarks_object, "toolbarFolder", False)

            self.assertEqual(len(bookmarks_object_cleaned.get("children")), 2)

        def run_testcase_2():
            print("[UNITTEST]\t\t... run_testcase_2")

            bookmarks_object = load_testcase(self, test_file2)
            bookmarks_object_cleaned = bookmark_utils.clean(bookmarks_object, "toolbarFolder", False)

            self.assertEqual(len(bookmarks_object_cleaned.get("children")), 3)

        run_testcase_1()
        run_testcase_2()

    def test_clean_bookmark_children_from_toolbarFolder_and_merge_folder(self):
        print("\n[UNITTEST] test_clean_bookmark_children_from_toolbarFolder_and_merge_folder()")

        def run_testcase_1():
            print("[UNITTEST]\t\t... run_testcase_1")

            bookmarks_object = load_testcase(self, test_file1)
            bookmarks_object_cleaned = bookmark_utils.clean(bookmarks_object, "toolbarFolder")

            self.assertEqual(len(bookmarks_object_cleaned.get("children")), 2)

        def run_testcase_2():
            print("[UNITTEST]\t\t... run_testcase_2")

            bookmarks_object = load_testcase(self, test_file2)
            bookmarks_object_cleaned = bookmark_utils.clean(bookmarks_object, "toolbarFolder")

            self.assertEqual(len(bookmarks_object_cleaned.get("children")), 3)

        run_testcase_1()
        run_testcase_2()

    def test_clean_bookmark_children_from_unfiledFolder(self):
        print("\n[UNITTEST] test_clean_bookmark_children_from_unfiledFolder()")

        def run_testcase_1():
            print("[UNITTEST]\t\t... run_testcase_1")

            bookmarks_object = load_testcase(self, test_file1)
            bookmarks_object_cleaned = bookmark_utils.clean(bookmarks_object, "unfiledBookmarksFolder", False)

            self.assertEqual(len(bookmarks_object_cleaned.get("children")), 3)

        def run_testcase_2():
            print("[UNITTEST]\t\t... run_testcase_2")

            bookmarks_object = load_testcase(self, test_file2)
            bookmarks_object_cleaned = bookmark_utils.clean(bookmarks_object, "unfiledBookmarksFolder", False)

            self.assertEqual(len(bookmarks_object_cleaned.get("children")), 3)

        run_testcase_1()
        run_testcase_2()

    def test_clean_bookmark_children_from_unfiledFolder_and_merge_folder(self):
        print("\n[UNITTEST] test_clean_bookmark_children_from_unfiledFolder_and_merge_folder()")

        def run_testcase_1():
            print("[UNITTEST]\t\t... run_testcase_1")

            bookmarks_object = load_testcase(self, test_file1)
            bookmarks_object_cleaned = bookmark_utils.clean(bookmarks_object, "unfiledBookmarksFolder")

            self.assertEqual(len(bookmarks_object_cleaned.get("children")), 2)

        def run_testcase_2():
            print("[UNITTEST]\t\t... run_testcase_2")

            bookmarks_object = load_testcase(self, test_file2)
            bookmarks_object_cleaned = bookmark_utils.clean(bookmarks_object, "unfiledBookmarksFolder")

            self.assertEqual(len(bookmarks_object_cleaned.get("children")), 3)

        run_testcase_1()
        run_testcase_2()

    def test_clean_bookmark_children_from_rootFolder(self):
        print("\n[UNITTEST] test_clean_bookmark_children_from_rootFolder()")

        def run_testcase_1():
            print("[UNITTEST]\t\t... run_testcase_1")

            bookmarks_object = load_testcase(self, test_file1)
            bookmarks_object_cleaned = bookmark_utils.clean(bookmarks_object, "placesRoot", False)

            children = bookmarks_object_cleaned.get("children")
            self.assertEqual(len(children), 3)

            [_, menu_children] = bookmark_utils.get_bookmark_children(bookmarks_object_cleaned, "bookmarksMenuFolder")
            self.assertEqual(len(menu_children), 3)
            self.assertEqual(len(menu_children[2].get("children")), 2)

            [_, toolbar_children] = bookmark_utils.get_bookmark_children(bookmarks_object_cleaned, "toolbarFolder")
            self.assertEqual(len(toolbar_children), 1)

            [_, unfiled_children] = bookmark_utils.get_bookmark_children(bookmarks_object_cleaned, "unfiledBookmarksFolder")
            self.assertEqual(len(unfiled_children), 3)
            self.assertEqual(len(unfiled_children[2].get("children")), 1)

        def run_testcase_2():
            print("[UNITTEST]\t\t... run_testcase_2")

            bookmarks_object = load_testcase(self, test_file2)
            bookmarks_object_cleaned = bookmark_utils.clean(bookmarks_object, "placesRoot", False)

            children = bookmarks_object_cleaned.get("children")
            self.assertEqual(len(children), 3)

            [_, menu_children] = bookmark_utils.get_bookmark_children(bookmarks_object_cleaned, "bookmarksMenuFolder")
            self.assertEqual(len(menu_children), 3)
            self.assertEqual(len(menu_children[2].get("children")), 2)

            [_, toolbar_children] = bookmark_utils.get_bookmark_children(bookmarks_object_cleaned, "toolbarFolder")
            self.assertEqual(len(toolbar_children), 3)
            self.assertEqual(len(toolbar_children[2].get("children")), 1)

            [_, unfiled_children] = bookmark_utils.get_bookmark_children(bookmarks_object_cleaned, "unfiledBookmarksFolder")
            self.assertEqual(len(unfiled_children), 2)
            self.assertEqual(len(unfiled_children[1].get("children")), 1)

        run_testcase_1()
        run_testcase_2()

    def test_clean_bookmark_children_from_rootFolder_and_merge_folder(self):
        print("\n[UNITTEST] test_clean_bookmark_children_from_rootFolder_and_merge_folder()")

        def run_testcase_1():
            print("[UNITTEST]\t\t... run_testcase_1")

            bookmarks_object = load_testcase(self, test_file1)
            bookmarks_object_cleaned = bookmark_utils.clean(bookmarks_object, "placesRoot")

            children = bookmarks_object_cleaned.get("children")

            self.assertEqual(len(children), 3)

            [_, menu_children] = bookmark_utils.get_bookmark_children(bookmarks_object_cleaned, "bookmarksMenuFolder")
            self.assertEqual(len(menu_children), 3)
            self.assertEqual(len(menu_children[2].get("children")), 2)

            [_, toolbar_children] = bookmark_utils.get_bookmark_children(bookmarks_object_cleaned, "toolbarFolder")
            self.assertEqual(len(toolbar_children), 1)

            [_, unfiled_children] = bookmark_utils.get_bookmark_children(bookmarks_object_cleaned, "unfiledBookmarksFolder")
            self.assertEqual(len(unfiled_children), 2)
            self.assertEqual(len(unfiled_children[1].get("children")), 1)

        def run_testcase_2():
            print("[UNITTEST]\t\t... run_testcase_2")

            bookmarks_object = load_testcase(self, test_file2)
            bookmarks_object_cleaned = bookmark_utils.clean(bookmarks_object, "placesRoot")

            children = bookmarks_object_cleaned.get("children")
            self.assertEqual(len(children), 3)

            [_, menu_children] = bookmark_utils.get_bookmark_children(bookmarks_object_cleaned, "bookmarksMenuFolder")
            self.assertEqual(len(menu_children), 3)
            self.assertEqual(len(menu_children[2].get("children")), 2)

            [_, toolbar_children] = bookmark_utils.get_bookmark_children(bookmarks_object_cleaned, "toolbarFolder")
            self.assertEqual(len(toolbar_children), 3)
            self.assertEqual(len(toolbar_children[2].get("children")), 1)

            [_, unfiled_children] = bookmark_utils.get_bookmark_children(bookmarks_object_cleaned, "unfiledBookmarksFolder")
            self.assertEqual(len(unfiled_children), 2)
            self.assertEqual(len(unfiled_children[1].get("children")), 1)

        run_testcase_1()
        run_testcase_2()

class BookmarksMergeMethods(unittest.TestCase):

    def test_merge_bookmarks_from_menuFolder(self):
        print("\n[UNITTEST] test_merge_bookmarks_from_menuFolder()")

        bookmarks_object1 = load_testcase(self, test_file1)
        self.assertIsNotNone(bookmarks_object1)
        self.assertIsInstance(type(bookmarks_object1), type(dict))

        bookmarks_object2 = load_testcase(self, test_file2)
        self.assertIsNotNone(bookmarks_object2)
        self.assertIsInstance(type(bookmarks_object2), type(dict))

        bookmarks_merged = bookmark_utils.merge(bookmarks_object1, bookmarks_object2, "bookmarksMenuFolder", False, "")

        children = bookmarks_merged.get("children")
        self.assertEqual(len(children), 6)
        self.assertEqual(len(children[2].get("children")), 4)
        self.assertEqual(len(children[5].get("children")), 3)

    def test_merge_bookmarks_from_menuFolder_without_duplicates(self):
        print("\n[UNITTEST] test_merge_bookmarks_from_toolbarFolder_without_duplicates()")

        bookmarks_object1 = load_testcase(self, test_file1)
        self.assertIsNotNone(bookmarks_object1)
        self.assertIsInstance(type(bookmarks_object1), type(dict))

        bookmarks_object2 = load_testcase(self, test_file2)
        self.assertIsNotNone(bookmarks_object2)
        self.assertIsInstance(type(bookmarks_object2), type(dict))

        # Removes duplicated bookmarks
        # Merges duplicated folder
        bookmarks_merged = bookmark_utils.merge(bookmarks_object1, bookmarks_object2, "bookmarksMenuFolder", True, "")

        children = bookmarks_merged.get("children")
        self.assertEqual(len(children), 4)
        self.assertEqual(len(children[2].get("children")), 4)

    def test_merge_bookmarks_from_toolbarFolder(self):
        print("\n[UNITTEST] test_merge_bookmarks_from_toolbarFolder()")

        bookmarks_object1 = load_testcase(self, test_file1)
        self.assertIsNotNone(bookmarks_object1)
        self.assertIsInstance(type(bookmarks_object1), type(dict))

        bookmarks_object2 = load_testcase(self, test_file2)
        self.assertIsNotNone(bookmarks_object2)
        self.assertIsInstance(type(bookmarks_object2), type(dict))

        bookmarks_merged = bookmark_utils.merge(bookmarks_object1, bookmarks_object2, "toolbarFolder", False, "")

        children = bookmarks_merged.get("children")
        self.assertEqual(len(children), 5)
        self.assertEqual(len(children[4].get("children")), 1)

    def test_merge_bookmarks_from_toolbarFolder_without_duplicates(self):
        print("\n[UNITTEST] test_merge_bookmarks_from_toolbarFolder_without_duplicates()")

        bookmarks_object1 = load_testcase(self, test_file1)
        self.assertIsNotNone(bookmarks_object1)
        self.assertIsInstance(type(bookmarks_object1), type(dict))

        bookmarks_object2 = load_testcase(self, test_file2)
        self.assertIsNotNone(bookmarks_object2)
        self.assertIsInstance(type(bookmarks_object2), type(dict))

        bookmarks_merged = bookmark_utils.merge(bookmarks_object1, bookmarks_object2, "toolbarFolder", True, "")

        children = bookmarks_merged.get("children")
        self.assertEqual(len(children), 4)
        self.assertEqual(len(children[3].get("children")), 1)

    def test_merge_bookmarks_from_unfiledFolder(self):
        print("\n[UNITTEST] test_merge_bookmarks_from_unfiledFolder()")

        bookmarks_object1 = load_testcase(self,  test_file1)
        self.assertIsNotNone(bookmarks_object1)
        self.assertIsInstance(type(bookmarks_object1), type(dict))

        bookmarks_object2 = load_testcase(self, test_file2)
        self.assertIsNotNone(bookmarks_object2)
        self.assertIsInstance(type(bookmarks_object2), type(dict))

        bookmarks_merged = bookmark_utils.merge(bookmarks_object1, bookmarks_object2, "unfiledBookmarksFolder", False, "")

        children = bookmarks_merged.get("children")
        self.assertEqual(len(children), 6)
        self.assertEqual(len(children[2].get("children")), 1)
        self.assertEqual(len(children[5].get("children")), 1)

    def test_merge_bookmarks_from_unfiledFolder_without_duplicates(self):
        print("\n[UNITTEST] test_merge_bookmarks_from_unfiledFolder_without_duplicates()")

        bookmarks_object1 = load_testcase(self, test_file1)
        self.assertIsNotNone(bookmarks_object1)
        self.assertIsInstance(type(bookmarks_object1), type(dict))

        bookmarks_object2 = load_testcase(self, test_file2)
        self.assertIsNotNone(bookmarks_object2)
        self.assertIsInstance(type(bookmarks_object2), type(dict))

        bookmarks_merged = bookmark_utils.merge(bookmarks_object1, bookmarks_object2, "unfiledBookmarksFolder", True, "")

        children = bookmarks_merged.get("children")
        self.assertEqual(len(children), 3)
        self.assertEqual(len(children[1].get("children")), 2)

    def test_merge_bookmarks_from_rootFolder(self):
        print("\n[UNITTEST] test_merge_bookmarks_from_rootFolder")


        bookmarks_object1 = load_testcase(self, test_file1)
        self.assertIsNotNone(bookmarks_object1)
        self.assertIsInstance(type(bookmarks_object1), type(dict))

        bookmarks_object2 = load_testcase(self, test_file2)
        self.assertIsNotNone(bookmarks_object2)
        self.assertIsInstance(type(bookmarks_object2), type(dict))

        bookmarks_merged = bookmark_utils.merge(bookmarks_object1, bookmarks_object2, "placesRoot", False, "")

        children = bookmarks_merged.get("children")
        self.assertEqual(len(children), 6)

    def test_merge_bookmarks_from_rootFolder_without_duplicates(self):
        print("\n[UNITTEST] test_merge_bookmarks_from_rootFolder_without_duplicates()")

        bookmarks_object1 = load_testcase(self, test_file1)
        self.assertIsNotNone(bookmarks_object1)
        self.assertIsInstance(type(bookmarks_object1), type(dict))

        bookmarks_object2 = load_testcase(self, test_file2)
        self.assertIsNotNone(bookmarks_object2)
        self.assertIsInstance(type(bookmarks_object2), type(dict))

        bookmarks_merged = bookmark_utils.merge(bookmarks_object1, bookmarks_object2)

        children = bookmarks_merged.get("children")
        self.assertEqual(len(children), 3)
        self.assertEqual(len(children[0].get("children")), 4)
        self.assertEqual(len(children[0].get("children")[2].get("children")), 3)
        self.assertEqual(len(children[1].get("children")), 3)
        self.assertEqual(len(children[1].get("children")[2].get("children")), 1)
        self.assertEqual(len(children[2].get("children")), 2)
        self.assertEqual(len(children[2].get("children")[1].get("children")), 2)


if __name__ == '__main__':
    unittest.main() 
