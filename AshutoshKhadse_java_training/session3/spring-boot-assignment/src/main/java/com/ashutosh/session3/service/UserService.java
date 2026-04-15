package com.ashutosh.session3.service;

import com.ashutosh.session3.model.User;
import com.ashutosh.session3.repository.UserRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

// Marking this as a Service. This is where I'm putting all my core business logic
@Service
public class UserService {

    private final UserRepository userRepository;

    // Strict Constructor Injection
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

}