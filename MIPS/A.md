```
void recursiveCopy(char dest[], char src[], int i, int j) {
    if (src[i] == '\0') {
        dest[j] = '\0';
        return;
    }
    recursiveCopy(dest, src, i + 1, j - 1);
    dest[j] = src[i]; 
}
```


        .text
        .globl recursiveCopy

recursiveCopy:
        # Stack frame
        addi $sp, $sp, -20
        sw   $ra, 16($sp)
        sw   $a0, 12($sp)
        sw   $a1, 8($sp)
        sw   $a2, 4($sp)    # save i
        sw   $a3, 0($sp)    # save j

        # if (src[i] == '\0')
        add  $t0, $a1, $a2  # &src[i]
        lb   $t1, 0($t0)    # src[i]

        beq  $t1, $zero, base_case

        # recursiveCopy(dest, src, i+1, j-1)
        addi $a2, $a2, 1    # i + 1
        addi $a3, $a3, -1   # j - 1
        jal  recursiveCopy

        # restore registers after return
        lw   $a0, 12($sp)
        lw   $a1, 8($sp)
        lw   $a2, 4($sp)    # restore i
        lw   $a3, 0($sp)    # restore j

        # dest[j] = src[i]
        add  $t2, $a1, $a2  # &src[i]
        lb   $t3, 0($t2)

        add  $t4, $a0, $a3  # &dest[j]
        sb   $t3, 0($t4)

        j    end_function

base_case:
        # dest[j] = '\0'
        add  $t4, $a0, $a3
        sb   $zero, 0($t4)

end_function:
        lw   $ra, 16($sp)
        addi $sp, $sp, 20
        jr   $ra
