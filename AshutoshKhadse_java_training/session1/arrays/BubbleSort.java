// 2) Implement a function to sort an array in ascending order using bubble sort or selection sort.
package AshutoshKhadse_java_training.session1.arrays;
import java.util.Arrays;
import java.util.Scanner;

// Using BubbleSort to sort an array in ascending order
public class BubbleSort {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter number of elements: ");
        int size = scanner.nextInt();
        int[] numbers = new int[size];

        System.out.println("Enter elements:");
        for (int i = 0; i < size; i++) {
            System.out.print("Element [" + (i + 1) + "]: ");
            numbers[i] = scanner.nextInt();
        }

        System.out.println("\nOriginal Array : " + Arrays.toString(numbers));

        // Sort using Bubble Sort
        int[] bubbleSorted = numbers.clone();
        bubbleSort(bubbleSorted);
        System.out.println("Bubble Sorted  : " + Arrays.toString(bubbleSorted));

        scanner.close();
    }

    private static void bubbleSort(int[] array) {
        int length = array.length;

        for (int pass = 0; pass < length - 1; pass++) {
            boolean swapHappened = false;

            for (int index = 0; index < length - pass - 1; index++) {
                if (array[index] > array[index + 1]) {
                    // Swap adjacent elements
                    int temp = array[index];
                    array[index] = array[index + 1];
                    array[index + 1] = temp;
                    swapHappened = true;
                }
            }
            // If no swaps happened in a pass, array is already sorted
            if (!swapHappened) break;
        }
    }
}
