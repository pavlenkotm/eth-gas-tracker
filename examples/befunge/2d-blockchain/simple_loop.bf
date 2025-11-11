0             v   Push 0 (counter)
>"Block ",,,,,,   Print "Block "
:.            v   Duplicate, print number
55+,          v   Print newline
1+            v   Increment
:3`           v   Duplicate, check if > 3
#v_           <   If true, go left (loop)
@                 End
