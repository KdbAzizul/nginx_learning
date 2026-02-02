# Advanced C to MIPS Conversion Practice

This document contains 10 complex problems with their corresponding C code and MIPS assembly solutions. These problems involve advanced concepts like 2D arrays, recursion, struct pointers, and nested loops sequences.

---

## 1. Matrix Multiplication (3x3)
**Concept:** 2D Array flattening `Addr = Base + (row * num_cols + col) * 4`, Nested Loops.

### C Code
```c
void mat_mul(int n, int A[], int B[], int C[]) {
    // A, B, C are n x n matrices stored in 1D arrays
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            int sum = 0;
            for (int k = 0; k < n; k++) {
                // A[i][k] * B[k][j]
                int a_val = A[i * n + k];
                int b_val = B[k * n + j];
                sum += a_val * b_val;
            }
            C[i * n + j] = sum;
        }
    }
}
```

### MIPS Solution
```asm
# Arguments: $a0 = n, $a1 = base_A, $a2 = base_B, $a3 = base_C
mat_mul:
    addi    $sp, $sp, -44       # Save registers
    sw      $ra, 40($sp)
    sw      $s0, 36($sp)        # i
    sw      $s1, 32($sp)        # j
    sw      $s2, 28($sp)        # k
    sw      $s3, 24($sp)        # n
    sw      $s4, 20($sp)        # base_A
    sw      $s5, 16($sp)        # base_B
    sw      $s6, 12($sp)        # base_C
    sw      $s7, 8($sp)         # sum

    move    $s3, $a0
    move    $s4, $a1
    move    $s5, $a2
    move    $s6, $a3

    li      $s0, 0              # i = 0
loop_i:
    bge     $s0, $s3, end_i     # if i >= n, exit

    li      $s1, 0              # j = 0
loop_j:
    bge     $s1, $s3, end_j     # if j >= n, next i

    li      $s7, 0              # sum = 0
    li      $s2, 0              # k = 0
loop_k:
    bge     $s2, $s3, end_k     # if k >= n, write to C

    # Calculate address of A[i][k] -> A + (i*n + k)*4
    mul     $t0, $s0, $s3       # i * n
    add     $t0, $t0, $s2       # + k
    sll     $t0, $t0, 2         # * 4
    add     $t0, $s4, $t0       # Base A + offset
    lw      $t1, 0($t0)         # Load A[i][k]

    # Calculate address of B[k][j] -> B + (k*n + j)*4
    mul     $t2, $s2, $s3       # k * n
    add     $t2, $t2, $s1       # + j
    sll     $t2, $t2, 2         # * 4
    add     $t2, $s5, $t2       # Base B + offset
    lw      $t3, 0($t2)         # Load B[k][j]

    mul     $t4, $t1, $t3       # A * B
    add     $s7, $s7, $t4       # sum += ...

    addi    $s2, $s2, 1         # k++
    j       loop_k

end_k:
    # Store C[i][j] -> C + (i*n + j)*4
    mul     $t0, $s0, $s3       # i * n
    add     $t0, $t0, $s1       # + j
    sll     $t0, $t0, 2         # * 4
    add     $t0, $s6, $t0       # Base C + offset
    sw      $s7, 0($t0)         # C[i][j] = sum

    addi    $s1, $s1, 1         # j++
    j       loop_j

end_j:
    addi    $s0, $s0, 1         # i++
    j       loop_i

end_i:
    lw      $ra, 40($sp)
    lw      $s0, 36($sp)
    lw      $s1, 32($sp)
    lw      $s2, 28($sp)
    lw      $s3, 24($sp)
    lw      $s4, 20($sp)
    lw      $s5, 16($sp)
    lw      $s6, 12($sp)
    lw      $s7, 8($sp)
    addi    $sp, $sp, 44
    jr      $ra
```

---

## 2. Recursive Binary Search
**Concept:** Recursion, Array Indexing, Halving.

### C Code
```c
int binary_search(int arr[], int l, int r, int x) {
    if (r >= l) {
        int mid = l + (r - l) / 2;
        if (arr[mid] == x) return mid;
        if (arr[mid] > x) 
            return binary_search(arr, l, mid - 1, x);
        return binary_search(arr, mid + 1, r, x);
    }
    return -1;
}
```

