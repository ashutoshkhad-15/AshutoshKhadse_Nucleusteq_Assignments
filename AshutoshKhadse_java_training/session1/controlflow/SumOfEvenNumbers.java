// 4) Create a program to calculate the sum of even numbers from 1 to 10 using a while loop.
package AshutoshKhadse_java_training.session1.controlflow;

public class SumOfEvenNumbers {
    
    public static void main(String[] args) {
        int currentNumber = 1;
        int totalSum = 0;
        System.out.println("Even numbers from 1 to " + 10 + ":");

        while (currentNumber <= 10) {
            if (currentNumber % 2 == 0) {
                System.out.print(currentNumber + " ");
                totalSum += currentNumber;
            }
            currentNumber++;
        }
        System.out.println("\n\nSum of even numbers from 1 to "
                           + 10 + " = " + totalSum);
        // Mathematical shortcut we use: n*(n+2)/4 where n=10 → 30
    }
}