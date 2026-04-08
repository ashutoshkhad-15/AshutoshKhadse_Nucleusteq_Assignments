// 3) Use a for loop to print a multiplication table.
package AshutoshKhadse_java_training.session1.controlflow;
import java.util.Scanner;

public class MultiplicationTable {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter the number for multiplication table: ");
        int number = scanner.nextInt();

        System.out.println("\n Multiplication Table of " + number + ":");

        for (int multiplier = 1; multiplier <= 10; multiplier++) {
            System.out.printf("%d x %2d = %3d%n", number, multiplier, number * multiplier);
        }

        scanner.close();
    }
}