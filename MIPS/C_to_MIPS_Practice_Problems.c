/*
 * C to MIPS Conversion Practice Problems
 * 
 * Instructions: Translate each of the following C functions into MIPS assembly language.
 * Assume standard MIPS calling conventions:
 * - Arguments passed in $a0-$a3
 * - Return value in $v0
 * - Saved registers $s0-$s7 must be preserved if used
 * - Return address $ra must be preserved for non-leaf functions
 */

// ==========================================
// Problem 1: Loop and Arithmetic (Iterative Factorial)
// Difficulty: Low-Medium
// Concept: Basic loop, multiplication
// ==========================================
int factorial(int n) {
    int result = 1;
    for (int i = 1; i <= n; i++) {
        result = result * i;
    }
    return result;
}

// ==========================================
// Problem 2: If-Else and Logical Operators
// Difficulty: Low-Medium
// Concept: Branching, logical AND/OR
// ==========================================
int check_range(int x, int y) {
    if (x > 0 && y > 0) {
        if (x > 100 || y > 100) {
            return 2;
        } else {
            return 1;
        }
    } else if (x < 0) {
        return -1;
    }
    return 0;
}

// ==========================================
// Problem 3: String Length (Pointer Arithmetic)
// Difficulty: Medium
// Concept: Loading bytes, looping until null terminator
// ==========================================
int string_length(char *str) {
    int len = 0;
    while (*str != '\0') {
        len++;
        str++;
    }
    return len;
}

// ==========================================
// Problem 4: Array Processing with Max Finding
// Difficulty: Medium
// Concept: Array access (base + offset), conditional update
// ==========================================
int find_max(int arr[], int size) {
    int max = arr[0];
    for (int i = 1; i < size; i++) {
        if (arr[i] > max) {
            max = arr[i];
        }
    }
    return max;
}

// ==========================================
// Problem 5: Recursive Fibonacci
// Difficulty: High
// Concept: Recursion, Stack management (saving $ra, $a0, $s0)
// ==========================================
int fibonacci(int n) {
    if (n == 0) return 0;
    if (n == 1) return 1;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// ==========================================
// Problem 6: Bubble Sort (Nested Loops)
// Difficulty: High
// Concept: Nested loops, array swapping, multiple registers
// ==========================================
void bubble_sort(int arr[], int n) {
    int i, j, temp;
    for (i = 0; i < n - 1; i++) {
        for (j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                // Swap
                temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}

// ==========================================
// Problem 7: Recursive Power Function
// Difficulty: Medium-High
// Concept: Simple recursion, multiplication
// ==========================================
int power(int base, int exp) {
    if (exp == 0)
        return 1;
    else
        return base * power(base, exp - 1);
}

// ==========================================
// Problem 8: Palindrome Check (Strings & Indexes)
// Difficulty: High
// Concept: Double variables (start/end indexes), byte comparison
// ==========================================
int is_palindrome(char *str, int len) {
    int start = 0;
    int end = len - 1;
    while (start < end) {
        if (str[start] != str[end]) {
            return 0; // False
        }
        start++;
        end--;
    }
    return 1; // True
}

// ==========================================
// Problem 9: Switch Case equivalent
// Difficulty: Medium
// Concept: Jump table or chain of branch if-else
// ==========================================
int calculate(int op, int a, int b) {
    int result = 0;
    switch(op) {
        case 0: result = a + b; break;
        case 1: result = a - b; break;
        case 2: result = a & b; break;
        case 3: result = a | b; break;
        default: result = -1; break;
    }
    return result;
}

// ==========================================
// Problem 10: Complex Mix (Non-leaf function calling another)
// Difficulty: Very High
// Concept: Function arguments preservation across calls
// ==========================================
int sum_squares(int n) {
    int sum = 0;
    for (int i = 1; i <= n; i++) {
        sum = sum + square(i); // Assume square(x) returns x*x
    }
    return sum;
}

int square(int x) {
    return x * x;
}
