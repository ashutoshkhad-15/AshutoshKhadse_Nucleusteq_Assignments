// 1) Write a program to calculate the area of a circle, rectangle, or triangle based on user input.
package AshutoshKhadse_java_training.session1.basic;
import java.util.Scanner;

public class AreaCalculator {

    // For PI value
    private static final double PI = Math.PI;

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Select shape: 1.Circle 2.Rectangle 3.Triangle");
        System.out.print("Enter your choice: ");

        int choice = scanner.nextInt();

        switch (choice) {
            case 1:
                System.out.print("Enter radius of circle: ");
                double radius = scanner.nextDouble();
                System.out.printf("Area of Circle = %.2f%n", calculateCircleArea(radius));
                break;

            case 2:
                System.out.print("Enter length of rectangle: ");
                double length = scanner.nextDouble();
                System.out.print("Enter width of rectangle: ");
                double width = scanner.nextDouble();
                System.out.printf("Area of Rectangle = %.2f%n", calculateRectangleArea(length, width));
                break;

            case 3:
                System.out.print("Enter base of triangle: ");
                double base = scanner.nextDouble();
                System.out.print("Enter height of triangle: ");
                double height = scanner.nextDouble();
                System.out.printf("Area of Triangle = %.2f%n", calculateTriangleArea(base, height));
                break;

            default:
                System.out.println("Invalid choice! Please enter 1, 2, or 3.");
        }

        scanner.close();
    }

    private static double calculateCircleArea(double radius) {
        return PI * radius * radius;
    }

    private static double calculateRectangleArea(double length, double width) {
        return length * width;
    }

    private static double calculateTriangleArea(double base, double height) {
        return 0.5 * base * height;
    }
}