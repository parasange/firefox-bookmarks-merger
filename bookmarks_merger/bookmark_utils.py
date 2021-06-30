glb_seen_bookmarks = {}
glb_seen_folder = {}
glb_recLevels = []
glb_nestLevels = []

glb_remove_list_bookmarks = []
glb_move_list_folder = {}



# Helper functions
##############################

def __get_duplicate_list(bookmarks, remove_list_bookmarks=[], move_list_folder={}):

    """
    Extracts from a list of nested dicts the index lists for duplicated bookmarks of type "text/x-moz-place" (to remove)
    and folders of type "text/x-moz-place-container" (to move).



    :param bookmarks:               List of nested dicts, e.g. [ { 'title':'rootFolder', children': [{},{},..] }, { }]
                                    (json text)
    :param remove_list_bookmarks    List of index-lists of bookmarks in nested hierarchy to remove,
                                    e.g. [[0,2], [1,2,3], ...], where
                                    [0,2] is second bookmark in very first folder ()
                                    [1,2,3] is third bookmark in second child folder of very first bookmark folder
    :param move_list_folder         Dict of tuple-index-lists of folders in nested hierarchy to merge into a key
                                    folder, e.g. {(2,): [[1,1],[3]], (0,1): [[2,2]], ...}, where
                                    (2,) is second folder at root layer, where other folders should be merged into,
                                    [1,1],[3] are first child folder in first folder, and third folder
                                    at root layer, whose children should be moved all into (2,) folder
    :return:                        List of nested dicts, e.g. [ { 'title':'rootFolder', children': [{},{},..] }, { }]
                                    (json text), but without any duplicates
    """

    # Temp storage the count recursion depth for current bookmark
    global glb_recLevels

    # Stores the recursion depth indices in tree of current bookmark as tuple (x,y,..)
    # where x,y,.. are composed from glb_recLevels
    global glb_nestLevels

    # Stores all seen bookmarks/folders for comparison as dict in format
    # { (x,y,z): bf1, (x,y): bf2, ... }
    # where (x,y,z) are tuples with recursion depths indices in tree for bookmark/folder bf1
    # and bf1, bf2, ... the bookmarks itself
    global glb_seen_bookmarks
    global glb_seen_folder

    for i, bookmark in enumerate(bookmarks):
        is_dup_bookmark = False
        is_dup_folder = False


        # Get children bookmarks recursively
        if bookmark.get("type") == "text/x-moz-place-container":
            glb_recLevels.append(i)
            # print("\n recLevels: ", glb_recLevels)
            __get_duplicate_list(bookmark.get("children"), remove_list_bookmarks, move_list_folder)

            # Append very first folder in any case
            if len(glb_seen_folder) == 0:
                glb_seen_folder[tuple(glb_recLevels)] = bookmark
                # print("\t\t\t -> add to list (first): ", bookmark)
                glb_recLevels.pop()
                continue

            else:
                # Compare current folder with each in glb_seen_folder
                # Add to remove_list if it's a duplicate
                for seen_folder_indices in glb_seen_folder:
                    seen_folder_indices = tuple(seen_folder_indices)
                    seenFolder = glb_seen_folder.get(seen_folder_indices)


                    if seenFolder.get("title") == bookmark.get("title"):
                        is_dup_bookmark = True

                        if len(glb_recLevels) > len(seen_folder_indices)\
                            or glb_recLevels > list(seen_folder_indices):

                            move_list_folder.setdefault(seen_folder_indices, []).append(list(glb_recLevels.copy()))
                            break

            if not is_dup_folder:
                glb_seen_folder[tuple(glb_recLevels)] = bookmark

            glb_recLevels.pop()

        elif bookmark.get("type") == "text/x-moz-place-separator":
            continue

        # Handle single child bookmarks
        else:

            glb_nestLevels = glb_recLevels
            glb_nestLevels.append(i)

            # Append very first bookmark in any case
            if len(glb_seen_bookmarks) == 0:
                glb_seen_bookmarks[tuple(glb_nestLevels)] = bookmark
                glb_nestLevels.pop()
                continue

            else:


                # Compare current bookmark with each in glb_seen_bookmarks
                # Add to remove_list if lastModified date is newer or it's not a duplicate
                for seen_bookmark_indices in glb_seen_bookmarks:

                    seen_bookmark_indices = tuple(seen_bookmark_indices)
                    seenBookmark = glb_seen_bookmarks.get(seen_bookmark_indices)


                    if (seenBookmark.get("uri") == bookmark.get("uri")) and (seenBookmark.get("title") == bookmark.get("title")):
                        # print("\t\t\t Uri ", bookmark.get("uri"), " already there! Compare dates")
                        is_dup_bookmark = True


                        # Convert just for comparison
                        seenBookmark_lastModified = seenBookmark.get("lastModified")
                        bookmark_lastModified = bookmark.get("lastModified")


                        # seenBookmark_lastModified = datetime.datetime.fromtimestamp(
                        #      seenBookmark_lastModified / 1E6).strftime('%Y-%m-%d %H:%M:%S')
                        # bookmark_lastModified = datetime.datetime.fromtimestamp(
                        #     bookmark_lastModified / 1E6).strftime('%Y-%m-%d %H:%M:%S')


                        if bookmark_lastModified == seenBookmark_lastModified:
                            # print("\t\t\t\t Dates are equal")

                            # compare current tree index with index of seenbookmark in glb_seen_bookmarks
                            # e.g. given seen_bookmark_indices (0,2,2).
                            # Remove glb_nestLevels if
                            # [0, 2, 2, x]
                            # [0, 2, > 2, x]
                            # [0, > 2, x, x]
                            # [ > 0, x, x, x]
                            # where x is there or not there
                            if glb_nestLevels > list(seen_bookmark_indices):
                                remove_list_bookmarks.append(glb_nestLevels.copy())

                                break

                        elif bookmark_lastModified > seenBookmark_lastModified:

                            # Delete bookmark at special index
                            # stored as seenBookmarkIndex to replace
                            # and replace glb_seen_bookmarks entry with newer one (current bookmark) afterwards
                            # print("\t\t\t\t Date is newer")

                            # Mark for deletion at index that was former in glb_seen_bookmarks
                            # before it got overwritten
                            remove_list_bookmarks.append(list(seen_bookmark_indices))

                            # print("\t\t\t\t -> Remove seen bookmark at: ", seen_bookmark_indices)
                            glb_seen_bookmarks.pop(seen_bookmark_indices)
                            glb_seen_bookmarks[tuple(glb_nestLevels)] = bookmark

                            break

                        elif bookmark_lastModified < seenBookmark_lastModified:
                            # print("\t\t\t\t Date is irrelevant")
                            # print("\t\t\t\t -> Delete bookmark child at i: ", i)
                            # print("\t\t\t\t (Left children bookmarks list: )", bookmarks, "\n")

                            # print("\t\t\t\t -> Delete bookmark: ", bookmark)
                            remove_list_bookmarks.append(glb_nestLevels.copy())
                            # print("\t\t\t\t -> Continue with next bookmark in list")

                            break

            if not is_dup_bookmark:
                glb_seen_bookmarks[tuple(glb_nestLevels)] = bookmark

            glb_nestLevels.pop()

    return remove_list_bookmarks, move_list_folder

