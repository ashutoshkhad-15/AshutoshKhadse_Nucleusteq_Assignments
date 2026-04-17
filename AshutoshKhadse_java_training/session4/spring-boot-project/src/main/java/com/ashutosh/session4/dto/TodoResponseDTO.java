package com.ashutosh.session4.dto;

import com.ashutosh.session4.entity.TodoStatus;
import java.time.LocalDateTime;

// I created this Response DTO specifically to send data back to the client.
// I read that returning raw Database Entities directly to the frontend is a bad practice
// because it can accidentally expose sensitive data, tightly couple our database to the API,
// or cause infinite recursion issues when Spring tries to turn it into JSON.
public class TodoResponseDTO {

    private Long id;
    private String title;
    private String description;
    private TodoStatus status;
    private LocalDateTime createdAt;

    // Constructors

    // Default constructor. Frameworks like Spring and Jackson (the JSON converter)
    // often need an empty constructor to work properly behind the scenes.
    public TodoResponseDTO() {}

    // All-args constructor. I added this so I can easily create a fully populated DTO
    // in my Service layer in just one single line when I'm converting my Database Entity into this DTO.
    public TodoResponseDTO(Long id, String title, String description, TodoStatus status, LocalDateTime createdAt) {
        this.id = id;
        this.title = title;
        this.description = description;
        this.status = status;
        this.createdAt = createdAt;
    }

    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public TodoStatus getStatus() { return status; }
    public void setStatus(TodoStatus status) { this.status = status; }

    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
}
