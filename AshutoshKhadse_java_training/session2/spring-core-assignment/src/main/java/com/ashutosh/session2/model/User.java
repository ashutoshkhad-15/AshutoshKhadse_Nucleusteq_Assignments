package com.ashutosh.session2.model;

// This is basic User model class to hold user details
public class User {
    private Long id;
    private String name;
    private String email;

    // Constructor
    public User(Long id, String name, String email) {
        this.id = id;
        this.name = name;
        this.email = email;
    }

    // Getters and Setters
    public Long getId()             { return id; }
    public void setId(Long id)      { this.id = id; }

    public String getName()             { return name; }
    public void   setName(String name)  { this.name = name; }

    public String getEmail()              { return email; }
    public void   setEmail(String email)  { this.email = email; }

    // Overriding toString so when we print a User object, we actually see their details instead of a memory address
    @Override
    public String toString() {
        return "User{id=" + id + ", name='" + name + "', email='" + email + "'}";
    }
}