def __flatten_bookmarks(bookmarks):

    """
    Converts a list of nested dicts (with children) from json file
    to a flattened, sequential list of all children dicts. Adds only those children
    of type 'text/x-moz-place' and ignores those of type 'text/x-moz-separator'.

    :param bookmarks:   List of nested dicts, e.g. [ { 'title':'rootFolder', children': [{},{},..] }, { }]
                        (json text)
    :return:            List of bookmarks dicts,
                        e.g. [{'type':'text/x-moz-place', 'uri':'abc', },{'type':'text/x-moz-place', 'uri':'def',},..]
    """

    result = []
    if bookmarks is not None:
        for bookmark in bookmarks:
            if bookmark.get("type") == "text/x-moz-place-container":
                children_bookmarks = __flatten_bookmarks(bookmark.get("children"))
                for child in children_bookmarks:
                    result.append(child)
            else:
                if bookmark.get("type") == 'text/x-moz-place':
                    result.append(bookmark)

    return result

def __move_bookmarks_in_tree(bookmarks, folder_indices_to_move):

    """
    Moves children bookmarks from given items of index dict to corresponding keys and removes occurring empty folders

    :param bookmarks:                   List of nested dicts, e.g. [ { 'title':'rootFolder', children': [{},{},..] }, { }]
                                        (json text)
    :param folder_indices_to_move:      Dict of indices whose items should be moved to a tuple-key
                                        in tree format: e.g. {(2,): [[1,1],[3]], (0,1): [[2,2]], ...}, where
                                        (2,):     is second folder at root layer, key that stores holds all moved children
                                        [1,1]:    is second child folder of second folder at root layer, whose children
                                                  should be moved to (2,)
                                        [3]:      is third folder at root layer, whose children should be moved to (2,)
                                        ...
    :return:                            List of nested dicts, e.g. [ { 'title':'rootFolder', children': [{},{},..] }, { }]
                                        (json text), where all bookmark children moved appropriately by given dict
    """

    for key, item in folder_indices_to_move.copy().items():


        while len(item) > 0:
            indices = item.pop(0)


            # Copy folder children to tmp and delete their folder
            if len(indices) == 1:
                children_to_move = bookmarks[indices[0]].get("children")

                bookmarks.pop(indices[0])

            else:

                folder = bookmarks[indices[0]].get('children')

                for j in range(1, len(indices)-1):
                    folder = folder[indices[j]].get('children')

                children_to_move = folder.pop(indices[len(indices)-1])
                children_to_move = children_to_move.get("children")


            # Adapt rest indices in list, reduce them by 1
            if len(item) > 0:
                __update_index_list(item, indices)


            # Move the copied children from tmp to the correct folder
            key = list(key)

            if len(key) == 1:
                previous_children = bookmarks[key[0]].get("children")
                previous_children = previous_children + children_to_move
                bookmarks[key[0]]["children"] = previous_children

            else:
                folder = bookmarks[key[0]].get('children')
                # print("DEBUg copy folder: ", folder)

                for j in range(1, len(key)-1):
                    folder = folder[key[j]].get('children')

                previous_children = folder[key[-1]].get("children")
                previous_children = previous_children + children_to_move

                folder[key[-1]]["children"] = previous_children



        folder_indices_to_move.pop(tuple(key))

        __update_index_list(folder_indices_to_move, indices)

    return bookmarks

