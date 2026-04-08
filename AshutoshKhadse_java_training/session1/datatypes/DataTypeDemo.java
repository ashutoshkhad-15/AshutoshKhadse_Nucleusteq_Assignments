// 1) Explain the difference between primitive and reference data types with examples.
package AshutoshKhadse_java_training.session1.datatypes;

/* 1. Primitive Data Types: 
        Primitive data types are the most basic, fundamental data types built directly into the Java language. 
        They are predefined by Java.
        They represent single, simple values.
        When we declare a primitive variable, the actual value is stored directly in that variable's allocated memory space 
        which is in the Stack memory.

    Characteristics:
        They have a predefined size in memory.
        They do not have methods or properties associated with them.
        They cannot be null. If you don't assign a value, they take a default value (e.g., 0 for numeric types, false for booleans).

    There are 8 Primitive Types in Java:
        byte, short, int, long (Whole numbers)
        float, double (Decimal numbers)
        boolean (True/false)
        char (Single character)
 */

/* 2. Reference Data Types:
        Reference data types are more complex and can represent objects, arrays, or any user-defined types. 
        They are not predefined by Java but are created by programmers using classes.
        When we declare a reference variable, it stores a reference (memory address) 
        to the actual object in the Heap memory, not the object itself.

    Characteristics:
        Their size is dynamic and depends on the complexity of the object.
        They provide access to methods and properties (e.g., myString.length()).
        They can be assigned a null value, which means the variable isn't pointing to any object in memory yet.

    Examples:
        String (e.g., String name = "Ashutosh";)
        Arrays (e.g., int[], String[])
        Custom classes (e.g., Student, Car)
        Wrapper classes (e.g., Integer, Double)
 */

public class DataTypeDemo {
    public static void main(String[] args) {
        
        System.out.println(" PRIMITIVE TYPES DEMO ");
        
        byte  smallNumber   = 100;               // 1 byte  
        short mediumNumber  = 30000;             // 2 bytes
        int   wholeNumber   = 123456789;         // 4 bytes 
        long  bigNumber     = 9876543210L;       // 8 bytes 
        float decimalShort  = 3.14f;             // 4 bytes 
        double decimalLong  = 3.141592653589793; // 8 bytes 
        char  singleChar    = 'A';               // 2 bytes 
        boolean isJavaFun   = true;              // 1 bit  

        System.out.println("byte    : " + smallNumber);
        System.out.println("short   : " + mediumNumber);
        System.out.println("int     : " + wholeNumber);
        System.out.println("long    : " + bigNumber);
        System.out.println("float   : " + decimalShort);
        System.out.println("double  : " + decimalLong);
        System.out.println("char    : " + singleChar);
        System.out.println("boolean : " + isJavaFun);

        // KEY POINT: Primitives are copied by VALUE
        System.out.println("\n Primitive Copy Behavior ");
        int originalValue = 50;
        int copiedValue   = originalValue; // A COPY is made
        copiedValue = 99;                  // Changing copy does NOT affect original
        System.out.println("Original: " + originalValue); // Still 50
        System.out.println("Copy    : " + copiedValue);   // 99

        System.out.println("\n REFERENCE TYPES DEMO ");

        // String 
        String greeting = "Hello, Java!";
        System.out.println("String  : " + greeting);

        // Array
        int[] numbers = {10, 20, 30};
        System.out.println("Array   : " + numbers[0] + ", " + numbers[1] + ", " + numbers[2]);

        // Object (custom class) 
        StudentRecord student = new StudentRecord("Alice", 101);
        System.out.println("Object  : " + student.getName() + " (Roll: " + student.getRollNumber() + ")");

        // Reference types are copied by REFERENCE (both point to same object)
        System.out.println("\n Reference Copy Behavior ");
        StudentRecord student2 = student; // Both point to SAME object
        student2.setName("Bob");          // Changing via student2 ALSO changes student!
        System.out.println("student.getName()  : " + student.getName());  // Bob (changed!)
        System.out.println("student2.getName() : " + student2.getName()); // Bob
    }
}

// Helper class 
class StudentRecord {
    private String name;
    private int rollNumber;

    public StudentRecord(String name, int rollNumber) {
        this.name = name;
        this.rollNumber = rollNumber;
    }

    public String getName()          { return name; }
    public void   setName(String n)  { this.name = n; }
    public int    getRollNumber()    { return rollNumber; }
}
