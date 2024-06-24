import inspect
import types
from typing import Any


def dict_has_key_chain(source: dict[Any,Any],
                       key_chain: list[str]) -> bool:
    """
    Indicate the existence of an element in *source*, pointed to by the nested key chain *[keys[0]: ... :keys[n]*.

    The path up to he last key in the chain must point to an existing element.
    A given key may indicate the element's position within a *list*, using the format *<key>[<pos>]*.

    :param source: the reference dict
    :param key_chain: the nested key chain
    :return: whether the element exists
    """
    # initialize the return variable
    result: bool = False

    # define the parent el;ement
    parent: dict | None = None

    # does the key chain contain just 1 element ?
    if len(key_chain) == 1:
        # yes, use the provided dict
        parent = source

    # does the key chain contain more than 1 element ?
    elif len(key_chain) > 1:
        # yes, obtain the parent element of the last key in the chain
        parent = dict_get_value(source=source,
                                key_chain=key_chain[:-1])

    # is the parent element a dict ?
    if isinstance(parent, dict):
        # yes, proceed
        key = key_chain[-1]

        # is the element denoted by the last key in the chain a list ?
        if key[-1] == "]":
            # yes, recover it
            pos: int = key.find("[")
            inx: int = int(key[pos+1:-1])
            key = key[:pos]
            child = parent.get(key)
            # success, if the element in question is a list with more than 'inx' elements
            result = isinstance(child, list) and len(child) > inx

        # success, if the parent element contains the last key in the chain
        else:
            result = key in parent

    return result


def dict_get_value(source: dict[Any,Any],
                   key_chain: list[str]) -> any:
    """
    Obtain the value of the element in *source*, pointed to by the nested key chain *[keys[0]: ... :keys[n]*.

    The path up to the last key in the chain must point to an existing element.
    A given key may indicate the element's position within a *list*, using the format *<key>[<pos>]*.
    Return *None* if the sought after value is not found.
    Note that returning *None* might not be indicative of the absence of the element in *source*,
    since that element might exist therein with the value *None*. To determine whether this is the case,
    use the operation *dict_has_value*.

    :param source: the reference dict
    :param key_chain: the key chain
    :return: the value obtained
    """
    # initialize the return variable
    result: any = source

    # traverse the keys in the chain
    for key in key_chain:

        # is it possible to proceed ?
        if not isinstance(result, dict):
            # no, terminate the operation
            result = None
            break

        # does the key refer to an elemenent in a list ?
        if key[-1] == "]":
            # yes, retrieve it
            pos: int = key.find("[")
            inx: int = int(key[pos+1:-1])
            result = result.get(key[:pos])

            result = result[inx] if isinstance(result, list) and len(result) > inx else None

            # is it possible to proceed ?
            if isinstance(result, list) and len(result) > inx:
                # yes, proceed
                result = result[inx]
            else:
                # no, abort the operation
                result = None
        else:
            # proceeding is not possible, the element corresponding to 'key' in the dictionary
            result = result.get(key)

    return result


