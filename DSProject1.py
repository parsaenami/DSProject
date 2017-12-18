import time


class Node:
    def __init__(self,
                 service_name,
                 car_model=None,
                 costumer_description=None,
                 agency_description=None,
                 price=None):
        self.next = None
        self.next_sub = None

        self.service_name = service_name
        self.car_model = car_model
        self.costumer_description = costumer_description
        self.agency_description = agency_description
        self.price = price

        self.next_list = []
        self.child = []

        self.heap1 = MaxHeap()
        self.heap2 = MaxHeap()
        self.heap3 = MaxHeap()


# noinspection PyRedeclaration,PyGlobalUndefined
class LinkedList:
    global save
    global lll
    global children

    save = []
    lll = []
    children = []

    def __init__(self):
        self.root = None

    def size(self):
        current = self.root
        count = 0

        while current is not None:
            count = count + 1
            current = current.next

        return count

    def is_empty(self):
        return self.root is None

    def add_service(self, service_name):
        temp = Node(service_name)
        current = self.root
        check = True

        if self.is_empty():
            self.root = temp

        else:
            while current is not None:
                if current.service_name == service_name:
                    print('Already added!')
                    check = False
                    return

                cur = current
                current = current.next
            if check:
                cur.next = temp
        if check:
            save.append(temp)

    def add_subservice3(self, subservice_name, service_name):
        if self.search3(subservice_name) is not None:
            print('already added!')
            return

        temp = Node(subservice_name)
        p = self.search3(service_name)

        if p is None:
            print('There is no such service!')

        if p.next_sub is not None:
            p = p.next_sub

            while p.next is not None:
                p = p.next

            p.next = temp

        else:
            p.next_sub = temp

        save.append(temp)

    def search3(self, item):
        for n in save:
            if n.service_name == item:
                return n

    def general_delete(self, service_name):
        current = self.root
        is_found = False

        if current.service_name == service_name:
            if current.next is not None:
                self.root, current = current.next, self.root
                is_found = True

            else:
                k = []
                for node in save:
                    if node in self.child(service_name):
                        k.append(node)

                for ks in k:
                    save.remove(ks)

                self.root = None
                return
        else:
            while current.next is not None:
                if current.next.service_name == service_name:
                    is_found = True
                    break

                current = current.next

        if is_found:
            k = []
            for node in save:
                if node in self.child(service_name):
                    k.append(node)

            for ks in k:
                save.remove(ks)
            current.next = current.next.next

    def in_agencies(self, service_name):
        provided = 0

        for a in save:
            if service_name in a.next_list:
                provided += 1

        return provided

    def delete(self, service_name, agency_name, services_list):
        if self.is_empty():
            print('There is nothing to delete!')
            return

        if self.search3(agency_name) is None:
            print('There is no such agency!')
            return

        current = self.root

        while current.service_name != agency_name:
            current = current.next

        if service_name in current.next_list:
            current.next_list.remove(service_name)

            if self.in_agencies(service_name) == 0:
                services_list.general_delete(service_name)

        else:
            print('There is no such service!')

    def add_offer(self, service_name, agency_name):
        current = self.root

        if self.search3(agency_name) is None:
            print('There is no such agency!')
            return

        if self.search3(service_name) is None:
            print('There is no such service!')
            return

        while current.service_name != agency_name:
            current = current.next

        if service_name not in current.next_list:
            current.next_list.append(service_name)

        else:
            print('Already added!')

    def add_agency(self, agency_name):
        self.add_service(agency_name)

    def list_agencies(self):
        if self.is_empty():
            print('There are no agencies yet!')
            return

        current = self.root

        while current.next is not None:
            print(current.service_name, end=',')
            current = current.next

        print(current.service_name)

    def list_services(self, service_name=None):
        if self.is_empty():
            print('There are no services yet!', end='')
            return

        current = self.root
        temp = self.root

        if service_name is None:
            while current is not None:
                if current.next_sub is None and current.next is None:
                    print(current.service_name, end='')

                elif current.next_sub is None and current.next is not None:
                    print(current.service_name, end=',')

                else:
                    print(current.service_name, end='<')

                if current.next_sub is not None:
                    t = current
                    self.root = current.next_sub
                    self.list_services()
                    self.root = t
                    print('>', end='')

                current = current.next

        else:
            if self.search3(service_name) is None:
                print('There is no such service!')
                return

            current = self.search3(service_name)
            self.root = current

            if current.next_sub is None and current.next is None:
                print(current.service_name, end='')

            elif current.next_sub is None and current.next is not None:
                print(current.service_name, end=',')

            else:
                print(current.service_name, end='<')

            current = current.next_sub
            while current is not None:
                if current.next_sub is not None:
                    tmp = self.root
                    self.root = current.next_sub
                    if current.next_sub is None and current.next is None:
                        print(current.service_name, end='')

                    elif current.next_sub is None and current.next is not None:
                        print(current.service_name, end=',')

                    else:
                        print(current.service_name, end='<')

                    self.list_services()
                    self.root = tmp
                    print('>', end='')

                else:
                    if current.next_sub is None and current.next is None:
                        print(current.service_name, end='')

                    elif current.next_sub is None and current.next is not None:
                        print(current.service_name, end=',')

                    else:
                        print(current.service_name, end='<')

                current = current.next

            print('>', end='')

        self.root = temp

    def child(self, service_name):
        if self.is_empty():
            print('Empty list!')
            return

        temp = self.root
        current = self.search3(service_name)
        self.root = current
        children.append(current)
        current = current.next_sub

        while current is not None:
            if current.next_sub is not None:
                tmp = self.root
                self.root = current.next_sub
                self.child(current.service_name)
                self.root = tmp

            else:
                children.append(current)

            current = current.next

        self.root = temp
        res = children

        return res

    # noinspection PyTypeChecker
    def order(self, service_name, agency_name, customer_name, immediacy_level, car_model=None):
        agency = self.search3(agency_name)
        is_found = False

        if agency is None:
            print('There is no such agency!')
            return

        for se in agency.next_list:
            searching = self.child(se)
            for n in searching:
                if service_name == n.service_name:
                    is_found = True
                    temp = HeapNode(service_name, immediacy_level, customer_name, agency_name, car_model)

                    if immediacy_level == 'high':
                        agency.heap1.__add__(temp)
                        break

                    elif immediacy_level == 'normal':
                        agency.heap2.__add__(temp)
                        break

                    elif immediacy_level == 'low':
                        agency.heap3.__add__(temp)
                        break

                    else:
                        print('Wrong priority level!\nFollow the instruction.')
                        # searching.clear()

                        # else:
                        #     print('This agency do not have your required service!')

            searching.clear()

        if not is_found:
            print('This agency do not have your required service!')

    def list_orders(self, agency_name):
        agency = self.search3(agency_name)

        if agency is None:
            print('There is no such agency!')

        if agency.heap1.__len__() == agency.heap2.__len__() == agency.heap3.__len__() == 0:
            print('There are no orders right now!')

        while agency.heap1.__len__() != 0:
            agency.heap1.__del__()

        while agency.heap2.__len__() != 0:
            agency.heap2.__del__()

        while agency.heap3.__len__() != 0:
            agency.heap3.__del__()