### MIPS Solution
```asm
# Arguments: $a0 = arr, $a1 = l, $a2 = r, $a3 = x
binary_search:
    addi    $sp, $sp, -4        # Save RA
    sw      $ra, 0($sp)

    blt     $a2, $a1, not_found # if r < l, return -1

    # mid = l + (r - l) / 2
    sub     $t0, $a2, $a1       # r - l
    srl     $t0, $t0, 1         # / 2
    add     $t0, $a1, $t0       # mid = l + ...

    # Load arr[mid]
    sll     $t1, $t0, 2         # mid * 4
    add     $t1, $a0, $t1       # arr + offset
    lw      $t2, 0($t1)         # t2 = arr[mid]

    beq     $t2, $a3, return_mid # if arr[mid] == x

    # if arr[mid] > x -> search left: (arr, l, mid-1, x)
    bgt     $t2, $a3, search_left

    # Else search right: (arr, mid+1, r, x)
    addi    $a1, $t0, 1         # l = mid + 1
    # $a0 (arr), $a2 (r), $a3 (x) remain same
    jal     binary_search
    j       end_search

search_left:
    addi    $a2, $t0, -1        # r = mid - 1
    # $a0 (arr), $a1 (l), $a3 (x) remain same
    jal     binary_search
    j       end_search

return_mid:
    move    $v0, $t0            # return mid
    j       end_search

not_found:
    li      $v0, -1

end_search:
    lw      $ra, 0($sp)
    addi    $sp, $sp, 4
    jr      $ra
```

---

## 3. Linked List Traversal (Sum)
**Concept:** Structs, Pointer Chasing (`ptr->next`).
Assumes `struct Node { int data; Node* next; }`.

### C Code
```c
int sum_list(struct Node* head) {
    int sum = 0;
    while (head != NULL) {
        sum += head->data;
        head = head->next;
    }
    return sum;
}
```

### MIPS Solution
```asm
# Arguments: $a0 = head pointer
sum_list:
    li      $v0, 0              # sum = 0
loop_list:
    beq     $a0, $zero, end_list # if head == NULL return

    lw      $t0, 0($a0)         # load data (offset 0)
    add     $v0, $v0, $t0       # sum += data

    lw      $a0, 4($a0)         # head = head->next (offset 4)
    j       loop_list

end_list:
    jr      $ra
```

---

## 4. String to Integer (atoi)
**Concept:** Byte processing, arithmetic accumulation, ASCII conversion.

### C Code
```c
int my_atoi(char *str) {
    int res = 0;
    int sign = 1;
    int i = 0;

    if (str[0] == '-') {
        sign = -1;
        i++;
    }

    while (str[i] != '\0') {
        int digit = str[i] - '0';
        res = res * 10 + digit;
        i++;
    }
    return sign * res;
}
```

### MIPS Solution
```asm
# Argument: $a0 = str pointer
my_atoi:
    li      $v0, 0              # res = 0
    li      $t0, 1              # sign = 1
    move    $t1, $a0            # current char ptr

    lb      $t2, 0($t1)         # load first char
    li      $t3, 45             # ASCII for '-'
    bne     $t2, $t3, loop_atoi

    # Handle negative
    li      $t0, -1             # sign = -1
    addi    $t1, $t1, 1         # i++

loop_atoi:
    lb      $t2, 0($t1)         # load char
    beq     $t2, $zero, end_atoi # if null terminator, exit

    sub     $t2, $t2, 48        # char - '0'
    mul     $v0, $v0, 10        # res * 10
    add     $v0, $v0, $t2       # res + digit

    addi    $t1, $t1, 1         # i++
    j       loop_atoi

end_atoi:
    mul     $v0, $v0, $t0       # apply sign
    jr      $ra
```

---

## 5. Merge Two Sorted Arrays
**Concept:** Multiple array pointers, conditional logic.

### C Code
```c
void merge(int A[], int n, int B[], int m, int C[]) {
    int i = 0, j = 0, k = 0;
    while (i < n && j < m) {
        if (A[i] < B[j]) {
            C[k++] = A[i++];
        } else {
            C[k++] = B[j++];
        }
    }
    while (i < n) C[k++] = A[i++];
    while (j < m) C[k++] = B[j++];
}
```

