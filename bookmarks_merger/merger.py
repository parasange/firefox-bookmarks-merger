import cli_parser
import file_operations
import bookmark_utils
import json


def main():

    args = cli_parser.parse_arguments()

    if args.list:

        bookmarks_object_wrappers_list = list(file_operations.load_bookmarks_files(args.files))

        if args.output is None:
            print("WARNING. No output file given. Write to input file copy.")

            filename_outputs = [bookmarks_object_wrappers_list[0].get("name")[0:-5] + "_tree.txt"]
        else:
            if len(args.output) > 1 and len(args.output) is not len(args.files):
                print("ERROR. Write all trees into one file or use one output file for each input file.")
                return
            else:
                filename_outputs = args.output


        file_operations.write_tree_to_txt(filename_outputs, bookmarks_object_wrappers_list)

    if args.clean and not args.merge:
        bookmarks_object_wrappers_list = list(file_operations.load_bookmarks_files(args.files))

        if args.output is None:
            print("WARNING. No output file given. Write to input file copy/copies.")

            for object_wrapper in bookmarks_object_wrappers_list:
                filename_output = object_wrapper.get("name")[0:-5] + "_cleaned.json"
                json_object = object_wrapper.get("json")
                json_object_cleaned = bookmark_utils.clean(json_object)

                file_operations.write_tree_to_json(filename_output, json_object_cleaned)

        else:
            if len(args.output) != len(bookmarks_object_wrappers_list):
                print("ERROR. Needs one output file for each input file.")

            else:
                for filename_output in args.output:
                    if filename_output[-5:len(filename_output)] != ".json":
                        print("ERROR. At least one output file has no .json ending.")
                        return

                for filename_output, object_wrapper in zip(args.output, bookmarks_object_wrappers_list):
                    json_object = object_wrapper.get("json")
                    json_object_cleaned = bookmark_utils.clean(json_object)

                    file_operations.write_tree_to_json(filename_output, json_object_cleaned)

    if args.merge:
        if len(args.files) <= 1:
            print("ERROR. At least two files are necessary for merging.")
            return

        bookmarks_object_wrappers_list = list(file_operations.load_bookmarks_files(args.files))

        if args.output is None:
            filename_output = bookmarks_object_wrappers_list[0].get("name")[0:-5] + "_merged.json"

        elif len(args.output) > 1:
            print("ERROR. Only one output file needed.")
            return
        else:
            filename_output = args.output[0]

        main_bookmarks_object = bookmarks_object_wrappers_list[0].get("json")

        for other_bookmarks_object_wrapper in bookmarks_object_wrappers_list[1:]:

            other_bookmarks_object = other_bookmarks_object_wrapper.get("json")

            if args.clean:
                main_bookmarks_object = bookmark_utils.merge(main_bookmarks_object, other_bookmarks_object)

            else:
                main_bookmarks_object = bookmark_utils.merge(main_bookmarks_object, other_bookmarks_object, remove_duplicates=False)

        file_operations.write_tree_to_json(filename_output, main_bookmarks_object)

    if args.sort:
        print("DEBUG --sort. Not implemented yet.")