class HeapNode:
    def __init__(self, service_name, priority_level, customer_name, agency_name, car_model=None):
        self.service = service_name
        self.customer = customer_name
        self.agency = agency_name
        self.priority = priority_level
        self.car = car_model

        self.real_time = time.ctime().split()[3]

        self.time = time.time() * -1

    def __str__(self):
        if self.car is None:
            print('- Customer "{}" has requested service "{}" from agency "{}" with "{}" priority in "{}"'.format(
                self.customer, self.service, self.agency, self.priority, self.real_time))

        else:
            print(
                '- Customer "{}" has requested service "{}" for car "{}" from agency "{}" with "{}" priority in "{}"'.format(
                    self.customer, self.service, self.car, self.agency, self.priority, self.real_time))


class MaxHeap:
    def __init__(self):
        self.data = []

    def __add__(self, item):
        self.data.append(item)
        self.arrange(self.__len__() - 1)

    def __del__(self):
        if self.__len__() == 0:
            return 'Error'

        elif self.__len__() == 1:
            res = self.data.pop()

        else:
            self.swap(0, self.__len__() - 1)
            res = self.data.pop()
            self.arrange(0, False)

        return res.__str__()

    def __len__(self):
        return len(self.data)

    def swap(self, i, j):
        self.data[i], self.data[j] = self.data[j], self.data[i]

    def arrange(self, index, is_up=True):
        if is_up:
            parent = index // 2

            if index == 0:
                return

            elif self.data[parent].time < self.data[index].time:
                self.swap(index, parent)
                self.arrange(parent)

        else:
            rc = 2 * index + 2
            lc = 2 * index + 1
            hl = self.__len__()

            if hl > rc:
                r, l, p = self.data[rc].time, self.data[lc].time, self.data[index].time

                if p > r and p > l:
                    return

                elif (l < p < r) or (p < l < r):
                    self.swap(index, rc)
                    self.arrange(rc, False)

                elif (l > p > r) or (l > r > p):
                    self.swap(index, lc)
                    self.arrange(lc, False)


