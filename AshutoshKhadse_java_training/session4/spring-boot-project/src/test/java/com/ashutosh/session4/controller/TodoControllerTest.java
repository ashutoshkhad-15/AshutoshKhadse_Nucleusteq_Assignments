package com.ashutosh.session4.controller;

import com.ashutosh.session4.dto.TodoRequestDTO;
import com.ashutosh.session4.dto.TodoResponseDTO;
import com.ashutosh.session4.entity.TodoStatus;
import com.ashutosh.session4.exception.TodoNotFoundException;
import com.ashutosh.session4.service.TodoService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;

// I was reading the documentation and got to know that @MockBean is actually deprecated
// in the newest Spring Boot 3.4 releases So, I used the new
// @MockitoBean from the test.context.bean.override package to keep my code modern and future-proof.
import org.springframework.test.context.bean.override.mockito.MockitoBean;

import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.time.LocalDateTime;
import java.util.List;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.doNothing;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

// Unit Tests for TodoController
// I used @WebMvcTest because I only want to test the web layer (routing, validation, JSON serialization).
// I learned that this avoids loading the entire database and application context, so the tests run in milliseconds
@WebMvcTest(TodoController.class)
public class TodoControllerTest {

    // MockMvc acts as our internal "fake Postman". It lets me simulate real HTTP GET/POST calls
    // without actually starting a Tomcat server.
    @Autowired
    private MockMvc mockMvc;

    // ObjectMapper is crucial here. Since my Controller expects raw JSON in the @RequestBody,
    // this tool automatically converts my Java RequestDTOs into JSON strings for the tests.
    @Autowired
    private ObjectMapper objectMapper;

    // Replacing the real TodoService inside the partial Spring Application Context with my mock.
    // This ensures my Controller tests aren't accidentally hitting the real database
    @MockitoBean
    private TodoService todoService;

    // Reusable DTOs to keep my tests DRY (Don't Repeat Yourself).
    private TodoResponseDTO responseDTO;
    private TodoRequestDTO requestDTO;

    // I use @BeforeEach to instantiate fresh data before every single test.
    @BeforeEach
    void setUp() {
        requestDTO = new TodoRequestDTO("API Task", "Testing MockMvc", TodoStatus.PENDING);

        responseDTO = new TodoResponseDTO(
                1L,
                "API Task",
                "Testing MockMvc",
                TodoStatus.PENDING,
                LocalDateTime.now()
        );
    }

    @Test
    void createTodo_ShouldReturn201Created() throws Exception {
        // Arrange: Tell the mock service what to do.
        when(todoService.createTodo(any(TodoRequestDTO.class))).thenReturn(responseDTO);

        // Act & Assert: Execute the POST request and verify.
        mockMvc.perform(post("/todos")
                        .contentType(MediaType.APPLICATION_JSON)
                        // Injecting the JSON string here
                        .content(objectMapper.writeValueAsString(requestDTO)))
                // I explicitly check for 201 Created to ensure REST compliance.
                .andExpect(status().isCreated())
                // I learned how to use jsonPath to directly inspect the JSON response body
                .andExpect(jsonPath("$.title").value("API Task"));
    }

    @Test
    void getAllTodos_ShouldReturn200Ok_AndList() throws Exception {
        when(todoService.getAllTodos()).thenReturn(List.of(responseDTO));

        mockMvc.perform(get("/todos"))
                .andExpect(status().isOk())
                // Validating that the returned JSON array has exactly 1 item.
                .andExpect(jsonPath("$.size()").value(1))
                .andExpect(jsonPath("$[0].title").value("API Task"));
    }

    @Test
    void getTodoById_ShouldReturn200Ok_WhenExists() throws Exception {
        when(todoService.getTodoById(1L)).thenReturn(responseDTO);

        mockMvc.perform(get("/todos/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1L));
    }

    @Test
    void getTodoById_ShouldReturn404NotFound_WhenDoesNotExist() throws Exception {
        // Arrange: Simulate the business logic failing to find the ID.
        when(todoService.getTodoById(99L)).thenThrow(new TodoNotFoundException(99L));

        // Act & Assert: This proves that my GlobalExceptionHandler is successfully
        // catching the exception and translating it into a 404 HTTP status
        mockMvc.perform(get("/todos/99"))
                .andExpect(status().isNotFound());
    }

    @Test
    void updateTodo_ShouldReturn200Ok() throws Exception {
        // I used eq(1L) to strictly enforce that the mock only triggers if the ID in the URL matches.
        when(todoService.updateTodo(eq(1L), any(TodoRequestDTO.class))).thenReturn(responseDTO);

        mockMvc.perform(put("/todos/1")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(requestDTO)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.title").value("API Task"));
    }

    @Test
    void deleteTodo_ShouldReturn204NoContent() throws Exception {
        // Since delete is a void method, doNothing() tells Mockito to just let it pass.
        doNothing().when(todoService).deleteTodo(1L);

        mockMvc.perform(delete("/todos/1"))
                // Expecting 204 No Content since a successful delete returns an empty body.
                .andExpect(status().isNoContent());
    }
}