// 1) Create a class to represent a student with attributes like name, roll number, and marks. 
package AshutoshKhadse_java_training.session1.oop;

public class Student {

    private String name;
    private int rollNumber;
    private double marks;

    // Constructor
    public Student(String name, int rollNumber, double marks) {
        this.name = name;
        this.rollNumber = rollNumber;
        this.marks = marks;
    }

    // Getters and Setters
    public String getName() {
        return name;
    }

    public void setName(String n) {
        this.name = n;
    }

    public int getRollNumber() {
        return rollNumber;
    }

    public void setRollNumber(int r) {
        this.rollNumber = r;
    }

    public double getMarks() {
        return marks;
    }

    public void setMarks(double m) {
        if (m >= 0 && m <= 100) {
            this.marks = m;
        } else {
            System.out.println("Invalid marks! Must be between 0 and 100.");
        }
    }

    // Method to determine grade — can be OVERRIDDEN in subclasses (Polymorphism)
    public String getGrade() {
        if (marks >= 90) return "A+";
        else if (marks >= 80) return "A";
        else if (marks >= 70) return "B";
        else if (marks >= 60) return "C";
        else return "F";
    }

    // Method to display student info
    public void displayInfo() {
        System.out.println("Name        : " + name);
        System.out.println("Roll Number : " + rollNumber);
        System.out.println("Marks       : " + marks);
        System.out.println("Grade       : " + getGrade());
    }

    public static void main(String[] args) {

        // Creating student object
        Student student1 = new Student("Ashutosh", 101, 85.5);

        // Display using method
        System.out.println(" Display Info ");
        student1.displayInfo();

        // Testing setter validation
        System.out.println("\n Testing Validation ");
        student1.setMarks(120); // invalid
        student1.setMarks(92); // valid

        // Final output
        System.out.println("\n Updated Student ");
        student1.displayInfo();
    }
}