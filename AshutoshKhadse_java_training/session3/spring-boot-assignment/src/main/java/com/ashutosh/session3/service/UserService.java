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
    // 1. SEARCH USERS (GET /users/search)

    // This method handles the dynamic searching.
    public List<User> searchUsers(String name, Integer age, String role) {
        // I'm grabbing all users and passing them through a stream pipeline.
        // It checks each user against our filters one by one, and then collects the
        // ones that pass into a new list.
        return userRepository.findAll().stream()
                .filter(user -> matchesName(user, name))
                .filter(user -> matchesAge(user, age))
                .filter(user -> matchesRole(user, role))
                .collect(Collectors.toList());
    }

    // Helper Methods for Filtering

    private boolean matchesName(User user, String name) {
        // If the user didn't provide a name to search for, I just return true.
        // This basically tells the stream to skip this filter and keep the user in the
        // list.
        if (name == null || name.isBlank())
            return true;
        return user.getName().equalsIgnoreCase(name); // case-insensitive exact match
    }

    private boolean matchesAge(User user, Integer age) {
        // Same logic here, If age is null, we just ignore the age filter entirely.
        if (age == null)
            return true;
        return user.getAge().equals(age); // exact match
    }

    private boolean matchesRole(User user, String role) {
        // Checking the role, ignoring case just in case someone searches for "admin"
        // instead of "ADMIN"
        if (role == null || role.isBlank())
            return true;
        return user.getRole().equalsIgnoreCase(role); // case-insensitive match
    }

    // 2. SUBMIT USER (POST /users/submit)
    public void saveUser(User user) {
        // custom validation to make sure the user didn't send bad data
        validateUser(user);

        // Normalize role for consistency
        user.setRole(user.getRole().toUpperCase());

        userRepository.save(user);
    }

    // Helper Method for Validation
    // I created private method so saveUser() stays clean and readable
    private void validateUser(User user) {
        // I noticed that if someone sends an empty JSON object "{}", Spring creates a User object
        // where all fields are null. So I added this extra check to catch that specific scenario
        if (user == null || (user.getName() == null && user.getAge() == null && user.getRole() == null)) {
            // Using standard IllegalArgumentException. As Global Exception Handler
            // can easily catch these and turn them into nice 400 Bad Request responses
            throw new IllegalArgumentException("Request body cannot be null");
        }

        // Checking that the name isn't null or just a bunch of empty spaces
        if (user.getName() == null || user.getName().trim().isEmpty()) {
            throw new IllegalArgumentException("Name is required");
        }

        // Age must be provided and has to be greater than 0
        if (user.getAge() == null || user.getAge() <= 0) {
            throw new IllegalArgumentException("Valid age is required");
        }

        // Role is mandatory as we wouldn't know their permissions
        if (user.getRole() == null || user.getRole().trim().isEmpty()) {
            throw new IllegalArgumentException("Role is required");
        }
    }

}