def __remove_bookmarks_from_tree(bookmarks, bookmark_indices_to_remove, folder_indices_to_move = {}):

    """
    Removes all bookmarks at the indices from given list while updating folder_indices_to_move appropriately

    :param bookmarks:                   List of nested dicts, e.g. [ { 'title':'rootFolder', children': [{},{},..] }, { }]
                                        (json text)
    :param bookmark_indices_to_remove:  List of indices whose keys should be removed in bookmarks,
                                        e.g. [[0], [1,2,0], [1,2,1], [4,2]], where
                                        [0]:        0 is index at root layer
                                        [1,2,0]:    1 is index at root layer, 2 index at root's children, 0 index at root's
                                                    child (2) children
                                        ...
    :param folder_indices_to_move:      Dict of indices whose items should be moved to a tuple-key
                                        in tree format: e.g. {(2,): [[1,1],[3]], (0,1): [[2,2]], ...}, where
                                        (2,):     is second folder at root layer, key that stores holds all moved children
                                        [1,1]:    is second child folder of second folder at root layer, whose children
                                                  should be moved to (2,)
                                        [3]:      is third folder at root layer, whose children should be moved to (2,)
                                        ...
    :return:                            List of nested dicts, e.g. [ { 'title':'rootFolder', children': [{},{},..] }, { }]
                                        (json text), where all bookmark children are removed appropriately by given
                                        bookmark_indices_to_remove list
    """

    while len(bookmark_indices_to_remove) > 0:


        current_rec_level_item = bookmark_indices_to_remove.pop(0)
        isSucceeded = False

        if len(current_rec_level_item) == 1:

            bookmarks.pop(current_rec_level_item[0])

        else:

            dictElem = bookmarks[current_rec_level_item[0]].get('children')

            for j in range(1, len(current_rec_level_item)-1):
                dictElem = dictElem[current_rec_level_item[j]].get('children')

            dictElem.pop(current_rec_level_item[len(current_rec_level_item)-1])


        # Reduce last index of each same glb_recLevels by 1
        # to be able to pop next correct one

        # Adapt all next indices in both removing lists when a bookmark item was removed
        __update_index_list(bookmark_indices_to_remove, current_rec_level_item)

        # Adapt both, key and item indices
        __update_index_list(folder_indices_to_move, current_rec_level_item)


    return bookmarks

