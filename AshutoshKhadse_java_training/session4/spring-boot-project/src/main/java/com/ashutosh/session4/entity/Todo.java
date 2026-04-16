package com.ashutosh.session4.entity;

// Importing required JPA annotations for database mapping
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

import java.time.LocalDateTime;
// Here Entity Marks this class as a JPA Entity which will be mapped to a database table
@Entity
// Specifies the table name in the database
@Table(name = "todos")
public class Todo {

    // @Id means it is Primary key of the table
    @Id
    // @GeneratedValue Auto-generates ID using database identity (auto-increment)
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // Title of the Todo task
    // Cannot be null and maximum length is 200 characters
    @Column(nullable = false, length = 200)
    private String title;

    // Description of the Todo task
    // Optional field with max length 1000 characters
    @Column(length = 1000)
    private String description;

    // Status of the Todo (PENDING or COMPLETED)
    // Stored as String in the database
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private TodoStatus status;

    // Stores the creation date and time of the Todo task
    // Cannot be updated once created
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    // Default constructor required by JPA
    public Todo() {
    }

    // Parameterized constructor for easy instantiation
    public Todo(String title, String description, TodoStatus status, LocalDateTime createdAt) {
        this.title = title;
        this.description = description;
        this.status = status;
        this.createdAt = createdAt;
    }

    // Getters and Setters

    // Getter for ID
    public Long getId() {
        return id;
    }

    // Setter for ID
    public void setId(Long id) {
        this.id = id;
    }

    // Getter for title
    public String getTitle() {
        return title;
    }

    // Setter for title
    public void setTitle(String title) {
        this.title = title;
    }

    // Getter for description
    public String getDescription() {
        return description;
    }

    // Setter for description
    public void setDescription(String description) {
        this.description = description;
    }

    // Getter for status
    public TodoStatus getStatus() {
        return status;
    }

    // Setter for status
    public void setStatus(TodoStatus status) {
        this.status = status;
    }

    // Getter for createdAt
    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    // Setter for createdAt
    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
}