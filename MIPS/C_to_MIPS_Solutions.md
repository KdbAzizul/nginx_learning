# C to MIPS Conversion Solutions

This document contains the MIPS assembly solutions for the problems found in `C_to_MIPS_Practice_Problems.c`.

---

## 1. Factorial (Loop)
### C Code
```c
int factorial(int n) {
    int result = 1;
    for (int i = 1; i <= n; i++) {
        result = result * i;
    }
    return result;
}
```

### MIPS Assembly
```asm
# Arguments: $a0 = n
# Returns: $v0 = result
factorial:
    li      $v0, 1              # result = 1
    li      $t0, 1              # i = 1

loop_fact:
    bgt     $t0, $a0, end_fact  # if i > n, exit loop
    mul     $v0, $v0, $t0       # result = result * i
    addi    $t0, $t0, 1         # i++
    j       loop_fact

end_fact:
    jr      $ra                 # return result
```

---

## 2. Check Range (If-Else Logic)
### C Code
```c
int check_range(int x, int y) {
    if (x > 0 && y > 0) {
        if (x > 100 || y > 100) return 2;
        else return 1;
    } else if (x < 0) {
        return -1;
    }
    return 0;
}
```

### MIPS Assembly
```asm
# Arguments: $a0 = x, $a1 = y
# Returns: $v0
check_range:
    # if (x > 0 && y > 0)
    blez    $a0, check_x_neg    # if x <= 0, jump to else-if check
    blez    $a1, check_x_neg    # if y <= 0, logic fails (but C code implies strictly nested, simplified here)
                                # Actually, if x>0 is true, we check y>0. if y<=0, we fall through to return 0? 
                                # C logic: if (x>0 && y>0) { ... } else if (x<0) ...
                                # If x>0 but y<=0, it skips the first block. Since x is not < 0, it falls to return 0.
                                # So branching to 'check_x_neg' is correct because that label checks x<0.

    # Inside if (x > 0 && y > 0)
    # if (x > 100 || y > 100)
    li      $t0, 100
    bgt     $a0, $t0, ret_two   # if x > 100 -> return 2
    bgt     $a1, $t0, ret_two   # if y > 100 -> return 2

    # else return 1
    li      $v0, 1
    jr      $ra

ret_two:
    li      $v0, 2
    jr      $ra

check_x_neg:
    # else if (x < 0)
    bge     $a0, $zero, ret_zero # if x >= 0, skip
    li      $v0, -1
    jr      $ra

ret_zero:
    li      $v0, 0
    jr      $ra
```

---

## 3. String Length
### C Code
```c
int string_length(char *str) {
    int len = 0;
    while (*str != '\0') {
        len++;
        str++;
    }
    return len;
}
```

### MIPS Assembly
```asm
# Arguments: $a0 = str pointer
# Returns: $v0 = len
string_length:
    li      $v0, 0              # len = 0

loop_len:
    lb      $t0, 0($a0)         # load byte *str
    beq     $t0, $zero, end_len # if *str == '\0', exit
    
    addi    $v0, $v0, 1         # len++
    addi    $a0, $a0, 1         # str++
    j       loop_len

end_len:
    jr      $ra
```

---

## 4. Find Max in Array
### C Code
```c
int find_max(int arr[], int size) {
    int max = arr[0];
    for (int i = 1; i < size; i++) {
        if (arr[i] > max) max = arr[i];
    }
    return max;
}
```

### MIPS Assembly
```asm
# Arguments: $a0 = arr, $a1 = size
# Returns: $v0 = max
find_max:
    lw      $v0, 0($a0)         # max = arr[0]
                                # Note: Assumes size >= 1
    li      $t0, 1              # i = 1

loop_max:
    bge     $t0, $a1, end_max   # if i >= size, exit

    sll     $t1, $t0, 2         # i * 4
    add     $t1, $a0, $t1       # arr + offset
    lw      $t2, 0($t1)         # t2 = arr[i]

    ble     $t2, $v0, next_iter # if arr[i] <= max, skip
    move    $v0, $t2            # max = arr[i]

next_iter:
    addi    $t0, $t0, 1         # i++
    j       loop_max

end_max:
    jr      $ra
```

