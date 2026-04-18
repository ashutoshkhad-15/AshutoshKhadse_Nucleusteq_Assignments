package com.ashutosh.session4.service;

import com.ashutosh.session4.repository.TodoRepository;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import com.ashutosh.session4.dto.TodoRequestDTO;
import com.ashutosh.session4.dto.TodoResponseDTO;
import com.ashutosh.session4.entity.Todo;
import com.ashutosh.session4.entity.TodoStatus;
import com.ashutosh.session4.exception.InvalidStatusTransitionException;
import com.ashutosh.session4.exception.TodoNotFoundException;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

// I'm using the MockitoExtension here to enable mock injections.
// This allows me to test the TodoService in complete isolation without
// actually hitting the H2 database.
@ExtendWith(MockitoExtension.class)
public class TodoServiceTest {

    // I mocked the repository because we only want to test the business logic
    // in the service layer, not the actual database saving process.
    @Mock
    private TodoRepository todoRepository;

    // I'm also mocking the notification client so we can verify it gets called
    // without it actually trying to send real notifications during the test run.
    @Mock
    private NotificationServiceClient notificationService;

    // @InjectMocks creates a real instance of TodoService and automatically
    // injects the mocked repository and notification service I defined above into it.
    @InjectMocks
    private TodoService todoService;

    private Todo pendingTodo;

    // I created this @BeforeEach annotation to ensure we have a fresh, predictable
    // object to test against before every single method runs.
    @BeforeEach
    void setUp() {
        pendingTodo = new Todo();
        pendingTodo.setId(1L);
        pendingTodo.setTitle("Sample Todo");
        pendingTodo.setDescription("A test todo item");
        pendingTodo.setStatus(TodoStatus.PENDING);
        pendingTodo.setCreatedAt(LocalDateTime.now());
    }

    // I structured all my tests using the "Arrange, Act, Assert" (AAA) pattern
    // to make them easy for anyone reviewing my code to read.
    @Test
    void createTodo_ShouldSaveTodoAndTriggerNotification() {
        // Arrange: Set up the mock to return our pre-made 'pendingTodo' whenever save() is called.
        // I used 'any(Todo.class)' because the exact object being saved is created *inside* the service method.
        TodoRequestDTO request = new TodoRequestDTO("New Task", "Desc", TodoStatus.PENDING);
        when(todoRepository.save(any(Todo.class))).thenReturn(pendingTodo);

        // Act: Actually call the method we are testing.
        TodoResponseDTO response = todoService.createTodo(request);

        // Assert: Verify the response is not null and mapped correctly.
        assertNotNull(response);
        assertEquals("Sample Todo", response.getTitle());

        // Verify: Check that the notification service was called exactly once.
        // I used anyString() here just in case the exact string format changes later
        verify(notificationService, times(1)).sendNotification(anyString());
    }

    @Test
    void getAllTodos_ShouldReturnList() {
        // Arrange: Tell the mock repository to return a list containing our single item.
        when(todoRepository.findAll()).thenReturn(List.of(pendingTodo));

        // Act
        List<TodoResponseDTO> result = todoService.getAllTodos();

        // Assert: Ensure the list has 1 item and the data mapped perfectly.
        assertEquals(1, result.size());
        assertEquals("Sample Todo", result.get(0).getTitle());
    }

    @Test
    void getTodoById_ShouldReturnTodo_WhenExists() {
        // Arrange: We wrap our entity in an Optional because that's what JpaRepository returns.
        when(todoRepository.findById(1L)).thenReturn(Optional.of(pendingTodo));

        // Act
        TodoResponseDTO result = todoService.getTodoById(1L);

        // Assert
        assertEquals(1L, result.getId());
        assertEquals("Sample Todo", result.getTitle());
    }

    @Test
    void updateTodo_ShouldUpdateAndReturnTodo() {
        // Arrange: We have to mock BOTH the findById (to check if it exists) AND the save (to return updated data).
        when(todoRepository.findById(1L)).thenReturn(Optional.of(pendingTodo));
        when(todoRepository.save(any(Todo.class))).thenReturn(pendingTodo);

        TodoRequestDTO request = new TodoRequestDTO("Updated Title", "Updated Desc", TodoStatus.COMPLETED);

        // Act
        TodoResponseDTO result = todoService.updateTodo(1L, request);

        // Assert: We verify that the status transition was successfully mapped to the response.
        assertEquals(TodoStatus.COMPLETED, result.getStatus());

        // I also want to verify that the repository actually called save() on our object!
        verify(todoRepository, times(1)).save(any(Todo.class));
    }

    @Test
    void deleteTodo_ShouldCallRepositoryDelete() {
        // Arrange: Mock the findById to simulate the item existing in the database.
        when(todoRepository.findById(1L)).thenReturn(Optional.of(pendingTodo));

        // Act: Since delete returns void, we just call it.
        todoService.deleteTodo(1L);

        // Assert: The only way to test a void method is to verify that its internal dependencies were called!
        // So I'm verifying that the repository's delete() method was executed exactly once with our object.
        verify(todoRepository, times(1)).delete(pendingTodo);
    }

    // Exception & Edge Case Testing
    // I wanted to make sure my code doesn't just work when everything goes right,
    // but also handles failures gracefully and exactly as we designed it to

    @Test
    void getTodoById_ShouldThrowException_WhenIdNotFound() {
        // Arrange: Simulate the database returning completely empty
        when(todoRepository.findById(99L)).thenReturn(Optional.empty());

        // Act & Assert: I used assertThrows here. I learned that this is the best way
        // to test exceptions in JUnit 5. It expects my specific TodoNotFoundException
        // to be thrown when the lambda function (todoService.getTodoById) executes.
        assertThrows(TodoNotFoundException.class, () -> todoService.getTodoById(99L));
    }

    @Test
    void updateTodo_ShouldThrowException_WhenIdNotFound() {
        // Arrange: Same as above, simulating a non-existent ID.
        when(todoRepository.findById(99L)).thenReturn(Optional.empty());
        TodoRequestDTO request = new TodoRequestDTO("Title", "Desc", TodoStatus.COMPLETED);

        // Act & Assert: Making sure the update method also throws our custom 404 exception
        // before it even tries to process the data.
        assertThrows(TodoNotFoundException.class, () -> todoService.updateTodo(99L, request));
    }

    @Test
    void updateTodo_ShouldThrowException_WhenInvalidStatusTransition() {
        // Arrange: Our existing task in the mock database is set to PENDING.
        when(todoRepository.findById(1L)).thenReturn(Optional.of(pendingTodo));

        // Act: User tries to update it to PENDING again (which our validation logic blocks)
        TodoRequestDTO request = new TodoRequestDTO("Title", "Desc", TodoStatus.PENDING);

        // Assert: Verify that our business logic catches the bad transition.
        assertThrows(InvalidStatusTransitionException.class, () -> todoService.updateTodo(1L, request));
    }

    @Test
    void deleteTodo_ShouldThrowException_WhenIdNotFound() {
        // Arrange: Simulate the ID not existing.
        when(todoRepository.findById(99L)).thenReturn(Optional.empty());

        // Act & Assert: Check for the exception.
        assertThrows(TodoNotFoundException.class, () -> todoService.deleteTodo(99L));

        // Verify: I used never() to explicitly guarantee
        // that if the ID is not found, the service completely stops and absolutely
        // DOES NOT try to call the delete method on the repository.
        verify(todoRepository, never()).delete(any());
    }
}