// I am using the provided array of student objects, so that i can access each student's data and I have also added test cases for fail conditions 

const students = [
  {
    name: "Lalit",
    marks: [
      { subject: "Math",     score: 78 },
      { subject: "English",  score: 82 },
      { subject: "Science",  score: 74 },
      { subject: "History",  score: 69 },
      { subject: "Computer", score: 88 }
    ],
    attendance: 82
  },
  {
    name: "Rahul",
    marks: [
      { subject: "Math",     score: 90 },
      { subject: "English",  score: 85 },
      { subject: "Science",  score: 80 },
      { subject: "History",  score: 76 },
      { subject: "Computer", score: 92 }
    ],
    attendance: 91
  },
  {
    name: "Vishesh",
    marks: [
      { subject: "Math",     score: 55 },
      { subject: "English",  score: 60 },
      { subject: "Science",  score: 58 },
      { subject: "History",  score: 52 },
      { subject: "Computer", score: 50 }
    ],
    attendance: 70   // This test case is added for the below 75 attendance fail condition
  },
  {
    name: "Ashwini",
    marks: [
      { subject: "Math",     score: 72 },
      { subject: "English",  score: 68 },
      { subject: "Science",  score: 38 },  // This test case is added for the ≤40 marks per subject fail condition
      { subject: "History",  score: 65 },
      { subject: "Computer", score: 70 }
    ],
    attendance: 85
  }
];

// This is a funciton to get the total marks of a student in the array of students using the forEach loop.

function getTotalMarks(student) {
  let total = 0;
  student.marks.forEach(function(markEntry) {
    total += markEntry.score;
  });
  return total;
}

// This is a function to get the average marks of a student in the array of students. I also used parseFloat to keep format decimal digits fixed to 1.
function AverageMarks(student) {
  const total = getTotalMarks(student);
  const avg = total / student.marks.length;
  return parseFloat(avg.toFixed(1));
}

// This is a function to get the grade of a student based on the average marks. 
// I have also added the fail condition for ≤40 marks per subject and below 75 attendance.
function Grade(student) {
  const avg = AverageMarks(student);
  // Fail condition 1: attendance below 75%
  if (student.attendance < 75) {
    return "Fail (Low Attendance)";
  }
  // Fail condition 2: any single subject score is 40 or below
  for (let i = 0; i < student.marks.length; i++) {
    if (student.marks[i].score <= 40) {
      return "Fail (Failed in " + student.marks[i].subject + ")";
    }
  }
  // Average-based grade scale
  if (avg >= 85) return "A";
  if (avg >= 70) return "B";
  if (avg >= 50) return "C";
  return "Fail";
}

// This is a function to analyze a student and return an object with their name, total marks, average marks, and grade.
function displayTotalsAndAverages() {
  console.log("____________________________________________");
  console.log("       TOTAL MARKS & AVERAGES");
  console.log("____________________________________________");

  students.forEach(function(student) {
    const total = getTotalMarks(student);
    const avg   = AverageMarks(student);
    console.log(student.name + " Total Marks: " + total);
    console.log(student.name + " Average: " + avg);
    console.log("--------------------------------------------");
  });
}

function displayGrades() {
  console.log("____________________________________________");
  console.log("              STUDENT GRADES");
  console.log("____________________________________________");

  students.forEach(function(student) {
    const grade = Grade(student);
    console.log(student.name + " Grade: " + grade);
  });
}