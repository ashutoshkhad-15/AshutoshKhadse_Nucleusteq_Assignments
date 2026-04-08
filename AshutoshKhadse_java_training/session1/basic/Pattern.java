// 5) Use loops to print patterns like a triangle or square.
package AshutoshKhadse_java_training.session1.basic;
import java.util.Scanner;

public class Pattern {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Pattern to Choose from:");
        System.out.println("1. Right-angled Triangle ");
        System.out.println("2. Solid Square ");
        System.out.println("3. Inverted Triangle");
        System.out.println("4. Pyramid");
        System.out.print("Choose pattern: ");
        int choice = scanner.nextInt();

        System.out.print("Enter number of rows: ");
        int rows = scanner.nextInt();

        switch (choice) {
            case 1: RightAngledTriangle(rows); break;
            case 2: SolidSquare(rows);         break;
            case 3: InvertedTriangle(rows);    break;
            case 4: Pyramid(rows);             break;
            default: System.out.println("Invalid choice!");
        }

        scanner.close();
    }

    // Pattern 1: Right-angled Triangle
    private static void RightAngledTriangle(int rows) {
        System.out.println("\n Right-Angled Triangle ");
        for (int row = 1; row <= rows; row++) {
            for (int col = 1; col <= row; col++) {
                System.out.print("* ");
            }
            System.out.println();
        }
    }

    // Pattern 2: Solid Square
    private static void SolidSquare(int rows) {
        System.out.println("\n Solid Square ");
        for (int row = 1; row <= rows; row++) {
            for (int col = 1; col <= rows; col++) {
                System.out.print("* ");
            }
            System.out.println();
        }
    }

    // Pattern 3: Inverted Triangle
    private static void InvertedTriangle(int rows) {
        System.out.println("\n Inverted Triangle ");
        for (int row = rows; row >= 1; row--) {
            for (int col = 1; col <= row; col++) {
                System.out.print("* ");
            }
            System.out.println();
        }
    }

    // Pattern 4: Pyramid (centered)
    private static void Pyramid(int rows) {
        System.out.println("\n Pyramid ");
        for (int row = 1; row <= rows; row++) {
            // Print leading spaces
            for (int space = 1; space <= rows - row; space++) {
                System.out.print(" ");
            }
            // Print stars (odd numbers: 1, 3, 5, 7...)
            for (int star = 1; star <= (2 * row - 1); star++) {
                System.out.print("*");
            }
            System.out.println();
        }
    }
}
