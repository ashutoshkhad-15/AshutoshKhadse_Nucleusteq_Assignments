// 1) Write a program to check if a given number is prime using an if-else statement.
package AshutoshKhadse_java_training.session1.controlflow;
import java.util.Scanner;

public class PrimeNumbers {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter a number to check: ");
        int number = scanner.nextInt();

        if (isPrime(number)) {
            System.out.println(number + " is a PRIME number.");
        } else {
            System.out.println(number + " is NOT a prime number.");
        }
        scanner.close();
    }

    private static boolean isPrime(int number) {
        if (number <= 1) return false;   // 0, 1 and negatives are not prime
        if (number == 2) return true;    // 2 is the only even prime
        if (number % 2 == 0) return false; // All other even numbers are not prime

        /*  
        Check odd divisors from 3 up to the square root of the number 
        because if a number is divisible by any number greater than its square root,
        it must have a corresponding divisor that is smaller than the square root.
        */
        for (int divisor = 3; divisor <= Math.sqrt(number); divisor += 2) {
            if (number % divisor == 0) {
                return false; 
            }
        }
        return true;
    }
}