def dict_set_value(target: dict,
                   key_chain: list[str],
                   value: Any) -> None:
    """
    Assign to an element of *source* the value *value*.

    The element in question is pointed to by the key chain *[keys[0]: ... :keys[n]*.
    If the element does not exist, it is created with the specified value.
    Any non-existing intermediate elements are created with the value of an empty *dict*.
    A key might indicate the position of the element within a list, using the format *<key>[<pos>]*.
    In such a case, that element must exist.

    :param target: the reference dict
    :param key_chain: the key chain
    :param value: the value to be assigned
    """
    dict_item: any = target
    # traverse the chain, up to end including its penultimate element
    for key in key_chain[:-1]:

        # is it possible to proceed ?
        if not isinstance(dict_item, dict):
            # no, abort the operation
            break

        # does 'key' refer to a list element ?
        if key[-1] == "]":
            # yes, retrieve it
            pos: int = key.find("[")
            inx: int = int(key[pos+1:-1])
            dict_item = dict_item.get(key[:pos])
            # is it possible to proceed ?
            if isinstance(dict_item, list) and len(dict_item) > inx:
                # yes, proceed
                dict_item = dict_item[inx]
            else:
                # no, abort the operation
                dict_item = None
        else:
            # no, does 'dict_item' have 'key' as one of its elements ?
            if key not in dict_item:
                # não, assign to 'dict_item' the element 'key', with an empty dict as value
                dict_item[key] = {}
            dict_item = dict_item.get(key)

    # does a key exist and is 'dict_item'a dict ?
    if len(key_chain) > 0 and isinstance(dict_item, dict):
        # yes, proceed
        key: str = key_chain[-1]
        # does 'key' refer to a list element ?
        if key[-1] == "]":
            # yes, retrieve it
            pos: int = key.find("[")
            inx: int = int(key[pos+1:-1])
            dict_item = dict_item.get(key[:pos])
            # is the assignment possible ?
            if isinstance(dict_item, list) and len(dict_item) > inx:
                # yes, do it
                dict_item[inx] = value
        else:
            # no, assign 'value' to the element 'key' in the dictionary
            dict_item[key] = value


def dict_pop_value(target: dict[Any,Any],
                   key_chain: list[str]) -> any:
    """
    Obtain the value of the element in *source*, pointed to by the nested key chain *[keys[0]: ... :keys[n]*.

    The path up to the last key in the chain must point to an existing element.
    A given key may indicate the element's position within a *list*, using the format *<key>[<pos>]*.
    Return *None* if the sought after value is not found.
    Note that returning *None* might not be indicative of the absence of the element in *source*,
    since that element might exist therein with the value *None*. To determine whether this is the case,
    use the operation *dict_has_value*.

    :param target: the reference dict
    :param key_chain: the key chain
    :return: the value removed
    """
    # initialize the return variable
    result: any = None

    # obtain the element pointed to by the las key in the chain
    parent: dict | None = None

    # does the key chain contain just 1 element ?
    if len(key_chain) == 1:
        # yes, use the provided dict
        parent = target

    # does the key chain contain more than 1 element ?
    elif len(key_chain) > 1:
        # yes, retrieve the parent element of the last key in the chain
        parent = dict_get_value(source=target,
                                key_chain=key_chain[:-1])

    # is the parent element a dict ?
    if isinstance(parent, dict):
        # yes, proceed
        key: str = key_chain[-1]

        # does the last key un the chain refer to a list element ?
        if key[-1] == "]":
            # sim, retrieve the list
            pos: int = key.find("[")
            inx: int = int(key[pos+1:-1])
            key = key[:pos]
            child: any = parent.get(key)

            # is the element pointed to by the last key in the chain a list with more than 'inx' elements ?
            if isinstance(child, list) and len(child) > inx:
                # yes, remove that element and return its value
                result = child.pop(inx)

        # does the parent item contain the last key in the chain ?
        elif key in parent:
            # yes, remove that element and return its value
            result = parent.pop(key)

    return result


def dict_replace_value(target: dict[Any,Any],
                       old_value: any,
                       new_value: any) -> None:
    """
    Replace, in *target*, all occurrences of *old_value* with *new_value*.

    :param target: the reference dict
    :param old_value: the value to be replaced
    :param new_value: the new value
    """
    def list_replace_value(items: list[any],
                           old_val: any,
                           new_val: any) -> None:
        # traverse the list
        for item in items:

            # is 'item' a dict ?
            if isinstance(item, dict):
                # yes, process it recursively
                dict_replace_value(target=item,
                                   old_value=old_val,
                                   new_value=new_val)

            # is 'item' a list ?
            elif isinstance(item, list):
                # yes, process it recursively
                list_replace_value(items=item,
                                   old_val=old_val,
                                   new_val=new_val)

    # traverse the dict
    for curr_key, curr_value in target.items():

        # is 'curr_value' the value to be replaced ?
        if curr_value == old_value:
            # yes, replace it
            target[curr_key] = new_value

        # is 'curr_value' a dict ?
        elif isinstance(curr_value, dict):
            # yes, process it recursively
            dict_replace_value(target=curr_value,
                               old_value=old_value,
                               new_value=new_value)

        # is 'curr_value' a list ?
        elif isinstance(curr_value, list):
            # yes, process it recursively
            list_replace_value(items=curr_value,
                               old_val=old_value,
                               new_val=new_value)