---

## 5. Recursive Fibonacci
### C Code
```c
int fibonacci(int n) {
    if (n == 0) return 0;
    if (n == 1) return 1;
    return fibonacci(n - 1) + fibonacci(n - 2);
}
```

### MIPS Assembly
```asm
# Arguments: $a0 = n
# Returns: $v0
fibonacci:
    # Base cases
    beqz    $a0, ret_n          # if n == 0 return 0
    li      $t0, 1
    beq     $a0, $t0, ret_n     # if n == 1 return 1

    # Recursive step
    addi    $sp, $sp, -12       # Allocate stack frame
    sw      $ra, 8($sp)         # Save return address
    sw      $s0, 4($sp)         # Save s0 (to hold n)
    sw      $s1, 0($sp)         # Save s1 (to hold result of fib(n-1))

    move    $s0, $a0            # s0 = n

    addi    $a0, $s0, -1        # n - 1
    jal     fibonacci
    move    $s1, $v0            # s1 = fib(n-1)

    addi    $a0, $s0, -2        # n - 2
    jal     fibonacci           # v0 = fib(n-2)

    add     $v0, $s1, $v0       # result = fib(n-1) + fib(n-2)

    lw      $ra, 8($sp)
    lw      $s0, 4($sp)
    lw      $s1, 0($sp)
    addi    $sp, $sp, 12
    jr      $ra

ret_n:
    move    $v0, $a0            # return n (0 or 1)
    jr      $ra
```

---

## 6. Bubble Sort
### C Code
```c
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
```

### MIPS Assembly
```asm
# Arguments: $a0 = arr, $a1 = n
bubble_sort:
    addi    $sp, $sp, -20       # While leaf, we use s-registers for vars
    sw      $s0, 16($sp)        # i
    sw      $s1, 12($sp)        # j
    sw      $s2, 8($sp)         # base of arr
    sw      $s3, 4($sp)         # n
    
    move    $s2, $a0
    move    $s3, $a1

    li      $s0, 0              # i = 0
loop_i_sort:
    addi    $t0, $s3, -1        # n - 1
    bge     $s0, $t0, end_sort  # if i >= n-1, exit

    li      $s1, 0              # j = 0
loop_j_sort:
    sub     $t1, $s3, $s0       # n - i
    addi    $t1, $t1, -1        # n - i - 1
    bge     $s1, $t1, next_i    # if j >= n - i - 1, next i

    # Load arr[j] and arr[j+1]
    sll     $t2, $s1, 2         # j * 4
    add     $t2, $s2, $t2       # arr + (j*4) -> &arr[j]
    lw      $t3, 0($t2)         # arr[j]
    lw      $t4, 4($t2)         # arr[j+1] (next word)

    ble     $t3, $t4, next_j    # if arr[j] <= arr[j+1], no swap

    # Swap
    sw      $t4, 0($t2)         # arr[j] = arr[j+1]
    sw      $t3, 4($t2)         # arr[j+1] = temp (old arr[j])

next_j:
    addi    $s1, $s1, 1         # j++
    j       loop_j_sort

next_i:
    addi    $s0, $s0, 1         # i++
    j       loop_i_sort

end_sort:
    lw      $s0, 16($sp)
    lw      $s1, 12($sp)
    lw      $s2, 8($sp)
    lw      $s3, 4($sp)
    addi    $sp, $sp, 20
    jr      $ra
```

---

## 7. Recursive Power
### C Code
```c
int power(int base, int exp) {
    if (exp == 0) return 1;
    else return base * power(base, exp - 1);
}
```

