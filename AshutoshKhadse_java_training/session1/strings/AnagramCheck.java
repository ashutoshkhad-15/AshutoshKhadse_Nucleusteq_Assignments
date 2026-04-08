// 3) Create a program to check if two strings are anagrams.
package AshutoshKhadse_java_training.session1.strings;

import java.util.Arrays;
import java.util.Scanner;

public class AnagramCheck {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter first string  : ");
        String firstString = scanner.nextLine();

        System.out.print("Enter second string : ");
        String secondString = scanner.nextLine();

        if (areAnagrams(firstString, secondString)) {
            System.out.println("\"" + firstString + "\" and \"" + secondString
                    + "\" ARE anagrams!");
        } else {
            System.out.println("\"" + firstString + "\" and \"" + secondString
                    + "\" are NOT anagrams.");
        }

        scanner.close();
    }

    /*
       Approach:
            1. convert to lowercase and remove spaces 
            2. sort both strings
            3. if sorted versions are equal means they're anagrams
     */
    private static boolean areAnagrams(String first, String second) {
        
        String normalizedFirst = first.replaceAll("\\s+", "").toLowerCase();
        String normalizedSecond = second.replaceAll("\\s+", "").toLowerCase();

        // checking length if equal are not
        if (normalizedFirst.length() != normalizedSecond.length()) {
            return false;
        }

        // Sorting both and compare
        char[] firstSorted = normalizedFirst.toCharArray();
        char[] secondSorted = normalizedSecond.toCharArray();

        Arrays.sort(firstSorted);
        Arrays.sort(secondSorted);

        return Arrays.equals(firstSorted, secondSorted);
    }
}