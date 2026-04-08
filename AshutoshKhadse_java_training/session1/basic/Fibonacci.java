// 4) Write a program to print the Fibonacci sequence up to a specified number.
package AshutoshKhadse_java_training.session1.basic;
import java.util.Scanner;

public class Fibonacci {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("How many Fibonacci terms do you want to print? ");
        int count = scanner.nextInt();

        if (count <= 0) {
            System.out.println("Please enter a positive number.");
        } else {
            System.out.println("Fibonacci Sequence:");
            printFibonacci(count);
        }

        scanner.close();
    }

    private static void printFibonacci(int count) {
        long firstTerm = 0;
        long secondTerm = 1;

        for (int i = 1; i <= count; i++) {
            System.out.print(firstTerm);

            if (i < count) {
                System.out.print(", ");
            }

            long nextTerm = firstTerm + secondTerm;
            firstTerm = secondTerm;
            secondTerm = nextTerm;
        }

        System.out.println();
    }
}