// 1) Explain the concept of interfaces and abstract classes with examples. 
package AshutoshKhadse_java_training.session1.advanced;

/*
ABSTRACT CLASS:
   An abstract class is a class that cannot be created directly. It is mainly used as a base class for other classes. 
   It can contain both abstract methods (methods without a body) and normal methods (methods with implementation).
   Abstract classes can have instance variables and constructors
   A class can extend only ONE abstract class
   Abstract classes are useful when we want to define some common functionality that all subclasses should share, 
   while allowing subclasses to provide their own specific implementation for certain methods.
 */

 /*
INTERFACE:
   An interface is like a blueprint of a class.
   It contains only method declarations (without implementation) and constants.
   A class that implements an interface must provide the implementation for all its methods.
   Interfaces are mainly used when we want to define a set of rules or
   capabilities that multiple classes can follow,
   regardless of their hierarchy.
   Interfaces cannot have constructors and only contain constants.
   A class can implement MULTIPLE interfaces
 */


// ABSTRACT CLASS
abstract class Animal {
    protected String name; 

    public Animal(String name) {
        this.name = name;
    }

    public void breathe() {
        System.out.println(name + " is breathing.");
    }

    // Abstract method each animal MUST define how it speaks
    public abstract void makeSound();

    // Abstract method each animal defines its movement
    public abstract void move();
}

// INTERFACES
interface Swimmable {
    void swim(); // Implicitly public and abstract
}

interface Flyable {
    void fly();
}

// CONCRETE CLASSES

// Dog extends Animal (abstract class) AND implements Swimmable (interface)
class Dog extends Animal implements Swimmable {

    public Dog(String name) {
        super(name);
    }

    @Override
    public void makeSound() {
        System.out.println(name + " says: Woof! Woof!");
    }

    @Override
    public void move() {
        System.out.println(name + " runs on four legs.");
    }

    @Override
    public void swim() {
        System.out.println(name + " is swimming!");
    }
}

// Duck extends Animal AND implements both Swimmable and Flyable
class Duck extends Animal implements Swimmable, Flyable {

    public Duck(String name) {
        super(name);
    }

    @Override
    public void makeSound() {
        System.out.println(name + " says: Quack! Quack!");
    }

    @Override
    public void move() {
        System.out.println(name + " waddles.");
    }

    @Override
    public void swim() {
        System.out.println(name + " is swimming like a duck!");
    }

    @Override
    public void fly() {
        System.out.println(name + " is flying!");
    }
}

// MAIN CLASS
public class InterfaceAbstractClassExample  {

    public static void main(String[] args) {
        System.out.println(" Abstract Class & Interface Demo \n");

        Animal myDog  = new Dog("Rex");
        Animal myDuck = new Duck("Donald");

        System.out.println(" Dog ");
        myDog.breathe();   // From Animal 
        myDog.makeSound(); // Overridden in Dog
        myDog.move();
        ((Swimmable) myDog).swim(); // Casting to use interface method

        System.out.println("\n Duck ");
        myDuck.breathe();
        myDuck.makeSound();
        myDuck.move();
        ((Swimmable) myDuck).swim();
        ((Flyable)   myDuck).fly();

        // Key Differences between Abstract Classes and Interfaces
        // Abstract Class : Animal (one class only)
        // Interfaces     : Swimmable, Flyable (multiple allowed)
    }
}
