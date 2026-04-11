package com.ashutosh.session2.controller;

import com.ashutosh.session2.model.User;
import com.ashutosh.session2.service.UserService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

// Telling Spring this class is our web controller for users
@RestController
// @RequestMapping means all our endpoints here will start with "/users"
@RequestMapping("/users")
public class UserController {

    private final UserService userService;

    // constructor
    public UserController(UserService userService) {
        this.userService = userService;
    }

    // This method runs when someone sends a GET request to "/users"
    @GetMapping
    public ResponseEntity<List<User>> getAllUsers() {
        return ResponseEntity.ok(userService.getAllUsers());
    }

    // This method runs when someone wants a specific user, like a GET request to "/users/5"
    @GetMapping("/{id}")
    public ResponseEntity<User> getUserById(@PathVariable Long id) {
        return ResponseEntity.ok(userService.getUserById(id));
    }

    // This method runs when someone sends a POST request to create a new user
    @PostMapping
    public ResponseEntity<User> createUser(@RequestBody User user) {
        User created = userService.createUser(user);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }
}
