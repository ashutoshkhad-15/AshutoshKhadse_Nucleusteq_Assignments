// 2) Implement a function to count the number of vowels in a string. 
package AshutoshKhadse_java_training.session1.strings;
import java.util.Scanner;

public class VowelCount {

    private static final String VOWELS = "aeiouAEIOU";

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter a string: ");
        String input = scanner.nextLine();

        int vowelCount = countVowels(input);
        System.out.println("Input     : \"" + input + "\"");
        System.out.println("Vowels    : " + vowelCount);
        System.out.println("Consonants: " + countConsonants(input));

        scanner.close();
    }

    private static int countVowels(String text) {
        int count = 0;
        for (char character : text.toCharArray()) {
            if (VOWELS.indexOf(character) != -1) {
                count++;
            }
        }
        return count;
    }

    private static int countConsonants(String text) {
        int count = 0;
        for (char character : text.toCharArray()) {
            if (Character.isLetter(character) && VOWELS.indexOf(character) == -1) {
                count++;
            }
        }
        return count;
    }
}
