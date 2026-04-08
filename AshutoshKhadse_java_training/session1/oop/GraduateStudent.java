// 2) Implement inheritance to create a "GraduateStudent" class that extends the "Student" class with additional features.
package AshutoshKhadse_java_training.session1.oop;

public class GraduateStudent extends Student { //inheritance

    private String researchTopic;
    private double thesisScore;

    // Constructor calls parent constructor using super()
    public GraduateStudent(String name, int rollNumber, double marks,
            String researchTopic, double thesisScore) {
        super(name, rollNumber, marks); // Calling Student's constructor
        this.researchTopic = researchTopic;
        this.thesisScore = thesisScore;
    }

    public String getResearchTopic() {
        return researchTopic;
    }

    public double getThesisScore() {
        return thesisScore;
    }

    @Override // to include thesis score in grading
    public String getGrade() {
        double combinedScore = (getMarks() * 0.6) + (thesisScore * 0.4);
        if (combinedScore >= 90)
            return "A+ (Distinction)";
        else if (combinedScore >= 75)
            return "A (Merit)";
        else if (combinedScore >= 60)
            return "B (Pass)";
        else
            return "F (Fail)";
    }

    @Override // adds extra graduate student details.
    public void displayInfo() {
        super.displayInfo(); // First display Student info
        System.out.println("Research Topic : " + researchTopic);
        System.out.println("Thesis Score   : " + thesisScore);
        System.out.println("Combined Grade : " + getGrade());
    }

    public static void main(String[] args) {

        GraduateStudent gs = new GraduateStudent(
                "Ashutosh",
                101,
                85,
                "AI in Climate Tech", 
                90 
        );
        gs.displayInfo();
    }
}
