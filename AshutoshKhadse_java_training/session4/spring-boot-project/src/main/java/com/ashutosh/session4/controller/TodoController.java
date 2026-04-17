package com.ashutosh.session4.controller;

import com.ashutosh.session4.dto.TodoRequestDTO;
import com.ashutosh.session4.dto.TodoResponseDTO;
import com.ashutosh.session4.service.TodoService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

// I used @RestController so Spring knows every method here will return data
// I also added @RequestMapping("/todos") at the class level
// to keep my code DRY—this way, I don't have to repeat "/todos" in every method path.
@RestController
@RequestMapping("/todos")
public class TodoController {

    private final TodoService todoService;

    // Constructor injection for the service layer
    public TodoController(TodoService todoService) {
        this.todoService = todoService;
    }

    // 1. CREATE TODO (POST /todos)
    // I added @Valid here to trigger the validation rules we defined in TodoRequestDTO.
    // If the title is too short, the request will stop here and jump straight to
    // our GlobalExceptionHandler before it even hits the service
    @PostMapping
    public ResponseEntity<TodoResponseDTO> createTodo(@Valid @RequestBody TodoRequestDTO requestDTO) {
        TodoResponseDTO response = todoService.createTodo(requestDTO);
        // Returning 201 Created as per REST best practices for POST requests
        return new ResponseEntity<>(response, HttpStatus.CREATED);
    }

    // 2. GET ALL TODOS (GET /todos)
    // This is a GET request to fetch the entire list.
    @GetMapping
    public ResponseEntity<List<TodoResponseDTO>> getAllTodos() {
        List<TodoResponseDTO> todos = todoService.getAllTodos();
        // ResponseEntity.ok() here returns the list with a 200 OK status.
        return ResponseEntity.ok(todos);
    }
}