def __update_index_list(index_list, item_to_compare):

    """
    Updates an index list/dict by comparing its elements to a given element

    :param index_list:          The index list or dict to update, can either be a list as bookmark indices to remove
                                or a dict as folder indices to merge
    :param item_to_compare      Index list to compare the elements of index_list to,
                                e.g. [0,2] as second bookmark or folder in very first root folder
    """

    # Duplicated bookmarks for removal are stored as index list of format [[1,2], [2,0,0], [3], ..]
    if isinstance(index_list,list):

        for next_item in index_list:

            assert isinstance(next_item, list)

            if len(item_to_compare) == 1 and next_item[0] > item_to_compare[0]:
                next_item[0] = next_item[0] - 1

            if len(item_to_compare) > 1:

                if next_item[0] == item_to_compare[0] and next_item[1:len(next_item)] > item_to_compare[1:len(item_to_compare)]:
                    next_item[len(item_to_compare)-1] = next_item[len(item_to_compare)-1] - 1

    # Duplicated folders for merging are stored as index dict of format {(1,): [[1,2], [2,0,0]], (3,4): [[0]]}
    elif isinstance(index_list, dict):

        for key, item in index_list.items():

            assert isinstance(key, tuple)
            assert isinstance(item, list)

            if len(item_to_compare) == 1:

                if list(key)[0] > item_to_compare[0]:

                    key_l = list(key)
                    key_l[0] = key_l[0] - 1
                    key = tuple(key_l)

                for i in item:
                    if i[0] > item_to_compare[0]:

                        i[0] = i[0] - 1

            if len(item_to_compare) > 1:

                if list(key)[0] == item_to_compare[0] and list(key)[1:len(key)] > item_to_compare[1:len(item_to_compare)]:

                    key_l = list(key)
                    key_l[len(item_to_compare)-1] = key_l[len(item_to_compare)-1]-1
                    key = tuple(key_l)

                for i in item:
                    if i[0:-1] == item_to_compare[0:-1] and i[-1] > item_to_compare[-1]:

                        i[len(item_to_compare)-1] = i[len(item_to_compare)-1]-1

    else:
        raise TypeError("ERROR. Cannot update a list of type ", type(index_list))


def get_bookmark_children(bookmarks_object, bookmark_location="placesRoot", flatten = False):
    """
    Extracts the children at bookmark location from bookmarks json file
    and returns it separately from root bookmarks

    :param bookmarks_object:    Reference to list of nested dicts, e.g. [ { 'title':'rootFolder', children': [{},{},..] }, { }]
                                (json text) to get children from
    :param bookmark_location    Bookmark location, i.e. string of folder name in json text,
                                to extract bookmark children from
                                E.g. "toolbarFolder", "bookmarksMenuFolder", "unfiledBookmarksFolder"
    :param flatten              If children should rather be returned as flattened list with single bookmarks
                                (only true bookmarks, i.e. dicts of type 'text/x-moz-place' are added)
    :return:                    [root, [children]] The root bookmarks_object with emptied children and its separated children as list
                                or empty list, if bookmark_location does not exist
    """

    found = [None, None]

    def get_unpacked_list(bookmarks):
        bookmark_children = bookmarks.get("children")

        if flatten:
            bookmark_children = __flatten_bookmarks(bookmark_children)

        bookmarks["children"] = []

        return [bookmarks, bookmark_children]

    def search_children(b_o, b_l, fl):

        for bookmark in b_o:

            if bookmark.get("type") == "text/x-moz-place-container":

                if bookmark.get("root") == b_l:

                    # Separate root json source from its children and return both
                    nonlocal found
                    found = get_unpacked_list(bookmark)
                    break

                bookmark_children = bookmark.get("children")
                search_children(bookmark_children, bookmark_location, flatten)

            else:
                continue

        # if found:
        return found

    if bookmarks_object.get("type") == "text/x-moz-place-container":

        if bookmarks_object.get("root") == bookmark_location:
            return get_unpacked_list(bookmarks_object)

        children = bookmarks_object.get("children")
        found = search_children(children, bookmark_location, flatten)
        return found

def set_bookmark_children(json_root_object, bookmarks):

    """ Sets bookmarks as value for 'children' key entry of a root bookmark

    :param json_root_object:    First (root) bookmark entry of a dict
    :param bookmarks:           The children list [{}, {},...] of dictionaries for root's 'children' key
    :return:                    The root bookmark entry with filled 'children' key
    """

    json_root_object["children"] = bookmarks

    return json_root_object

