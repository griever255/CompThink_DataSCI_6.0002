###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    global calls 
    calls += 1
    minEggs = target_weight
    if target_weight in egg_weights:
        memo[target_weight] = 1
        return 1
    elif target_weight in memo.keys(): 
        return memo[target_weight]
    else:
        for e in egg_weights:
            if e <= target_weight:
                numEggs = 1 + dp_make_weight(egg_weights, target_weight - e, memo)
            if numEggs < minEggs:
                minEggs = numEggs
                memo[target_weight] = numEggs
    return minEggs
    

# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    global calls
    calls = 0
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n, {}))
    print(f"Recursive calls = {calls}")
    print()

    calls = 0
    egg_weights = (1, 5, 24, 25)
    n = 72
    print("Egg weights = (1, 5, 24, 25)")
    print("n = 72")
    print("Expected output: 3 (3 * 24 = 72)")
    print("Actual output:", dp_make_weight(egg_weights, n, {}))
    print(f"Recursive calls = {calls}")
    print()