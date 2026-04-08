// 4) Explain the concept of encapsulation with a suitable example
package AshutoshKhadse_java_training.session1.oop;

/*
   Encapsulation is one of the fundamental principles of Object-Oriented Programming (OOP). 
   It refers to the process of wrapping data (variables) and methods (functions) into a single unit called a class, 
   and restricting direct access to the internal data of the object.
   In encapsulation, the internal state of an object is hidden from the outside world, 
   and access is provided only through well-defined methods. 
   This ensures that the data is accessed and modified in a controlled and secure manner. 

   Advantages of Encapsulation
       Data Security
       Data Integrity
       Modularity
       Flexibility
       Ease of Maintenance
*/
class BankAccount {
    // Private data (hidden)
    private String accountHolder;
    private double balance;

    public BankAccount(String accountHolder, double balance) {
        this.accountHolder = accountHolder;
        this.balance = balance;
    }

    // Getter (read access)
    public String getAccountHolder() {
        return accountHolder;
    }

    public double getBalance() {
        return balance;
    }

    // Setter (controlled write access)
    public void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
        } else {
            System.out.println("Invalid deposit amount!");
        }
    }

    public void withdraw(double amount) {
        if (amount > 0 && amount <= balance) {
            balance -= amount;
        } else {
            System.out.println("Invalid withdrawal!");
        }
    }
}

public class Encapsulation {
    public static void main(String[] args) {

        BankAccount acc = new BankAccount("Ashutosh", 1000);

        // Access via methods only
        acc.deposit(500);
        acc.withdraw(200);

        System.out.println("Account Holder: " + acc.getAccountHolder());
        System.out.println("Balance: " + acc.getBalance());

        // This way Direct access not allowed
        // like doing acc.balance = 100000; 
        // it would cause a compilation error because balance is private and cannot be accessed directly.
    }
}
