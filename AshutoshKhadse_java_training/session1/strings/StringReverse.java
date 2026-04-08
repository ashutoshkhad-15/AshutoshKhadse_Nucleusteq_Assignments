// 1) Write a program to reverse a given string.
package AshutoshKhadse_java_training.session1.strings;
import java.util.Scanner;

public class StringReverse {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter a string to reverse: ");
        String input = scanner.nextLine();

        System.out.println("Original String  : " + input);
        System.out.println("Reversed (Manual): " + reverseManually(input));
        System.out.println("Reversed (Builder): " + reverseUsingBuilder(input));

        scanner.close();
    }

    // Manual approach: build reversed string character by character
    private static String reverseManually(String text) {
        String reversed = "";
        for (int i = text.length() - 1; i >= 0; i--) {
            reversed += text.charAt(i);
        }
        return reversed;
    }

    // Using StringBuilder is more efficient for reversing strings as it uses less memory 
    private static String reverseUsingBuilder(String text) {
        return new StringBuilder(text).reverse().toString();
    }
}
