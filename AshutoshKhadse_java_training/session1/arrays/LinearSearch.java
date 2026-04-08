// 3) Create a program to search for a specific element within an array using linear search.
package AshutoshKhadse_java_training.session1.arrays;
import java.util.Scanner;

public class LinearSearch {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter number of elements: ");
        int size = scanner.nextInt();
        int[] array = new int[size];

        System.out.println("Enter elements:");
        for (int i = 0; i < size; i++) {
            System.out.print("Element [" + (i + 1) + "]: ");
            array[i] = scanner.nextInt();
        }

        System.out.print("\nEnter element to search: ");
        int target = scanner.nextInt();

        int foundIndex = linearSearch(array, target);

        if (foundIndex != -1) {
            System.out.println("Element " + target + " found at index " + foundIndex);
        } else {
            System.out.println("Element " + target + " not found in the array.");
        }

        scanner.close();
    }

    private static int linearSearch(int[] array, int target) {
        for (int index = 0; index < array.length; index++) {
            if (array[index] == target) {
                return index; // Element found at index
            }
        }
        return -1; // Element not found
    }
}