if __name__ == '__main__':

    agencies = LinkedList()
    services = LinkedList()

    print(45 * '*')
    print('\t\tWelcome to parsa\'s car agency!'.upper())
    print(45 * '*')
    print('Note1: Type "EXIT" when you wanted to quit.')
    print(45 * '-')
    print('Note2: Type "HELP" for allowed commands.')
    print(45 * '-')
    while True:
        inp = input('Enter a command: ').split()

        if len(inp) == 0:
            print('No command entered!')

        elif inp[0] == 'EXIT':
            break

        elif inp[0] == 'free':
            pass
            # agencies.add_agency('a1')
            # agencies.add_agency('a2')
            # agencies.add_agency('a3')
            #
            # services.add_service('s1')
            # services.add_service('s2')
            # services.add_service('s3')
            #
            # services.add_subservice3('s11', 's1')
            # services.add_subservice3('s21', 's2')
            #
            # agencies.add_offer('s1', 'a1')
            # agencies.add_offer('s2', 'a1')
            # agencies.add_offer('s1', 'a2')

        elif inp[0] == 'HELP':
            print(45 * '-')
            print('1. add an agency : \n\t>>> add agency <agency_name>\n', 45 * '-')
            print('2. add a service : \n\t>>> add agency <service_name>\n', 45 * '-')
            print('3. add a subservice to a service : \n\t>>> add subservice <subservice_name> to <service_name>\n',
                  45 * '-')
            print('4. add a service to an agency : \n\t>>> add offer <service_name> to <agency_name>\n', 45 * '-')
            print('5. list all available services : \n\t>>> list services\n', 45 * '-')
            print('6. list all services of a particular service : \n\t>>> list services from <service_name>\n',
                  45 * '-')
            print('7. list all agencies : \n\t>>> list agencies\n', 45 * '-')
            print('8. list all requests from an agency : \n\t>>> list orders of <agency_name>\n', 45 * '-')
            print('9. delete a service from an agency : \n\t>>> delete <service_name> from <agency_name>\n', 45 * '-')
            print('10. send a request for a service from an agency : \n\t>>> order <service_name> from <agency_name> by'
                  ' <customer_name> with <immediacy_level> priority\n', 45 * '-')
            print('11. priority levels; choose one of them for sending request :\n\t1. high\n\t2. normal\n\t3. low')

        elif inp[0] == 'add':
            if inp[1] in 'service':
                try:
                    services.add_service(inp[2])
                except:
                    print('Wrong command!\nCheck out the instruction with "HELP" command.')

            elif inp[1] in 'subservice':
                try:
                    services.add_subservice3(inp[2], inp[4])
                except:
                    print('Wrong command!\nCheck out the instruction with "HELP" command.')

            elif inp[1] in 'agency':
                try:
                    agencies.add_agency(inp[2])
                except:
                    print('Wrong command!\nCheck out the instruction with "HELP" command.')

            elif inp[1] in 'offer':
                try:
                    agencies.add_offer(inp[2], inp[4])
                except:
                    print('Wrong command!\nCheck out the instruction with "HELP" command.')

            else:
                print('Wrong command!\nCheck out the instruction with "HELP" command.')

        elif inp[0] == 'delete':
            try:
                agencies.delete(inp[1], inp[3], services)
            except:
                print('Wrong command!\nCheck out the instruction with "HELP" command.')

        elif inp[0] == 'list':
            if inp[1] in '‫‪agencies‬‬':
                try:
                    agencies.list_agencies()
                except:
                    print('Wrong command!\nCheck out the instruction with "HELP" command.')

            elif inp[1] in '‫‪services‬‬' and len(inp) > 2 and inp[2] in 'from':
                try:
                    services.list_services(inp[3])
                except:
                    print('Wrong command!\nCheck out the instruction with "HELP" command.')
                print()

            elif inp[1] in '‫‪services‬‬':
                try:
                    services.list_services()
                except:
                    print('Wrong command!\nCheck out the instruction with "HELP" command.')
                print()

            elif inp[1] in 'orders':
                try:
                    agencies.list_orders(inp[3])
                except:
                    print('Wrong command!\nCheck out the instruction with "HELP" command.')
                    print()

            else:
                print('Wrong command!\nCheck out the instruction with "HELP" command.')

        elif inp[0] == 'order':
            try:
                agencies.order(inp[1], inp[3], inp[5], inp[7])
            except:
                print('Wrong command!\nCheck out the instruction with "HELP" command.')

        else:
            print('Wrong command!\nCheck out the instruction with "HELP" command.')
        print(45 * '-')