### MIPS Solution
```asm
# Args: $a0=A, $a1=n, $a2=B, $a3=m, 16($sp)=C (5th arg on stack)
merge_arrays:
    lw      $t9, 0($sp)         # Load C base address from stack (5th arg logic usually matches calling convention)
                                # NOTE: Assuming standard convention, args 5+ are on stack. 
                                # Let's assume passed in temporary register for simplicity or standard stack.
                                # For this example, let's assume $t9 holds C.

    li      $t0, 0              # i = 0
    li      $t1, 0              # j = 0
    li      $t2, 0              # k = 0

merge_loop:
    # Check i < n && j < m
    bge     $t0, $a1, flush_a   # if i >= n, done with loop
    bge     $t1, $a3, flush_a   # if j >= m, done with loop (logic actually splits here)
    
    # Needs checking both conditions. If either fails, exit main loop.
    # Actually logic: while(i<n && j<m). Exit if i>=n OR j>=m.

    # Load A[i]
    sll     $t3, $t0, 2
    add     $t3, $a0, $t3
    lw      $t4, 0($t3)         # A[i]

    # Load B[j]
    sll     $t5, $t1, 2
    add     $t5, $a2, $t5
    lw      $t6, 0($t5)         # B[j]

    # Compare
    bge     $t4, $t6, take_b

take_a:
    # C[k] = A[i]
    sll     $t7, $t2, 2
    add     $t7, $t9, $t7
    sw      $t4, 0($t7)
    addi    $t2, $t2, 1         # k++
    addi    $t0, $t0, 1         # i++
    j       merge_loop

take_b:
    # C[k] = B[j]
    sll     $t7, $t2, 2
    add     $t7, $t9, $t7
    sw      $t6, 0($t7)
    addi    $t2, $t2, 1         # k++
    addi    $t1, $t1, 1         # j++
    j       merge_loop

flush_a:
    bge     $t0, $a1, flush_b
    # Store A[i] -> C[k] ... (similar to take_a)
    sll     $t3, $t0, 2
    add     $t3, $a0, $t3
    lw      $t4, 0($t3)
    sll     $t7, $t2, 2
    add     $t7, $t9, $t7
    sw      $t4, 0($t7)
    addi    $t0, $t0, 1
    addi    $t2, $t2, 1
    j       flush_a

flush_b:
    bge     $t1, $a3, done_merge
    # Store B[j] -> C[k]
    sll     $t5, $t1, 2
    add     $t5, $a2, $t5
    lw      $t6, 0($t5)
    sll     $t7, $t2, 2
    add     $t7, $t9, $t7
    sw      $t6, 0($t7)
    addi    $t1, $t1, 1
    addi    $t2, $t2, 1
    j       flush_b

done_merge:
    jr      $ra
```

---

## 6. Count Set Bits (Kernighan's Algorithm)
**Concept:** Bitwise AND, Loop.

### C Code
```c
int count_set_bits(int n) {
    int count = 0;
    while (n > 0) {
        n = n & (n - 1);
        count++;
    }
    return count;
}
```

### MIPS Solution
```asm
count_bits:
    li      $v0, 0          # count = 0
    move    $t0, $a0        # t0 = n

loop_cnt:
    blez    $t0, end_cnt    # while (n > 0)

    addi    $t1, $t0, -1    # t1 = n - 1
    and     $t0, $t0, $t1   # n = n & (n-1)
    addi    $v0, $v0, 1     # count++
    j       loop_cnt

end_cnt:
    jr      $ra
```

---

## 7. Tower of Hanoi (Recursive)
**Concept:** Double Recursion, Stack arguments.
`void hanoi(int n, char from, char to, char aux)`

### C Code
```c
void hanoi(int n, int from, int to, int aux) {
    if (n == 1) {
        print_move(from, to);
        return;
    }
    hanoi(n - 1, from, aux, to);
    print_move(from, to);
    hanoi(n - 1, aux, to, from);
}
```

