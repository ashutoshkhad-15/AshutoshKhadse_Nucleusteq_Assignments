package com.ashutosh.session4.service;

import com.ashutosh.session4.repository.TodoRepository;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

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

}