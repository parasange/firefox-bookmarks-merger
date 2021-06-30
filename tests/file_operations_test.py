import unittest
from firefox_bookmarks_merger import file_operations

class BookmarksMergerFileLoadMethods(unittest.TestCase):

    def test_file_load(self):
        print("\n[UNITTEST] test_file_load()")

        def run_testcase_1():
            print("[UNITTEST]\t\t... run_testcase_1")

            bookmarks_object_wrapper = file_operations.load_bookmarks_file("../tests/testcase1.json")
            self.assertEqual(bookmarks_object_wrapper.get("name"), "../tests/testcase1.json")
            bookmarks_object = bookmarks_object_wrapper.get("json")
            self.assertEqual(bookmarks_object.get("root"), "placesRoot")
            self.assertEqual(len(bookmarks_object.get("children")), 3)

        def run_testcase_2():
            print("[UNITTEST]\t\t... run_testcase_2")

            bookmarks_object_wrapper = file_operations.load_bookmarks_file("../tests/testcase2.json")
            self.assertEqual(bookmarks_object_wrapper.get("name"), "../tests/testcase2.json")
            bookmarks_object = bookmarks_object_wrapper.get("json")
            self.assertEqual(bookmarks_object.get("root"), "placesRoot")
            self.assertEqual(len(bookmarks_object.get("children")), 3)

        run_testcase_1()
        run_testcase_2()

    def test_multiple_file_load(self):
        print("\n[UNITTEST] test_multiple_file_load()")

        bookmarks_object_list = list(file_operations.load_bookmarks_files(["../tests/testcase1.json", "../tests/testcase2.json"]))
        self.assertEqual(len(bookmarks_object_list), 2) 


if __name__ == '__main__':
    unittest.main() 
