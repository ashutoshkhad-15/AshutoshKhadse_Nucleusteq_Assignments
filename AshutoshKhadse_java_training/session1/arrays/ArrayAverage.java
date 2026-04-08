// 1) Write a program to find the average of elements in an array.
package AshutoshKhadse_java_training.session1.arrays;
import java.util.Scanner;

public class ArrayAverage {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter number of elements in the array: ");
        int size = scanner.nextInt();
        
        int[] numbers = new int[size];

        System.out.println("Enter the elements:");
        for (int i = 0; i < size; i++) {
            System.out.print("Element [" + (i + 1) + "]: ");
            numbers[i] = scanner.nextInt();
        }

        float average = calculateAverage(numbers);
        System.out.printf("\nArray Average = %.2f%n", average);
        scanner.close();
    }

    private static float calculateAverage(int[] numbers) {
        int sum = 0;
        for (int num : numbers) {
            sum += num;
        }
        return (float) sum / numbers.length;
    }
}