def dict_get_key(source: dict[Any,Any],
                 value: any) -> any:
    """
    Return the key in *source*, mapping the first occurrence of *value* found.

    Return *None*, if no key is found.
    No recursion is attempted; only the first-level attributes in *source* are inspected.

    :param source: dict to search
    :param value: the reference value
    :return: first key mapping the reference value
    """
    result: any = None
    for key, val in source.items():
        if val == value:
            result = key
            break

    return result


def dict_get_keys(source: [Any,Any],
                  value: any) -> list[str]:
    """
    Return all keys in *source*, mapping the value *value*.

    Return *[]* if no key is found.

    :param source: dict to search
    :param value: the reference value
    :return: list containing all keys mapping the reference value
    """
    return [key for key, val in source.items() if val == value]


def dict_merge(target: dict[Any,Any],
               source: dict) -> None:
    """
    Traverse the elements in *source* to update *target*, according to the criteria presented herein.

    The criteria to be followed are:
      - add the element to *target*, if it does not exist
      - if the element exists in *target*:

        - recursively process both elements, if both are type *dict*
        - add the missing items, if both are type *list*
        - replace the element in *target* if it is a different type, ou if both elements are not of the same type

    :param target: the dictionary to be updated
    :param source: the dictionary with the new elements
    """
    # traverse the dictionary with the new elements
    for skey, svalue in source.items():

        # is the item in target ?
        if skey in target:
            # yes, proceed
            tvalue: any = target.get(skey)

            # are both elements dictionaries  ?
            if isinstance(svalue, dict) and isinstance(tvalue, dict):
                # yes, recursively process them
                dict_merge(target=tvalue,
                           source=svalue)

            # are both elements lists ?
            elif isinstance(svalue, list) and isinstance(tvalue, list):
                # yes, add the missing elements
                for item in svalue:
                    if item not in tvalue:
                        tvalue.append(item)
            else:
                # both elements are not lists or dictionarie, replace the value in target
                target[skey] = svalue
        else:
            # the item is not in target, add it
            target[skey] = svalue