### MIPS Solution
```asm
# $a0=n, $a1=from, $a2=to, $a3=aux
hanoi:
    addi    $sp, $sp, -20
    sw      $ra, 16($sp)
    sw      $s0, 12($sp) # n
    sw      $s1, 8($sp)  # from
    sw      $s2, 4($sp)  # to
    sw      $s3, 0($sp)  # aux

    move    $s0, $a0
    move    $s1, $a1
    move    $s2, $a2
    move    $s3, $a3

    li      $t0, 1
    beq     $s0, $t0, base_case

    # Recursive Step 1: hanoi(n-1, from, aux, to)
    addi    $a0, $s0, -1
    move    $a1, $s1
    move    $a2, $s3  # to = aux
    move    $a3, $s2  # aux = to
    jal     hanoi

    # Move current disk (simulate print)
    # We could call a function here or just continues
    # print_move(s1, s2)

    # Recursive Step 2: hanoi(n-1, aux, to, from)
    addi    $a0, $s0, -1
    move    $a1, $s3  # from = aux
    move    $a2, $s2  # to = to
    move    $a3, $s1  # aux = from
    jal     hanoi

    j       end_hanoi

base_case:
    # print_move(s1, s2) - Base case action
    nop

end_hanoi:
    lw      $ra, 16($sp)
    lw      $s0, 12($sp)
    lw      $s1, 8($sp)
    lw      $s2, 4($sp)
    lw      $s3, 0($sp)
    addi    $sp, $sp, 20
    jr      $ra
```

---

## 8. Swapping using Pointers (Function Call)
**Concept:** Memory operations via pointers.

### C Code
```c
void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}
```

### MIPS Solution
```asm
# $a0 = address of a, $a1 = address of b
swap:
    lw      $t0, 0($a0)     # t0 = *a
    lw      $t1, 0($a1)     # t1 = *b
    
    sw      $t1, 0($a0)     # *a = t1
    sw      $t0, 0($a1)     # *b = t0
    
    jr      $ra
```

---

## 9. Palindrome Check with Pointers
**Concept:** Two pointers moving towards each other.

### C Code
```c
int is_palindrome(char *start, char *end) {
    while (start < end) {
        if (*start != *end) return 0;
        start++;
        end--;
    }
    return 1;
}
```

### MIPS Solution
```asm
# $a0 = start ptr, $a1 = end ptr
is_palindrome_ptr:
loop_pal:
    bge     $a0, $a1, is_true   # if start >= end, pointers met

    lb      $t0, 0($a0)         # *start
    lb      $t1, 0($a1)         # *end
    bne     $t0, $t1, is_false  # if mismatch

    addi    $a0, $a0, 1         # start++
    addi    $a1, $a1, -1        # end--
    j       loop_pal

is_true:
    li      $v0, 1
    jr      $ra

is_false:
    li      $v0, 0
    jr      $ra
```

---

## 10. Sparse Array Multiplication (Indirect access)
**Concept:** `A[B[i]]` - Address calculation dependent on loaded value.

### C Code
```c
// Calculate sum of A[index_arr[i]] for i from 0 to n
int sparse_sum(int A[], int index_arr[], int n) {
    int sum = 0;
    for (int i = 0; i < n; i++) {
        int idx = index_arr[i];
        sum += A[idx];
    }
    return sum;
}
```

### MIPS Solution
```asm
# $a0 = A base, $a1 = index_arr base, $a2 = n
sparse_sum:
    li      $v0, 0              # sum = 0
    li      $t0, 0              # i = 0

loop_sparse:
    bge     $t0, $a2, end_sparse

    # Get index_arr[i]
    sll     $t1, $t0, 2         # i * 4
    add     $t1, $a1, $t1       # index_arr + offset
    lw      $t2, 0($t1)         # idx = index_arr[i]

    # Get A[idx]
    sll     $t3, $t2, 2         # idx * 4
    add     $t3, $a0, $t3       # A + offset_idx
    lw      $t4, 0($t3)         # val = A[idx]

    add     $v0, $v0, $t4       # sum += val

    addi    $t0, $t0, 1         # i++
    j       loop_sparse

end_sparse:
    jr      $ra
```
