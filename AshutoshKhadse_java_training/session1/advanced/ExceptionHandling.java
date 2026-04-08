// 2) Create a program to handle exceptions using try-catch blocks.
package AshutoshKhadse_java_training.session1.advanced;

import java.util.Scanner;

public class ExceptionHandling {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // 1. ArithmeticException (Division by zero)
        System.out.println(" 1. ArithmeticException ");
        try {
            System.out.print("Enter numerator   : ");
            int numerator = scanner.nextInt();
            System.out.print("Enter denominator : ");
            int denominator = scanner.nextInt();

            int result = numerator / denominator; // Throws if denominator = 0
            System.out.println("Result: " + result);

        } catch (ArithmeticException e) {
            System.out.println("Caught an ArithmeticException!");
            System.out.println("Error Details: Cannot divide a number by zero.");
        } finally {
            System.out.println("Finally block 1 executed. \n");
        }

        // 2. NumberFormatException
        System.out.println(" 2. NumberFormatException ");
        String invalidNumber = "abc123";
        try {
            int parsed = Integer.parseInt(invalidNumber);
            System.out.println("Parsed: " + parsed);
        } catch (NumberFormatException e) {
            System.out.println("Error: \"" + invalidNumber + "\" is not a valid number!");
        }

        // 3. ArrayIndexOutOfBoundsException
        System.out.println("\n 3. ArrayIndexOutOfBoundsException ");
        int[] numbers = { 10, 20, 30 };
        try {
            System.out.println("Accessing index 5: " + numbers[5]); // Only 0,1,2 exist!
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.println("Caught an ArrayIndexOutOfBoundsException!");
            System.out.println("Error Details: You tried to access an index that doesn't exist in the array.");
        } finally {
            System.out.println("Finally block 2 executed.\n");
        }

        System.out.println("\n 4. Scenario: Multiple Catch Blocks");
        try {
            String text = null;
            // Attempting to call a method on a null object
            int length = text.length();
            System.out.println("String length is: " + length);
        } catch (ArithmeticException e) {
            System.out.println("Caught ArithmeticException.");
        } catch (NullPointerException e) {
            System.out.println("Caught a NullPointerException!");
            System.out.println("Error Details: Attempted to perform an operation on a null object reference.");
        } catch (Exception e) {
            // This is a generic catch block. It acts as a fallback for any other unexpected
            // exceptions.
            // It should always be placed last.
            System.out.println("Caught a generic Exception: " + e.getMessage());
        } finally {
            System.out.println("Finally block 4 executed.\n");
        }
        scanner.close();
        System.out.println("\nProgram ended gracefully!");
    }

}