def dict_coalesce(target: dict[Any,Any],
                  key_chain: list[str]) -> None:
    """
    Coalesce the element of type *list* in *target* at the level *n* with the list at the level immediately above.

    This element is pointed to by the key chain *[keys[0]: ... :keys[n]*, and is processed as a sequence
    of multiple elements. The two last keys in *key_chain* must be associated with values of type *list*.

    :param target: the dictionary to be coalesced
    :param key_chain: the chain of nested keys
    """
    # traverse the kay chain up to its penultimate element
    curr_dict: dict | None = target
    # 'key_chain[:-2]' returns an empy list if it has less the 3 elements
    for inx, key in enumerate(key_chain[:-2]):

        # is 'curr_dict' a dictionary ?
        if not isinstance(curr_dict, dict):
            # no, abort the operation
            break

        # is 'key' associated to a list ?
        in_list: list[any] = curr_dict.get(key)
        if isinstance(in_list, list):
            # yes, recursively invoke the coalescing of the dictionaries in the list
            for in_dict in in_list:
                # is 'in_dict' a dictionary ?
                if isinstance(in_dict, dict):
                    # yes, recursively coaslesce it
                    dict_coalesce(target=in_dict,
                                  key_chain=key_chain[inx + 1:])
            # finalize the operation
            curr_dict = None
            break

        # proceed, with the value associated to 'key'
        curr_dict = curr_dict.get(key)

    # is 'curr_dict' a dictionary containing the penultimate key ?
    if isinstance(curr_dict, dict) and \
       isinstance(curr_dict.get(key_chain[-2]), list):
        # yes, proceed with the operation
        penultimate_elem: list[dict] = curr_dict.pop(key_chain[-2])
        penultimate_list: list[dict] = []

        # traverse the penultimate element
        for last_elem in penultimate_elem:

            # is 'last_elem' a dictionary ?
            if isinstance(last_elem, dict):
                # yes, proceed
                outer_dict: dict = {}
                last_list: list[dict] = []

                # traverse the last element
                for k1, v1 in last_elem.items():
                    # if 'k1' the last key, and is it a list ?
                    if k1 == key_chain[-1] and isinstance(v1, list):
                        # yes, obtain its items for further coalescing
                        for in_dict in v1:
                            # is 'in_dict' a dictionary ?
                            if isinstance(in_dict, dict):
                                # yes, coalesce and save it
                                inner_dict: dict = {}
                                for k2, v2 in in_dict.items():
                                    inner_dict[k2] = v2
                                last_list.append(inner_dict)
                            else:
                                # no, save it as is
                                last_list.append(in_dict)
                    else:
                        # no, coalesce it
                        outer_dict[k1] = v1

                # are there items to be coalesced ?
                if len(last_list) > 0:
                    # yes, do it
                    for in_dict in last_list:
                        # is 'in_dict' a dictionary ?
                        if isinstance(in_dict, dict):
                            # yes, add the saved data to it
                            in_dict.update(outer_dict)
                        # save the item
                        penultimate_list.append(in_dict)
                else:
                    # no, save the already coalesced items
                    penultimate_list.append(outer_dict)
            else:
                # no, save it
                penultimate_list.append(last_elem)

        # replace the original list with the coalesced new list
        curr_dict[key_chain[-2]] = penultimate_list


def dict_reduce(target: dict[Any,Any],
                key_chain: list[str]) -> None:
    """
    Relocate the elements from *target* at level *n*, to the level immediately above.

    These elements are pointed to by the nested key chain *[keys[0]: ... :keys[n]*.
    The element at level *n* is removed at the end.

    :param target: the 'dict' to be reduced
    :param key_chain: the key chain
    """
    # does the key chain contain at least 1 key ?
    if len(key_chain) > 0:
        # yes, proceed

        curr_dict: dict | None = target
        # traverse the chain up to its penultimate key
        for inx, key in enumerate(key_chain[:-1]):

            # is it possible to proceed?
            if not isinstance(curr_dict, dict):
                # no, abort the operation
                break

            # is 'key' associated with a list ?
            in_list: list[any] = curr_dict.get(key)
            if isinstance(in_list, list):
                # yes, recursively invoke reduction of the dictionaries in 'in_list'
                for in_dict in in_list:
                    # Is the list item a dictionary ?
                    if isinstance(in_dict, dict):
                        # sim, recursively reduce it
                        dict_reduce(target=in_dict,
                                    key_chain=key_chain[inx + 1:])
                # terminate the operation
                curr_dict = None
                break

            # proceed with the value associated with 'key'
            curr_dict = curr_dict.get(key)

        last_key: str = key_chain[-1]
        # does 'curr_dict' contain a dictionary associated with 'last_key' ?
        if isinstance(curr_dict, dict) and \
           isinstance(curr_dict.get(last_key), dict):
            # yes, proceed with the reduction
            last: dict = curr_dict.pop(last_key)
            for key, value in last.items():
                curr_dict[key] = value


def dict_from_list(source: list[dict[Any,Any]],
                   key_chain: list[str],
                   value: any) -> dict:
    """
    Locate in *source*, and return, the element of type *dict* with value *value* in the key chain *key_chain*.

    :param source: the list to be inspected
    :param key_chain: the key chain used in the search process
    :param value: the value of the element pointed to by the key chain
    :return: the 'dict' wanted, or 'None' if not found
    """
    # initialize the return variable
    result: dict | None = None

    for item in source:
        if isinstance(item, dict) and \
           value == dict_get_value(source=item,
                                   key_chain=key_chain):
            result = item
            break

    return result


