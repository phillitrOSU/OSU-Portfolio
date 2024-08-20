# Name: Trevor Phillips
# OSU Email: phillitr@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - HashMap Implementation
# Due Date: 08/05/2022
# Description: Implementing a Hash Map.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        Adds a new key value pair to the hash map. If the key already exists, it's
        value is replaced with the new value.
        :param key: The key which can be hashed to a table index.
        :param value: The value stored at the key's index.
        """
        # Find the key's corresponding chain
        chain = self.get_chain(key)

        # Check if the key already exists -- if so, replace key's value.
        if self.replace_value(chain, key, value) == True:
            return

        # Otherwise insert the key/value pair.
        chain.insert(key, value)
        self._size = self._size + 1

    def compute_index(self, key: str) -> int:
        """
        Returns the hashed array index for a key.
        :param key: The key whose index is computed.
        :return int: The corresponding index in the bucket array.
        """
        hash = self._hash_function(key)

        # Adjust hash index to array length.
        return hash % self.get_capacity()

    def get_chain(self, key: str) -> LinkedList:
        """
        Returns the Linked List chain corresponding to hashed key.
        :param key: The key to be hashed.
        :return LinkedList: The chain in the bucket the key hashes to.
        """
        index = self.compute_index(key)
        return self._buckets[index]

    def replace_value(self, chain: object,  key: str, value: object) -> bool:
        """
        Attempt to replace the value of a key in a linked list.
        If the key is not in the list, return False
        :param chain: A linked list.
        :param key: The key being searched for.
        :param value: The value to replace the key's current value.
        :return bool: True if value replaced, False otherwise.
        """
        # If a key exists, replace and return True.
        key = chain.contains(key)
        if key:
            key.value = value
            return True

        # Otherwise return False
        return False

    def empty_buckets(self) -> int:
        """
        Returns the total number of unfilled buckets in the hash map.
        :return int: The number of empty buckets.
        """
        emptyBuckets = 0

        # Iterate through buckets and examine the chain in each.
        for index in range(self.get_capacity()):
            chain = self._buckets[index]
            # If list in bucket has length 0, it is empty.
            if chain.length() == 0:
                emptyBuckets += 1

        return emptyBuckets

    def table_load(self) -> float:
        """
        Returns the load factor of the hash table.
        :return float: Load factor
        """
        return self.get_size()/self.get_capacity()

    def clear(self) -> None:
        """
        Clears the contents of the hash map without changing capacity.
        """
        self._size = 0

        # Remove values from every bucket.
        for index in range(self._buckets.length()):
            self._buckets[index] = LinkedList()

    def resize_table(self, newCapacity: int) -> None:
        """
        Updates the capacity of the table and rehashes all existing key value pairs.
        :param new_capacity: The new capacity of the table.
        """
        if newCapacity < 1:
            return

        # Set new capacity to next prime if not prime.
        if self._is_prime(newCapacity) != True:
            newCapacity = self._next_prime(newCapacity)

        # Save old table values for reference.
        oldValues = self._buckets

        # Reinitialize table with new capacity.
        self._buckets = DynamicArray()
        self._capacity, self._size = newCapacity,0
        for _ in range(newCapacity):
            self._buckets.append(LinkedList())

        self.rehash(oldValues)

    def rehash(self, bucketArray) -> None:
        """
        Rehashes the values from a bucket array to self.
        """
        # Check each bucket for chain values.
        for index in range(bucketArray.length()):
            chain = bucketArray[index]
            # Map any chain key/value pairs to self.
            for link in chain:
                self.put(link.key, link.value)


    def get(self, key: str) -> object:
        """
        Returns the value associated with the key or None if key not in map.
        :param key: The key string.
        :return object: The value associated with the key.
        """
        # Search for the key in it's corresponding chain.
        chain = self.get_chain(key)
        node = chain.contains(key)

        # If found, return the key's value.
        if node:
            return node.value

        # If not found, return None.
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns true if a key is in the hash map. Otherwise returns false.
        :param key: The key being searched for.
        :return bool: True if found, False if not found.
        """
        # Search for the key in it's corresponding chain.
        chain = self.get_chain(key)
        if chain.contains(key):
            return True

        return False

    def remove(self, key: str) -> None:
        """
        Removes a key/value pair from the hash map. If the key does not exist, does nothing.
        :param key: The key to be removed
        """
        chain = self.get_chain(key)
        remove = chain.remove(key)

        # If successfully removed, reduce map size.
        if remove == True:
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a Dynamic Array of tuples with the key/value pairs in the map.
        """
        # Initialize key/value array.
        keyValArr = DynamicArray()

        # Iterate through map array, appending any key/value pairs from the chains.
        for index in range(self.get_capacity()):
            chain = self._buckets[index]

            for link in chain:
                pair = (link.key, link.value)
                keyValArr.append(pair)

        return keyValArr

def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    From a Dynamic Array of strings, returns a tuple containing a Dynamic Array
    of the mode values and an integer representing their frequency.
    :param da: An input Dynamic Array of strings
    :return tuple: (DynamicArray of Mode Values, Frequency)
    """
    # Map the frequency of each string in the input array.
    freqMap = map_frequencies(da)
    freqArr = freqMap.get_keys_and_values()

    # Initialize a mode array and set frequency/mode to first array value.
    modeArr = DynamicArray()
    initialVal, frequency = freqArr[0][0], freqArr[0][1]
    modeArr.append(initialVal)

    # Iterate through the freqArr, updating mode and freq if necessary.
    for index in range(1, freqArr.length()):
        currentVal, currentFreq = freqArr[index][0], freqArr[index][1]

        # If current value's frequency equal to mode frequency, append value to mode array.
        if currentFreq == frequency:
            modeArr.append(currentVal)

        # If current value's frequency greater than mode frequency, reinitialize
        # mode array with current value and set frequency to current.
        elif currentFreq > frequency:
            modeArr = DynamicArray()
            modeArr.append(currentVal)
            frequency = currentFreq

    return modeArr, frequency

def map_frequencies(da: DynamicArray) -> HashMap:
    """
    Receives a Dynamic Array of strings and creates a map of key/value
    pairs representing string/array frequency.
    :param da: An array of strings
    :return map: A hash map with key/value = string/frequency
    """
    map = HashMap()

    # Iterate through array. Add or update each value's frequency.
    for index in range(da.length()):
        val = da[index]
        oldFreq = map.get(val)

        # If no entry, initialize at 1.
        if not oldFreq:
            map.put(val, 1)

        # If already entry, increment.
        else:
            map.put(val, oldFreq + 1)

    return map

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

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

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
    m = HashMap(53, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(1)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
