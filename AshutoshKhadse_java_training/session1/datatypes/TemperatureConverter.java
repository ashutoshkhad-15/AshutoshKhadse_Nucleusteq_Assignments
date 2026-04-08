// 3) Create a program to convert a temperature from Celsius to Fahrenheit and vice versa.
package AshutoshKhadse_java_training.session1.datatypes;
import java.util.Scanner;

public class TemperatureConverter {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println(" Temperature Converter ");
        System.out.println("1. Celsius    -> Fahrenheit");
        System.out.println("2. Fahrenheit -> Celsius");
        System.out.print("Choose conversion type: ");
        int choice = scanner.nextInt();

        switch (choice) {
            case 1:
                System.out.print("Enter temperature in Celsius: ");
                double celsius = scanner.nextDouble();
                double fahrenheit = celsiusToFahrenheit(celsius);
                System.out.printf("%.2f°C = %.2f°F%n", celsius, fahrenheit);
                break;

            case 2:
                System.out.print("Enter temperature in Fahrenheit: ");
                double fahrenheitInput = scanner.nextDouble();
                double celsiusResult = fahrenheitToCelsius(fahrenheitInput);
                System.out.printf("%.2f°F = %.2f°C%n", fahrenheitInput, celsiusResult);
                break;

            default:
                System.out.println("Invalid choice!");
        }

        scanner.close();
    }

    private static double celsiusToFahrenheit(double celsius) {
        return (celsius * 9.0 / 5.0) + 32;
    }

    private static double fahrenheitToCelsius(double fahrenheit) {
        return (fahrenheit - 32) * 5.0 / 9.0;
    }
}