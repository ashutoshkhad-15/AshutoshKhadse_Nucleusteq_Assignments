// 3) Demonstrate polymorphism by creating methods with the same name but different parameters in a parent and child class.
package AshutoshKhadse_java_training.session1.oop;

// Parent Class
class Calculator {

    public void calculate(int a, int b) {
        System.out.println("Addition: " + (a + b));
    }
}

// Child Class
class AdvancedCalculator extends Calculator {
    // Overloading parent method with different parameters
    public void calculate(int a, int b, int c) {
        System.out.println("Addition of three numbers: " + (a + b + c));
    }
}

// Main Class
public class Polymorphism {

    public static void main(String[] args) {
        AdvancedCalculator calc = new AdvancedCalculator();
        calc.calculate(5, 10); // Parent method
        calc.calculate(5, 10, 15); // Child method (overloaded)
    }
}