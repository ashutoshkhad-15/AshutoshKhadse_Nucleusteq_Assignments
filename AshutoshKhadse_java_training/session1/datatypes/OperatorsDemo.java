// 2) Write a program to demonstrate the use of arithmetic, logical, and relational operators.
package AshutoshKhadse_java_training.session1.datatypes;

public class OperatorsDemo {

    public static void main(String[] args) {
        int a = 15, b = 4;

        // ARITHMETIC OPERATORS
        System.out.println(" ARITHMETIC OPERATORS ");
        System.out.println("a = " + a + ", b = " + b);
        System.out.println("Addition       (a + b)  = " + (a + b));   
        System.out.println("Subtraction    (a - b)  = " + (a - b));   
        System.out.println("Multiplication (a * b)  = " + (a * b));   
        System.out.println("Division       (a / b)  = " + (a / b));   
        System.out.println("Modulo         (a % b)  = " + (a % b));   // remainder

        // Increment / Decrement
        int counter = 10;
        System.out.println("\nPre-increment  (++counter) = " + (++counter)); // 11
        System.out.println("Post-increment (counter++) = " + (counter++)); // 11, then becomes 12
        System.out.println("After post-increment, counter = " + counter);   // 12
        System.out.println("Pre-decrement  (--counter) = " + (--counter)); // 11

        
        // RELATIONAL (Comparison) OPERATORS
        System.out.println("\n RELATIONAL OPERATORS ");
        System.out.println("a = " + a + ", b = " + b);
        System.out.println("a == b  : " + (a == b));   // false
        System.out.println("a != b  : " + (a != b));   // true
        System.out.println("a >  b  : " + (a > b));    // true
        System.out.println("a <  b  : " + (a < b));    // false
        System.out.println("a >= b  : " + (a >= b));   // true
        System.out.println("a <= b  : " + (a <= b));   // false

            
        // LOGICAL OPERATORS
        System.out.println("\n LOGICAL OPERATORS ");
        boolean isAdult    = true;
        boolean hasTicket  = false;

        System.out.println("isAdult    = " + isAdult);
        System.out.println("hasTicket  = " + hasTicket);
        System.out.println("AND (&&) : " + (isAdult && hasTicket)); // false - both must be true
        System.out.println("OR  (||) : " + (isAdult || hasTicket)); // true  - at least one true
        System.out.println("NOT (!)  : " + (!isAdult));             // false - flips the value

        // Compound logical example
        int age  = 20;
        int marks = 85;
        boolean isEligibleForScholarship = (age < 25) && (marks >= 80);
        System.out.println("\nIs eligible for scholarship (age<25 AND marks>=80): "
                           + isEligibleForScholarship); // true
    }
}