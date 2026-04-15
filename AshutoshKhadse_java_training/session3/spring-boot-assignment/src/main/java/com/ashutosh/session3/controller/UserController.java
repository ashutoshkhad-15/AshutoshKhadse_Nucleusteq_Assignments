package com.ashutosh.session3.controller;

import com.ashutosh.session3.model.User;
import com.ashutosh.session3.service.UserService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

// Setting this class up as a RestController so Spring knows it will handle incoming HTTP requests
@RestController
// I added @RequestMapping here at the class level to keep things clean.
// Now, all endpoints in this controller will automatically start with "/users"
@RequestMapping("/users")
public class UserController {

    private final UserService userService;

    // Strict Constructor Injection
    public UserController(UserService userService) {
        this.userService = userService;
    }

    // 1. Search API
    // This endpoint will now map to "/users/search" because of the class-level
    // mapping above.
    @GetMapping("/search")
    public ResponseEntity<List<User>> searchUsers(
            // By setting required = false, the client doesn't HAVE to provide these query
            // parameters.
            // If they skip one, Spring just passes 'null' to my variables, which works
            // perfectly
            // with the null-checking logic I wrote earlier in the UserService
            @RequestParam(required = false) String name,
            @RequestParam(required = false) Integer age,
            @RequestParam(required = false) String role) {

        // Passing whatever filters the user provided directly into our service logic
        List<User> results = userService.searchUsers(name, age, role);
        // Sending back the filtered list with a 200 OK status
        return ResponseEntity.ok(results);
    }
}
