// 4) Explore multithreading in Java to perform multiple tasks concurrently.
package AshutoshKhadse_java_training.session1.advanced;

// Two ways to create threads:
// 1. Extending the Thread class
// 2. Implementing the Runnable interface

// Approach 1: Extending Thread class
class NumberPrinter extends Thread {

    private String threadName;
    private int start;
    private int end;

    public NumberPrinter(String threadName, int start, int end) {
        this.threadName = threadName;
        this.start = start;
        this.end = end;
    }

    @Override
    public void run() {
        System.out.println("[" + threadName + "] Started.");
        for (int i = start; i <= end; i++) {
            System.out.println("[" + threadName + "] -> " + i);
            try {
                Thread.sleep(100); // Pause 100ms to show interleaving
            } catch (InterruptedException e) {
                System.out.println("[" + threadName + "] Interrupted!");
            }
        }
        System.out.println("[" + threadName + "] Finished.");
    }
}

// Approach 2: Implementing Runnable interface
class LetterPrinter implements Runnable {

    private String letters;

    public LetterPrinter(String letters) {
        this.letters = letters;
    }

    @Override
    public void run() {
        System.out.println("[LetterPrinter] Started.");
        for (char letter : letters.toCharArray()) {
            System.out.println("[LetterPrinter] -> " + letter);
            try {
                Thread.sleep(150);
            } catch (InterruptedException e) {
                System.out.println("[LetterPrinter] Interrupted!");
            }
        }
        System.out.println("[LetterPrinter] Finished.");
    }
}

// MAIN CLASS
public class Multithreading {

    public static void main(String[] args) throws InterruptedException {
        System.out.println(" Multithreading \n");

        // Create threads
        NumberPrinter thread1 = new NumberPrinter("Thread-Numbers-1to5", 1, 5);
        NumberPrinter thread2 = new NumberPrinter("Thread-Numbers-6to10", 6, 10);

        // Runnable approach
        Runnable letterTask = new LetterPrinter("ABCDE");
        Thread thread3 = new Thread(letterTask); // Wrap Runnable in Thread

        // Lambda shorthand for simple Runnable task
        Thread thread4 = new Thread(() -> {
            System.out.println("[LambdaThread] Running a quick task!");
        });

        System.out.println("Starting all threads...\n");

        // Start all threads — they run concurrently
        thread1.start();
        thread2.start();
        thread3.start();
        thread4.start();

        // Wait for all threads to finish before continuing
        thread1.join();
        thread2.join();
        thread3.join();
        thread4.join();

        System.out.println("\nAll threads have finished!");
        System.out.println("Main thread continues...");
    }
}