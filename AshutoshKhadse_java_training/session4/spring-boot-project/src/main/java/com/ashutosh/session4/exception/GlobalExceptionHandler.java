package com.ashutosh.session4.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.util.HashMap;
import java.util.Map;

// @RestControllerAdvice allows us to handle exceptions globally across all controllers.
// This centralizes error handling logic, ensuring consistent API responses.
@RestControllerAdvice
public class GlobalExceptionHandler {

    // Handles our custom TodoNotFoundException
    // User get a nice, structured JSON object and a clear 404 Not Found status code.
    @ExceptionHandler(TodoNotFoundException.class)
    public ResponseEntity<Map<String, String>> handleNotFound(TodoNotFoundException ex) {
        Map<String, String> error = new HashMap<>();
        error.put("error", "Resource Not Found");
        error.put("message", ex.getMessage());
        // In a real production system, we could also log ex.getTodoId()
        // I could easily log it here for our internal monitoring without exposing extra
        // technical details to the user.
        return new ResponseEntity<>(error, HttpStatus.NOT_FOUND);
    }

    // Handles our custom InvalidStatusTransitionException
    // I mapped this to a 400 Bad Request because it's technically a client-side error
    // they tried to do something that our project don't allow
    @ExceptionHandler(InvalidStatusTransitionException.class)
    public ResponseEntity<Map<String, String>> handleInvalidTransition(InvalidStatusTransitionException ex) {
        Map<String, String> error = new HashMap<>();
        error.put("error", "Bad Request");
        error.put("message", ex.getMessage());
        // We can access ex.getFromStatus() and ex.getToStatus() fields here,
        // in case we want to build complex error logs in the future.
        return new ResponseEntity<>(error, HttpStatus.BAD_REQUEST);
    }

    // This catches MethodArgumentNotValidException, which
    // happens when the @Valid check in our Controller fails like if a title is too short
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<Map<String, String>> handleValidationErrors(MethodArgumentNotValidException ex) {
        Map<String, String> errors = new HashMap<>();
        // Extracting only the field name and the specific error message for the client.
        // This makes it super easy for the frontend developer to show the error
        ex.getBindingResult().getFieldErrors().forEach(error ->
                errors.put(error.getField(), error.getDefaultMessage()));
        return new ResponseEntity<>(errors, HttpStatus.BAD_REQUEST);
    }
}