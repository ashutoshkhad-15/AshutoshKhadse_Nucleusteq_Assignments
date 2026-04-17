package com.ashutosh.session4.dto;

import com.ashutosh.session4.entity.TodoStatus;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

// I created this Request DTO to handle incoming data from the client (like a POST or PUT).
// I learned that we shouldn't use the Response DTO or the main Entity for incoming requests because
// the client shouldn't be allowed to send fields like 'id' or 'createdAt' (the database/server handles those).
public class TodoRequestDTO {

    // Using Jakarta Validation annotations here to catch bad data right at the Controller layer.
    // By adding these, Spring will automatically validate the incoming JSON before my Service even sees it
    @NotNull(message = "Title cannot be null")
    @Size(min = 3, max = 200, message = "Title must be at least 3 characters")
    private String title;

    // Capped description at 1000 characters so it don't overload our database
    @Size(max = 1000, message = "Description must not exceed 1000 characters")
    private String description;

    private TodoStatus status;

    // Constructors

    // Default constructor. Jackson needs this to instantiate the object when it deserializes
    // the incoming JSON request body into this Java class.
    public TodoRequestDTO() {}

    // Parameterized constructor for easy object creation
    public TodoRequestDTO(String title, String description, TodoStatus status) {
        this.title = title;
        this.description = description;
        this.status = status;
    }

    // Getters and Setters

    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public TodoStatus getStatus() { return status; }
    public void setStatus(TodoStatus status) { this.status = status; }

}