def dict_from_object(source: object) -> dict:
    """
    Create a *dict* and populate it with the attributes in *source* containing non-None values.

    The input *source* might be any *object*, specially those decorated with *@dataclass*.

    :param source: the reference object
    :return: 'dict' structurally similar to the reference object
    """
    # initialize the return variable
    result: dict = {}

    # obtain the object's source module
    source_module: types.ModuleType = inspect.getmodule(object=source)
    # obtain the source module's dictionary
    source_dict: dict = source.__dict__
    # traverse it
    for key, value in source_dict.items():
        # is 'value' None or an empty list ?
        if not (value is None or (isinstance(value, list) and len(value) == 0)):
            # no, proceed
            name: str = key

            # is 'value' a list ?
            if isinstance(value, list):
                # es, traverse it
                result[name] = []
                for list_item in value:
                    # is 'list_item' an object of the same module ?
                    if source_module == inspect.getmodule(object=list_item):
                        # yes, proceed recursively
                        result[name].append(dict_from_object(source=list_item))
                    else:
                        # no, proceed linearly
                        result[name].append(list_item)

            # is 'value' an object of the same module ?
            elif source_module == inspect.getmodule(object=value):
                # yes, proceed recursively
                result[name] = dict_from_object(source=value)
            else:
                # no, proceed linearly
                result[name] = value

    return result


def dict_transform(source: dict[Any,Any],
                   from_to_keys: list[tuple[str,str]],
                   prefix_from: str = None,
                   prefix_to: str = None) -> dict:
    """
    Build a new *dict*, according to the rules presented herein.

    This dictionary is constructed by creating, for each element of the list of tuples in
    *from_to_keys*, the element indicated by the second term of the tuple, assigning to it
    the value of the *source* element indicated by the first term of the tuple. Both terms
    of the tuples are represented by a chain of nested keys.

    The prefixes for the source and destination keys, if defined, have fferent treatments.
    They are added when searching for values in *Source*, and removed when assigning values
    to the return *dict*.

    :param source: the source 'dict' of the values
    :param from_to_keys: the list of tuples containing the source and destination key sequences
    :param prefix_from: prefix to be added to source keys
    :param prefix_to: prefix to be removed from target keys
    :return: the new 'dict'
    """
    # import the needed functions
    from .list_pomes import list_find_coupled, list_transform, list_unflatten

    # initialize the return variable
    result: dict = {}

    # traverse the source dictionary
    for key, value in source.items():

        # define the source key chain
        if prefix_from:
            from_keys: str = f"{prefix_from}.{key}"
        else:
            from_keys: str = key

        # get the target key chain
        to_keys: str = list_find_coupled(coupled_elements=from_to_keys,
                                         primary_element=from_keys)

        # has the destination been defined ?
        if to_keys:
            # yes, get the target value
            if isinstance(value, dict):
                # 'value' is a dictionary, transform it
                to_value: dict = dict_transform(source=value,
                                                from_to_keys=from_to_keys,
                                                prefix_from=from_keys,
                                                prefix_to=to_keys)
            elif isinstance(value, list):
                # 'value' is a list, transform it
                to_value: list = list_transform(source=value,
                                                from_to_keys=from_to_keys,
                                                prefix_from=from_keys,
                                                prefix_to=to_keys)
            else:
                # 'value' is neither a dictionary nor a list
                to_value: any = value

            # has the target prefix been defined and does it occur in the target string ?
            if prefix_to and to_keys.startswith(prefix_to):
                # yes, remove the prefix
                to_keys = to_keys[len(prefix_to)+1:]
            to_keys_deep: list[str] = list_unflatten(source=to_keys)

            # assign the transformed value to the result
            dict_set_value(target=result,
                           key_chain=to_keys_deep,
                           value=to_value)

    return result


