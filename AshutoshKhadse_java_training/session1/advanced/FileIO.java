// 3) Implement a simple file I/O operation to read data from a text file. 
package AshutoshKhadse_java_training.session1.advanced;

import java.io.*;

public class FileIO{

    private static final String FILE_NAME = "students.txt";

    public static void main(String[] args) {
        // Step 1: Write to file
        writeToFile();

        // Step 2: Read from file
        readFromFile();

        // Step 3: Append to file
        appendToFile("David, 104, 91.5");

        // Step 4: Read again to confirm append
        System.out.println("\n After Appending ");
        readFromFile();
    }

    //  Writes student data to a file using BufferedWriter.
    //  BufferedWriter is faster than FileWriter alone.
    private static void writeToFile() {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(FILE_NAME))) {
            writer.write("Name, RollNo, Marks");
            writer.newLine();
            writer.write("Alice, 101, 88.5");
            writer.newLine();
            writer.write("Bob, 102, 76.0");
            writer.newLine();
            writer.write("Charlie, 103, 95.0");
            writer.newLine();

            System.out.println("Data written to \"" + FILE_NAME + "\" successfully.");

        } catch (IOException e) {
            System.out.println("Error writing to file: " + e.getMessage());
        }
        // try with resources automatically closes the writer
    }
    
    // Reads and displays all lines from the file using BufferedReader.
    private static void readFromFile() {
        System.out.println("\n Reading from \"" + FILE_NAME + "\"");

        try (BufferedReader reader = new BufferedReader(new FileReader(FILE_NAME))) {
            String line;
            int lineNumber = 1;

            while ((line = reader.readLine()) != null) {
                System.out.println(lineNumber + ": " + line);
                lineNumber++;
            }

        } catch (FileNotFoundException e) {
            System.out.println("File not found: " + FILE_NAME);
        } catch (IOException e) {
            System.out.println("Error reading file: " + e.getMessage());
        }
    }

    //   Appends a new line to the existing file.
    //   'true' in FileWriter constructor = append mode.
    private static void appendToFile(String newEntry) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(FILE_NAME, true))) {
            writer.write(newEntry);
            writer.newLine();
            System.out.println("\nAppended: \"" + newEntry + "\"");

        } catch (IOException e) {
            System.out.println("Error appending to file: " + e.getMessage());
        }
    }
}
