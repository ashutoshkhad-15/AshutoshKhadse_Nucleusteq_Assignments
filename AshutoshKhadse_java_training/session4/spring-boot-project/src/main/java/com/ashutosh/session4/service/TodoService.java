package com.ashutosh.session4.service;

import com.ashutosh.session4.dto.TodoRequestDTO;
import com.ashutosh.session4.dto.TodoResponseDTO;
import com.ashutosh.session4.entity.Todo;
import com.ashutosh.session4.entity.TodoStatus;
import com.ashutosh.session4.exception.TodoNotFoundException;
import com.ashutosh.session4.repository.TodoRepository;
import org.springframework.stereotype.Service;
import com.ashutosh.session4.exception.InvalidStatusTransitionException;
// added for logging functionalities
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

// I've added the @Service annotation to mark this as the business logic layer.
// this class handles all the data transformations.
@Service
public class TodoService {

    // I initialized the SLF4J logger specifically for the TodoService class.
    // Keeping it 'private static final' ensures we don't waste memory creating a new logger
    // object every time the service is called, and it accurately tags our logs in the console
    private static final Logger logger = LoggerFactory.getLogger(TodoService.class);

    private final TodoRepository todoRepository;
    // I added the NotificationServiceClient here as a 'private final' field.
    private final NotificationServiceClient notificationService;

    // Using constructor-based injection
    // I updated the constructor to accept our new notification service.
    public TodoService(TodoRepository todoRepository, NotificationServiceClient notificationService) {
        this.todoRepository = todoRepository;
        this.notificationService = notificationService;
    }

    // POST: Handles the logic for adding a new task.
    public TodoResponseDTO createTodo(TodoRequestDTO requestDTO) {

        // I added an INFO log right at the start of the method.
        // If something breaks during the save process,
        // we can look at the logs to look what failed
        // I also used the `{}` placeholder to let SLF4J handle injecting the title efficiently
        logger.info("Service: Processing request to create new TODO with title: {}", requestDTO.getTitle());

        // I'm creating a new Entity object and mapping the DTO fields to it
        Todo todo = new Todo();
        todo.setTitle(requestDTO.getTitle());
        todo.setDescription(requestDTO.getDescription());

        // Setting the Default status to PENDING if not provided.
        todo.setStatus(requestDTO.getStatus() != null ? requestDTO.getStatus() : TodoStatus.PENDING);

        // Set createdAt automatically not from user input
        todo.setCreatedAt(LocalDateTime.now());

        Todo savedTodo = todoRepository.save(todo);

        // after we successfully save the Todo, the dummy NotificationServiceClient is triggered
        notificationService.sendNotification("New TODO created: " + savedTodo.getTitle());

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

     // Updates an existing Todo's details and status.
     // I've structured this to allow "partial updates," meaning the client doesn't
     // have to send every single field if they only want to change the title.
    public TodoResponseDTO updateTodo(Long id, TodoRequestDTO requestDTO) {
        // 1. Verify existence using your custom exception
        // If the ID is invalid, this throws immediately, preventing any unnecessary logic execution
        Todo existingTodo = todoRepository.findById(id)
                .orElseThrow(() -> new TodoNotFoundException(id));

        // 2. Validate and Update Status
        // I only trigger the validation logic if the user is actually providing a new status
        // that is different from what we already have in the database.
        if (requestDTO.getStatus() != null && requestDTO.getStatus() != existingTodo.getStatus()) {
            validateStatusTransition(existingTodo.getStatus(), requestDTO.getStatus());
            existingTodo.setStatus(requestDTO.getStatus());
        }

        // 3. Update Title and Description
        // This ensures that a user can't accidentally "update" a title to just empty spaces.
        if (requestDTO.getTitle() != null && !requestDTO.getTitle().isBlank()) {
            existingTodo.setTitle(requestDTO.getTitle());
        }

        // 4. Update Description: Simple null check allows clearing a description if they send an empty string
        if (requestDTO.getDescription() != null) {
            existingTodo.setDescription(requestDTO.getDescription());
        }

        // Saving the updated state and converting it back to a DTO for the response.
        Todo updatedTodo = todoRepository.save(existingTodo);
        return mapToResponseDTO(updatedTodo);
    }

    // Deletes a Todo
    public void deleteTodo(Long id) {
        // Instead of just checking if it exists, I fetch the whole object
        Todo todo = todoRepository.findById(id)
                .orElseThrow(() -> new TodoNotFoundException(id));
        todoRepository.delete(todo);
    }

    // Tasks can only move between PENDING and COMPLETED.
    private void validateStatusTransition(TodoStatus current, TodoStatus requested) {
        // Only PENDING <-> COMPLETED is allowed.
        boolean isValid = (current == TodoStatus.PENDING && requested == TodoStatus.COMPLETED) ||
                (current == TodoStatus.COMPLETED && requested == TodoStatus.PENDING);

        if (!isValid) {
            // I'm using our custom exception here so the GlobalExceptionHandler
            // can tell the user exactly which transition was illegal
            throw new InvalidStatusTransitionException(current, requested);
        }
    }
}