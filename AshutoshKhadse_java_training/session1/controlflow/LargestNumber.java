// 2) Implement a program to find the largest number among three given numbers using a conditional statement.
package AshutoshKhadse_java_training.session1.controlflow;
import java.util.Scanner;

public class LargestNumber {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter first number  : ");
        int first = scanner.nextInt();

        System.out.print("Enter second number : ");
        int second = scanner.nextInt();

        System.out.print("Enter third number  : ");
        int third = scanner.nextInt();

        int largest = findLargestNumber(first, second, third);
        System.out.println("Largest number is: " + largest);

        scanner.close();
    }

    private static int findLargestNumber(int a, int b, int c) {
        if (a >= b && a >= c) {
            return a;
        } else if (b >= a && b >= c) {
            return b;
        } else {
            return c;
        }
        // Alternative inbuilt approach: return Math.max(a, Math.max(b, c));
    }
}
