package com.ashutosh.session3.controller;

import com.ashutosh.session3.model.User;
import com.ashutosh.session3.service.UserService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.util.Map;
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

    // 2. Submit API
    // I mapped this to "/submit" for POST requests (so the full URL is POST /users/submit).
    // I used POST to save new data.
    @PostMapping("/submit")
    public ResponseEntity<Map<String, String>> submitData(
            // @RequestBody automatically takes the JSON string the user sent and converts it into our Java User object.
            // I added 'required = false' here This way, if someone sends a completely empty POST request,
            // my Service layer's validateUser() method can catch the 'null' and return custom error message
            // instead of Spring throwing a generic missing body error before it even reaches code
            @RequestBody(required = false) User user) {
        try {
            // Calling the service method to validate and save the user
            userService.saveUser(user);

            // I'm putting the response inside Map.of() so it gets sent back as proper, clean JSON
            // instead of just a raw text string.
            return ResponseEntity.status(HttpStatus.CREATED)
                    .body(Map.of("message", "User successfully created"));

        } catch (IllegalArgumentException e) {

            // If the user sends bad data (like a blank name), it
            // sends back a 400 BAD REQUEST status along with the exact error message.
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                    .body(Map.of("error", e.getMessage()));
        }
    }
}
