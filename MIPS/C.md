int main(){
    int x = 3, y = 2; // x = $s0, y = $s1
    int limit = 50; // limit = $s2
    
    do{
        if((x &1) == 0){
            x += y;
            y += x;
        }else if((y | 1) > y){
            y += x;
            x += y;
        }else{
            x += 1
            y += 1
        }
        
    }while(x + y < limit);
    
    return 0;
}


solution=>

main:
        # initialize variables
        li   $s0, 3        # x = 3
        li   $s1, 2        # y = 2
        li   $s2, 50       # limit = 50

do_loop:
        # if ((x & 1) == 0)
        andi $t0, $s0, 1   # t0 = x & 1
        beq  $t0, $zero, if_even

        # else if ((y | 1) > y)
        ori  $t1, $s1, 1   # t1 = y | 1
        ble  $t1, $s1, else_block

        # y += x
        add  $s1, $s1, $s0
        # x += y
        add  $s0, $s0, $s1
        j    end_if

if_even:
        # x += y
        add  $s0, $s0, $s1
        # y += x
        add  $s1, $s1, $s0
        j    end_if

else_block:
        addi $s0, $s0, 1   # x += 1
        addi $s1, $s1, 1   # y += 1

end_if:
        # while (x + y < limit)
        add  $t2, $s0, $s1
        blt  $t2, $s2, do_loop

        # return 0
        li   $v0, 10
        syscall
