import json
import bookmark_utils

def load_bookmarks_file(filename):
    with open(filename) as json_data:
        return { "name" : filename, "json" : json.load(json_data) }

def load_bookmarks_files(filenames):
    for filename in filenames:
        yield load_bookmarks_file(filename)

def write_to_file(filename, content):
    with open(filename, "w") as out:
        out.write(content)
    out.close()

def write_tree_to_json(filename, content):
    write_to_file(filename, json.dumps(content, indent=4))

def write_tree_to_txt(filenames, bookmarks_object_list, bookmark_location="placesRoot", padding = 1):

    """
    Recursively writes
    folder name, bookmark title and bookmark uri
    of list with all nested (dicts) from json file human readable to the given output file

    :param filenames:               List of one or several output files to write into
    :param bookmarks_object_list:   List of bookmarks_object lists, i.e.
                                    nested dicts, e.g. [ { 'title':'rootFolder', children': [{},{},..] }, { }]
                                    (json text)
    :param bookmark_location        bookmark_location    Bookmark location, i.e. string of folder name in json text,
                                    to extract bookmark children from.
                                    E.g. "placesRoot", "toolbarFolder", "bookmarksMenuFolder", "unfiledBookmarksFolder"
    :param padding:                 Number of indents (\t) for the written line
    """


    def write_root(out_file, json_object, json_location, json_padding=1):
        if json_object.get("root") == json_location:
            out_file.write((padding * "\t") + json_object.get("title") + "\n")

            [json_root, bookmarks] = bookmark_utils.get_bookmark_children(json_object, json_location)

            for bookmark in bookmarks:
                if bookmark.get("type") == "text/x-moz-place-container":
                    root_location = bookmark.get("root")
                    write_root(out_file, bookmark, root_location, json_padding + 1)

                elif bookmark.get("type") == "text/x-moz-place":
                    out_file.write(((json_padding + 1) * "\t") + bookmark.get("title") + " - " + bookmark.get("uri") + "\n")
                else:
                    out_file.write(((padding + 1) * "\t") + "----\n")

            bookmark_utils.set_bookmark_children(json_root, bookmarks)

    if len(filenames) == 1:

        with open(filenames[0], "w") as out:

            for bookmarks_object in bookmarks_object_list:
                out.write(bookmarks_object.get("name") + "\n")
                write_root(out, bookmarks_object.get("json"), bookmark_location, padding)
                out.write("\n\n")
        out.close()

    else:

        for i,bookmarks_object in enumerate(bookmarks_object_list):

            filename = filenames[i]
            with open(filename, "w") as out:
                out.write(bookmarks_object.get("name") + "\n")
                write_root(out, bookmarks_object.get("json"), bookmark_location, padding)
                out.write("\n\n")
            out.close()
