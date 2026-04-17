package com.ashutosh.session4.exception;

// I have created a specific exception just for Todos
public class TodoNotFoundException extends RuntimeException {

    // I kept this field 'final' because once the exception is thrown for a specific ID and that ID should not change
    private final Long todoId;

    public TodoNotFoundException(Long todoId) {
        // I used a descriptive message in super showing ID not found
        super("Todo with id " + todoId + " not found");
        // I'm also saving the actual ID into the class field.
        this.todoId = todoId;
    }

    // I added a getter for the ID so that our Global Exception Handler
    // can use the same ID to send back in a custom JSON error response
    public Long getTodoId() {
        return todoId;
    }
}