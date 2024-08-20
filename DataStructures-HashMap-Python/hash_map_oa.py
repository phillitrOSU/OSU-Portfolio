# Name: Trevor Phillips
# OSU Email: phillitr@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - Open Addressing HashMap Implementation
# Due Date: 08/05/2022
# Description: Implementing an open addressing Hash Map.


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)

class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Adds a new key/value pair to the map, or updates the key value
        if the key already exists.
        :param key: The key to be hashed.
        :param value: The value stored with the key.
        """
        # Check load and resize if necessary.
        self.check_load_and_resize()

        # Hash key to index.
        index, status = self.compute_index(key, 'insertion')

        # If filling empty bucket, increase size.
        if status == 'empty':
            self._size += 1

        # Insert or update key/value pair as hash entry.
        self._buckets[index] = HashEntry(key, value)

    def compute_index(self, key: str, method: str) -> (int, str):
        """
        Returns an insertion index for a hashed key.
        :param key: The key whose index is computed.
        :param method: 'insert' if searching for empty insertion index. 'search' if searching for key.
        """
        # Compute initial index and bucket.
        hash = self._hash_function(key)
        initialIndex = hash % self.get_capacity()
        index = initialIndex

        # Set probing variables.
        j, m = 1, self.get_capacity()

        status = 'empty'

        # While bucket filled.
        while self._buckets[index] != None:
            # Note: method value should be set to 'search' or 'insert'. If inserting, we
            # return the index from tombstone entries as they are functionally empty.
            # If searching we continue probing past tombstone entries.
            
            # If inserting and bucket is tombstone (empty), return insertion index.
            if self._buckets[index].is_tombstone == True and method == 'insert':
                break

            # If duplicate key, return index.
            if self._buckets[index].key == key:
                # If value is active, set status to duplicate.
                if self._buckets[index].is_tombstone == False:
                    status = 'duplicate'
                break

            # Otherwise update index with quadratic probing.
            else:
                index = (initialIndex + j**2) % m
                j += 1

        return index, status

    def check_load_and_resize(self) -> None:
        """
        Checks the table's current load factor and resizes the table if
        the load is greater than .5
        """
        # If table load greater than .5, resize table to double capacity.
        if self.table_load() >= .5:
            self.resize_table(self._capacity * 2)

    def table_load(self) -> float:
        """
        Returns the load factor of the table.
        """
        return self.get_size() / self.get_capacity()

    def empty_buckets(self) -> int:
        """
        Returns the total number of unfilled buckets in the hash map.
        :return 'EmptyBuckets': The number of empty buckets.
        """
        emptyBuckets = 0

        # Iterate through buckets array and tally empty buckets.
        for index in range(self.get_capacity()):
            if self._buckets[index] == None:
                emptyBuckets += 1

        return emptyBuckets

    def resize_table(self, newCapacity: int) -> None:
        """
        Updates the capacity of the table and rehashes all existing key/value pairs.
        :param new_capacity: The new capacity of the table.
        """
        if newCapacity < self.get_size():
            return

        # Set new capacity to next prime if not prime.
        if self._is_prime(newCapacity) != True:
            newCapacity = self._next_prime(newCapacity)

        # Save old table values for reference.
        oldValues = self._buckets

        # Reinitialize table with new capacity.
        self._buckets = DynamicArray()
        self._capacity, self._size = newCapacity, 0
        for _ in range(newCapacity):
            self._buckets.append(None)

        # Rehash old values into new table.
        self.rehash(oldValues)

    def rehash(self, bucketArray: DynamicArray) -> None:
        """
        Rehashes the values from a bucket array to self.
        """
        for index in range(bucketArray.length()):
            entry = bucketArray[index]
            # If entry is valid, map to self.
            if entry != None and entry.is_tombstone != True:
                self.put(entry.key, entry.value)

    def get(self, key: str) -> object:
        """
        Returns the value associated the key. If key not in map, returns None.
        :param key: string
        :return object: value associated with key, or None if key not found.
        """
        # Search for the key.
        index, status = self.compute_index(key, 'search')

        # If key hashes to an empty index, key is not in map.
        if status == 'empty':
            return None

        # Otherwise return key's value.
        return self._buckets[index].value

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the key is in the map, false otherwise.
        :param key: string.
        :return bool: True if found, False if not found.
        """
        #Search for the key.
        index, status = self.compute_index(key, 'search')

        # If key hashes to an empty index, key is not in map.
        if status == 'empty':
            return False

        # Key found.
        return True

    def remove(self, key: str) -> None:
        """
        Removes a key from the map and updates the index with a tombstone marker.
        :param key: string
        :return: None
        """
        index, status = self.compute_index(key, 'search')

        # If key hashes to an empty index, key is not in map. Do nothing.
        if status == 'empty':
            return

        # Otherwise set the key to a tombstone and decrement size.
        self._buckets[index].is_tombstone = True
        self._size -= 1

    def clear(self) -> None:
        """
        Clears the maps' contents without changing its underlying capacity.
        :return: None
        """
        # Set size to zero
        self._size = 0

        # Generate a new empty bucket array.
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(None)

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array of tuples representing key/value pairs stored in the map.
        :return: Dynamic Array
        """
        keyValArr = DynamicArray()

        # Iterate through map.
        for index in range(self._capacity):
            # If valid key/value pair, append to key value array.
            if self._buckets[index] != None and self._buckets[index].is_tombstone != True:
                key, value = self._buckets[index].key, self._buckets[index].value
                keyValArr.append((key, value))

        return keyValArr

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2), m.get_size())
    m.put('key1', 10)
    print(round(m.table_load(), 2),m.get_size())
    m.put('key2', 20)
    print(round(m.table_load(), 2),m.get_size())
    m.put('key1', 30)
    print(round(m.table_load(), 2),m.get_size())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())
