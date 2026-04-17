package com.ashutosh.session4.service;

import com.ashutosh.session4.dto.TodoRequestDTO;
import com.ashutosh.session4.dto.TodoResponseDTO;
import com.ashutosh.session4.entity.Todo;
import com.ashutosh.session4.entity.TodoStatus;
import com.ashutosh.session4.exception.TodoNotFoundException;
import com.ashutosh.session4.repository.TodoRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

// I've added the @Service annotation to mark this as the business logic layer.
// this class handles all the data transformations.
@Service
public class TodoService {

    private final TodoRepository todoRepository;

    // Using constructor-based injection
    public TodoService(TodoRepository todoRepository) {
        this.todoRepository = todoRepository;
    }

    // POST: Handles the logic for adding a new task.
    public TodoResponseDTO createTodo(TodoRequestDTO requestDTO) {
        // I'm creating a new Entity object and mapping the DTO fields to it
        Todo todo = new Todo();
        todo.setTitle(requestDTO.getTitle());
        todo.setDescription(requestDTO.getDescription());

        // Setting the Default status to PENDING if not provided.
        todo.setStatus(requestDTO.getStatus() != null ? requestDTO.getStatus() : TodoStatus.PENDING);

        // Set createdAt automatically not from user input
        todo.setCreatedAt(LocalDateTime.now());

        Todo savedTodo = todoRepository.save(todo);
        // returning a ResponseDTO so the frontend never sees the raw Entity
        return mapToResponseDTO(savedTodo);
    }

    // GET ALL: Returns a list of all DTOs.
    public List<TodoResponseDTO> getAllTodos() {
        // I used a stream here It fetches all entities, transforms each one using our helper method
        // and bundles them into a clean list
        return todoRepository.findAll()
                .stream()
                .map(this::mapToResponseDTO)
                .collect(Collectors.toList());
    }

    // GET BY ID: Returns a single DTO or throws our custom exception.
    public TodoResponseDTO getTodoById(Long id) {
        // I used .orElseThrow() to handle the "Not Found"
        // we created TodoNotFoundException, our GlobalExceptionHandler
        // will automatically turn this into a 404 response.
        Todo todo = todoRepository.findById(id)
                .orElseThrow(() -> new TodoNotFoundException(id));
        return mapToResponseDTO(todo);
    }

    // Helper method to manually map Entity to DTO, No MapStruct/Lombok used
    private TodoResponseDTO mapToResponseDTO(Todo todo) {
        return new TodoResponseDTO(
                todo.getId(),
                todo.getTitle(),
                todo.getDescription(),
                todo.getStatus(),
                todo.getCreatedAt()
        );
    }
}