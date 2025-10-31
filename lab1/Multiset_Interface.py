from Multiset import Multiset

def main():
    """
    @brief Interactive REPL interface for manipulating Multiset objects.
    @details Allows users to define named multisets, perform operations on them, and inspect their state.
             Supports union, intersection, subtraction, cardinality, boolean construction, and element deletion.

    @command A = {a, b, {c, d}, a}   Defines a new multiset named A with specified elements.
    @command list                    Lists all defined multisets and their contents.
    @command show A                 Displays the contents of multiset A.
    @command delete A a             Removes all instances of element 'a' from multiset A.
    @command ndelete A a:2          Removes 2 instances of element 'a' from multiset A.
    @command isempty A              Checks whether multiset A is empty.
    @command cardinality A          Returns the total number of elements in multiset A.
    @command rm A                   Deletes multiset A entirely.
    @command A + B                  Displays the union of multisets A and B.
    @command A += B                 Updates multiset A with the union of A and B.
    @command A - B                  Displays the subtraction of B from A.
    @command A -= B                 Updates multiset A by subtracting B.
    @command A * B                  Displays the intersection of multisets A and B.
    @command A *= B                 Updates multiset A with its intersection with B.
    @command bolean A               Constructs and displays all possible subsets of multiset A.
    @command help                   Displays all available commands and formats.
    @command exit                   Terminates the program.

    @return None
    """

    multisets = {}
    
    print('''
        Enter multiset in the following format: A = {a, b, {c, d}, a}
        Available commands:
            list            check list of multisets
            show A          show multiset A
            delete A a      remove element from multiset
            ndelete A a:2   remove a specified number of instances of an element
            isempty A       check for empty multiset
            cardinality A   count cardinality A
            rm A            remove multiset A
            A + B           union A and B
            A += B          save result union in A
            A - B           substract from A to B
            A -= B          save result substaction in A
            A * B           intersection between A and B
            A *= B          save result intersection in A
            bolean A        create bolean from A
            help            show all available commands
            exit            stop programm
    ''')

    while True:
        try:
            choice = input('').strip()
            parts = choice.split()

            if not parts:
                continue

            if parts[0] == 'list':
                for name in multisets:
                    print(f"{name} = {multisets[name]}")

            elif parts[0] == 'show' and len(parts) > 1 and parts[1] in multisets:
                print(f"{parts[1]} = {multisets[parts[1]]}")

            elif parts[0] == 'delete' and len(parts) > 2 and parts[1] in multisets:
                if parts[2] in multisets[parts[1]].multiset:
                    multisets[parts[1]].delete(parts[2])
                else:
                    print(f"Element '{parts[2]}' not found in {parts[1]}")

            elif parts[0] == 'ndelete' and len(parts) > 2 and parts[1] in multisets and ':' in parts[2]:
                elem, num = parts[2].split(':', 1)
                multisets[parts[1]].ndelete(elem, int(num))

            elif parts[0] == 'isempty' and len(parts) > 1 and parts[1] in multisets:
                print(f"{parts[1]} is empty: {multisets[parts[1]].is_empty()}")

            elif parts[0] == 'cardinality' and len(parts) > 1 and parts[1] in multisets:
                print(f"Cardinality of {parts[1]}: {multisets[parts[1]].cardinality()}")

            elif parts[0] == 'rm' and len(parts) > 1 and parts[1] in multisets:
                del multisets[parts[1]]

            elif len(parts) == 3 and parts[1] == '+' and parts[0] in multisets and parts[2] in multisets:
                print(multisets[parts[0]] + multisets[parts[2]])

            elif len(parts) == 3 and parts[1] == '+=' and parts[0] in multisets and parts[2] in multisets:
                multisets[parts[0]] += multisets[parts[2]]

            elif len(parts) == 3 and parts[1] == '-' and parts[0] in multisets and parts[2] in multisets:
                print(multisets[parts[0]] - multisets[parts[2]])

            elif len(parts) == 3 and parts[1] == '-=' and parts[0] in multisets and parts[2] in multisets:
                multisets[parts[0]] -= multisets[parts[2]]

            elif len(parts) == 3 and parts[1] == '*' and parts[0] in multisets and parts[2] in multisets:
                print(multisets[parts[0]] * multisets[parts[2]])

            elif len(parts) == 3 and parts[1] == '*=' and parts[0] in multisets and parts[2] in multisets:
                multisets[parts[0]] *= multisets[parts[2]]

            elif parts[0] == 'bolean' and len(parts) > 1 and parts[1] in multisets:
                result = multisets[parts[1]].bolean()
                print(f"Bolean {parts[1]} contains {len(result)} subsets:")
                for subset in result:
                    print(subset)

            elif '=' in choice:
                name, mul = choice.split('=', 1)
                multisets[name.strip()] = Multiset(mul.strip())

            elif parts[0] == 'help':
                print('''
                    Enter multiset in the following format: A = {a, b, {c, d}, a}
                    Available commands:
                        list            check list of multisets
                        show A          show multiset A
                        delete A a      remove element from multiset
                        ndelete A a:2   remove a specified number of instances of an element
                        isempty A       check for empty multiset
                        cardinality A   count cardinality A
                        rm A            remove multiset A
                        A + B           union A and B
                        A += B          save result union in A
                        A - B           substract from A to B
                        A -= B          save result substaction in A
                        A * B           intersection between A and B
                        A *= B          save result intersection in A
                        bolean A        create bolean from A
                        help            show all available commands
                        exit            stop programm
                ''')

            elif parts[0] == 'exit':
                return

            else:
                print('Wrong command. Try again.')

        except Exception as e:
            print(f"⚠️ Error: {e}")

main()