def dict_clone(source: dict,
               from_to_keys: list[str | tuple[str,str]]) -> dict:
    """
    Build a new *dict*, according to the rules presented herein.

    This dictionary is constructed by creating a new element for each element in the list
    *from_to_keys*. When the element of this list is a tuple, the name indicated by its
    second term is used, and the value of the *source* element indicated by the tuple's
    first term is assigned. This first term can be represented by a chain of  nested keys.
    The name of the element to be created can be omitted, in which case the name of the term
    indicative of the value to be assigned is used. If the corresponding value is not found
    in *source*, *None* is assigned.

    :param source: the source dict
    :param from_to_keys: list of elements indicative of the source and target keys
    :return: the new dict
    """
    # import the needed function
    from .list_pomes import list_unflatten

    # inicialize the return variable
    result: dict = {}

    # traverse the list of elements and add to the target dict
    for elem in from_to_keys:
        from_key: str = elem[0] if isinstance(elem, tuple) else elem
        to_key: str = (elem[1] if isinstance(elem, tuple) and len(elem) > 1 else None) or from_key
        result[to_key] = dict_get_value(source=source,
                                        key_chain=list_unflatten(from_key))

    return result


def dict_listify(target: dict[Any,Any],
                 key_chain: list[str]) -> None:
    """
    Insert the value of the item pointed to by the key chain *[keys[0]: ... :keys[n]* in a list.

    This insertion will happen only if such a value is not itself a list.
    All lists eventually found, up to the penultimate key in the chain, will be processed recursively.

    :param target: the dictionary to be modified
    :param key_chain: the chain of nested keys pointing to the item in question
    """
    def items_listify(in_targets: list,
                      in_keys: list[str]) -> None:

        # traverse the list
        for in_target in in_targets:
            # is the element a dictionary ?
            if isinstance(in_target, dict):
                # yes, process it
                dict_listify(target=in_target,
                             key_chain=in_keys)
            # is the element a list ?
            elif isinstance(in_target, list):
                # yes, recursively process it
                # (key chain is also applicable to lists directly nested in lists)
                items_listify(in_targets=in_target,
                              in_keys=in_keys)

    parent: any = target
    # traverse the chain up to its penultimate key
    for inx, key in enumerate(key_chain[:-1]):
        parent = parent.get(key)
        # is the item a list ?
        if isinstance(parent, list):
            # yess, process it and close the operation
            items_listify(in_targets=parent,
                          in_keys=key_chain[inx+1:])
            parent = None

        # is it possible to proceed ?
        if not isinstance(parent, dict):
            # no, exit the loop
            break

    if isinstance(parent, dict) and len(key_chain) > 0:
        key: str = key_chain[-1]
        # does the item exist and is not a list ?
        if key in parent and not isinstance(parent.get(key), list):
            # yes, insert it in a list
            item: any = parent.pop(key)
            parent[key] = [item]


if __name__ == "__main__":

    s1 = {
        "a0": 0,
        "a1": {
            "b0": "qwert",
            "b1": {
                "c0": None,
                "c1": [1, {"d": [2, {"e": 3}, 4]}, {"d": 5}, {"d": [6, 7]}, [8, 9]]
            }
        }
    }
    mapping = [
        ("a0", "w0"),
        ("a1", "w1"),
        ("a1.b0", "w1.x0"),
        ("a1.b1", "w1.x1"),
        ("a1.b1.c0", "w1.x1.r.y0"),
        ("a1.b1.c1", "w1.x1.y1"),
        ("a1.b1.c1.d", "w1.x1.y1.z")
    ]
    s2 = dict_transform(s1, mapping)

    print(f"original dict:  {s1}")
    keys: list[str] = ["a1", "b1"]
    print(f"reduced chain:  {keys}")
    dict_reduce(s1, keys)
    print(f"reduced dict:   {s1}")
    keys = ["a1", "c1", "d"]
    print(f"listified chain: {keys}")
    dict_listify(s1, keys)
    print(f"listified dict:  {s1}")
    keys = ["a1", "c1", "d"]
    print(f"coalesced chain: {keys}")
    dict_coalesce(s1, keys)
    print(f"coalesced dict:   {s1}")
    print(f"mapping:          {mapping}")
    print(f"transformed dict: {s2}")