### MIPS Assembly
```asm
# Arguments: $a0 = base, $a1 = exp
# Returns: $v0
power:
    # Base case
    bne     $a1, $zero, recurse_pow
    li      $v0, 1
    jr      $ra

recurse_pow:
    addi    $sp, $sp, -8
    sw      $ra, 4($sp)
    sw      $a0, 0($sp)         # Save base (since we need it after call)

    addi    $a1, $a1, -1        # exp - 1
    jal     power               # power(base, exp-1)

    lw      $a0, 0($sp)         # Restore base
    mul     $v0, $a0, $v0       # base * result

    lw      $ra, 4($sp)
    addi    $sp, $sp, 8
    jr      $ra
```

---

## 8. Palindrome Check
### C Code
```c
int is_palindrome(char *str, int len) {
    int start = 0;
    int end = len - 1;
    while (start < end) {
        if (str[start] != str[end]) return 0;
        start++;
        end--;
    }
    return 1;
}
```

### MIPS Assembly
```asm
# Arguments: $a0 = str pointer, $a1 = len
is_palindrome:
    li      $t0, 0              # start = 0
    addi    $t1, $a1, -1        # end = len - 1

loop_pal:
    bge     $t0, $t1, is_pal_true # if start >= end, done

    # Get str[start]
    add     $t2, $a0, $t0       # str + start
    lb      $t3, 0($t2)         # load byte

    # Get str[end]
    add     $t4, $a0, $t1       # str + end
    lb      $t5, 0($t4)         # load byte

    bne     $t3, $t5, is_pal_false # if mismatch

    addi    $t0, $t0, 1         # start++
    addi    $t1, $t1, -1        # end--
    j       loop_pal

is_pal_true:
    li      $v0, 1
    jr      $ra

is_pal_false:
    li      $v0, 0
    jr      $ra
```

---

## 9. Switch Loop (Calculator)
### C Code
```c
int calculate(int op, int a, int b) {
    switch(op) {
        case 0: return a + b;
        case 1: return a - b;
        case 2: return a & b;
        case 3: return a | b;
        default: return -1;
    }
}
```

### MIPS Assembly
```asm
# Arguments: $a0 = op, $a1 = a, $a2 = b
calculate:
    # Switch cases
    beq     $a0, 0, case_0
    beq     $a0, 1, case_1
    beq     $a0, 2, case_2
    beq     $a0, 3, case_3
    j       case_default

case_0:
    add     $v0, $a1, $a2
    jr      $ra
case_1:
    sub     $v0, $a1, $a2
    jr      $ra
case_2:
    and     $v0, $a1, $a2
    jr      $ra
case_3:
    or      $v0, $a1, $a2
    jr      $ra
case_default:
    li      $v0, -1
    jr      $ra
```

---

## 10. Sum of Squares (Call Function)
### C Code
```c
int sum_squares(int n) {
    int sum = 0;
    for (int i = 1; i <= n; i++) {
        sum = sum + square(i);
    }
    return sum;
}
int square(int x) { return x * x; }
```

### MIPS Assembly
```asm
# Function: sum_squares
# Arguments: $a0 = n
sum_squares:
    addi    $sp, $sp, -16       # Save registers
    sw      $ra, 12($sp)
    sw      $s0, 8($sp)         # n
    sw      $s1, 4($sp)         # sum
    sw      $s2, 0($sp)         # i

    move    $s0, $a0            # Save n
    li      $s1, 0              # sum = 0
    li      $s2, 1              # i = 1

loop_sq:
    bgt     $s2, $s0, end_sq    # if i > n, exit

    move    $a0, $s2            # Argument for square is i
    jal     square             
    
    add     $s1, $s1, $v0       # sum += result (v0)

    addi    $s2, $s2, 1         # i++
    j       loop_sq

end_sq:
    move    $v0, $s1            # return sum
    lw      $ra, 12($sp)
    lw      $s0, 8($sp)
    lw      $s1, 4($sp)
    lw      $s2, 0($sp)
    addi    $sp, $sp, 16
    jr      $ra

# Function: square
# Arguments: $a0 = x
square:
    mul     $v0, $a0, $a0       # return x * x
    jr      $ra
```
