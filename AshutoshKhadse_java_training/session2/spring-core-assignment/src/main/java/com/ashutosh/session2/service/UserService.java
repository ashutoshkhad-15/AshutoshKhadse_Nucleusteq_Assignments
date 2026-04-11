package com.ashutosh.session2.service;

import com.ashutosh.session2.model.User;
import com.ashutosh.session2.repository.UserRepository;
import org.springframework.stereotype.Service;

import java.util.List;

// Marking this as a Service so Spring knows it handles our main business logic for users
@Service
public class UserService {

    // Making it final so it doesn't get changed by mistake
    private final UserRepository userRepository;

    // Constructor
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    // asking the repository to give us the full list of everyone we've saved
    public List<User> getAllUsers() {
        return userRepository.findAll();
    }

    // Trying to find a specific user using their ID number
    public User getUserById(Long id) {
        return userRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("User not found with id: " + id));
    }
    // Taking a new user and sending them over to the repository to be saved
    public User createUser(User user) {
        return userRepository.save(user);
    }
}