def strip_ids_in_tree(bookmarks_object, bookmark_location="placesRoot"):

    """
    Removes recursively removes tags 'guid', 'id' and 'index' in all single bookmarks
    in nested dicts (with children) from bookmark location. Removes tags only in those bookmarks that
    are of type 'text/x-moz-place'.

    :param bookmarks_object:    Reference to list of nested dicts, e.g. [ { 'title':'rootFolder', children': [{},{},..] }, { }]
                                (json text)
    :param bookmark_location    Bookmark location, i.e. string of folder name in json text,
                                to extract bookmark children from.
                                E.g. "placesRoot", "toolbarFolder", "bookmarksMenuFolder", "unfiledBookmarksFolder"
    """

    if bookmarks_object.get("root") == bookmark_location:
        [json_root, bookmarks] = get_bookmark_children(bookmarks_object, bookmark_location)

        for bookmark in bookmarks:
            if bookmark.get("type") == "text/x-moz-place-container":
                root_location = bookmark.get("root")
                strip_ids_in_tree(bookmark, root_location)

            elif bookmark.get("type") == "text/x-moz-place":
                bookmark.pop("id", None)
                bookmark.pop("guid", None)
                bookmark.pop("index", None)

        set_bookmark_children(json_root, bookmarks)



# CLI functions
##############################

def clean(bookmarks_object, bookmark_location = "placesRoot", merge_folders = True):

    """
    Cleans list of nested dicts (with children) from bookmark duplicates, and merges folders
    of duplicated bookmarks folders into first occurrence of that folder by default

    :param bookmarks_object:    List of nested dicts, e.g. [ { 'title':'rootFolder', children': [{},{},..] }, { }]
                                (json text) to be cleaned
    :param bookmark_location    Bookmark location, i.e. string of folder name in json text,
                                to clean from duplicated bookmarks
    :param merge_folders:       If duplicated folders should be merged into first occurrence of folder, too
    :return:                    List of nested dicts, e.g. [ { 'title':'rootFolder', children': [{},{},..] }, { }]
                                (json text), with unique bookmarks and potentially unique bookmark folders
    """


    # Re-set all to run bunch of unittests
    global glb_seen_bookmarks
    global glb_seen_folder
    global glb_recLevels
    global glb_nestLevels
    global glb_remove_list_bookmarks
    global glb_move_list_folder

    glb_seen_bookmarks = {}
    glb_seen_folder = {}
    glb_recLevels = []
    glb_nestLevels = []
    glb_remove_list_bookmarks = []
    glb_move_list_folder = {}

    [jsonRoot, bookmarks] = get_bookmark_children(bookmarks_object, bookmark_location)

    remove_list_bookmarks, move_list_folder = __get_duplicate_list(bookmarks, glb_remove_list_bookmarks, glb_move_list_folder)

    cleaned_bookmarks = __remove_bookmarks_from_tree(bookmarks, remove_list_bookmarks, move_list_folder)

    if merge_folders:
        cleaned_bookmarks = __move_bookmarks_in_tree(cleaned_bookmarks, move_list_folder)


    return set_bookmark_children(jsonRoot, cleaned_bookmarks)

def merge(main_bookmarks_object, second_bookmarks_object, bookmark_location="placesRoot", remove_duplicates=True):

    """
    Merges two lists of nested dicts (with children) by appending the second one. Removes bookmark duplicates in result
    nested dict and merges it folder duplicates by default.


    :param main_bookmarks_object:       Main list of nested dicts, e.g. [ { 'title':'rootFolder', children': [{},{},..] }, { }]
                                        (json text)
    :param second_bookmarks_object:     Second list of nested dicts, that gets appended to first one
                                        e.g. [ { 'title':'rootFolder', children': [{},{},..] }, { }]
                                        (json text)
    :param bookmark_location            Bookmark location, i.e. string of folder name in json text,
                                        to clean from duplicated bookmarks/to merge duplicated folders
                                        If it's empty then merge the second list's bookmarks into main's nested dicts
    :param remove_duplicates:           True, if bookmark duplicates should be removed/folder duplicates should be
                                        merged after appending
    :return:                            List of nested dicts, e.g. [ { 'title':'rootFolder', children': [{},{},..] }, { }]
                                        (json text) that contains bookmarks and folders of main and second list merged
    """


    [json_root_main, main_bookmarks] = get_bookmark_children(main_bookmarks_object, bookmark_location)
    [_, second_bookmarks] = get_bookmark_children(second_bookmarks_object, bookmark_location)

    for bookmark in second_bookmarks:
        main_bookmarks.append(bookmark)

    main_bookmarks_object = set_bookmark_children(json_root_main, main_bookmarks)

    if remove_duplicates:
        main_bookmarks_object = clean(main_bookmarks_object, bookmark_location)

    return main_bookmarks_object



