def find_close(value,arr):
    size = len(arr)
    idx = 0
    val = abs(value - arr[idx])

    for i in range(1, size):
        val1 = abs(value - arr[i])
        if val1 < val:
            idx = i
            val = val1

    return arr[idx]
