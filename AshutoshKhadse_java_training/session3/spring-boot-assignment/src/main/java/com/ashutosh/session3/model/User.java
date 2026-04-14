package com.ashutosh.session3.model;

// This is my main User model class. I'm using it as a simple container to hold user details across the application.
public class User {
    private Long id;
    private String name;
    private Integer age;
    private String role;
    private String email;

    // Constructor
    public User(Long id, String name, Integer age, String role, String email) {
        this.id = id;
        this.name = name;
        this.age = age;
        this.role = role;
        this.email = email;
    }

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Integer getAge() {
        return age;
    }

    public void setAge(Integer age) {
        this.age = age;
    }

    public String getRole() {
        return role;
    }

    public void setRole(String role) {
        this.role = role;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }
}
