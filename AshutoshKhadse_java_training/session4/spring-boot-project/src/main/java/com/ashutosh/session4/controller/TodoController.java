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

    // 3. GET TODO BY ID (GET /todos/{id})
    // I used @PathVariable to grab the ID directly from the URL.
    // If the service doesn't find the todo, it throws an exception which our
    // GlobalExceptionHandler handles, so I can keep this method simple and clean.
    @GetMapping("/{id}")
    public ResponseEntity<TodoResponseDTO> getTodoById(@PathVariable Long id) {
        TodoResponseDTO todo = todoService.getTodoById(id);
        return ResponseEntity.ok(todo);
    }

    // 4. UPDATE TODO (PUT /todos/{id})
    // I'm using @Valid here because even when updating, we must ensure
    // the title and description follow our length and nullability rules.
    @PutMapping("/{id}")
    public ResponseEntity<TodoResponseDTO> updateTodo(
            @PathVariable Long id,
            @Valid @RequestBody TodoRequestDTO requestDTO) {
        // I'm passing both the ID from the URL and the data from the Body
        // to the service layer to handle the state-transition business logic.
        TodoResponseDTO updatedTodo = todoService.updateTodo(id, requestDTO);
        return ResponseEntity.ok(updatedTodo);
    }

    // 5. DELETE TODO (DELETE /todos/{id})
    // For the delete operation, I noticed that we don't really have any data
    // to send back to the user once the record is gone.
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteTodo(@PathVariable Long id) {
        todoService.deleteTodo(id);
        // Following standard REST practices, I'm returning '204 No Content'
        // It's a clear signal to the client that the action was successful
        // and there is nothing more to show.
        return ResponseEntity.noContent().build();
    }
}